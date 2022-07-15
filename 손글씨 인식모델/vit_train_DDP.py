from __future__ import print_function
import argparse
import torch
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim
from torchvision import datasets, transforms
from torch.optim.lr_scheduler import StepLR
from torch.nn.parallel import DistributedDataParallel as DDP
import torch.multiprocessing as mp
import torch.distributed as dist
import os
from model import Vit
from dataset import Hanguldataset


def setup(rank, world_size):
    os.environ['MASTER_ADDR'] = 'localhost'
    os.environ['MASTER_PORT'] = '12355'

    # initialize the process group
    dist.init_process_group("nccl", rank=rank, world_size=world_size)
def cleanup():
    dist.destroy_process_group()

def train(args, model, device, train_loader, optimizer, epoch, rank):
    model.train()
    criterion = nn.CrossEntropyLoss()
    for batch_idx, (data, target) in enumerate(train_loader):

        data, target = data.to(rank), target.to(rank)
        optimizer.zero_grad()
        output = model(data)
        loss = criterion(output, target)
        loss.backward()
        optimizer.step()

        if batch_idx % args.log_interval == 0:
            dist.all_reduce(loss, op=dist.ReduceOp.SUM)

            if(rank == 0):
                print('Train Epoch: {} [{}/{} ({:.0f}%)]\tLoss: {:.6f}'.format(
                    epoch, batch_idx * len(data), len(train_loader.dataset),
                    100. * batch_idx / len(train_loader), loss.item()))


def test(model,  test_loader, rank):
    model.eval()
    test_loss = 0
    correct = 0
    data_len = 0
    test_loss_tensor = 0
    correct_tensor = 0

    with torch.no_grad():
        for data, target in test_loader:

            data, target = data.to(rank), target.to(rank)
            output = model(data)
            test_loss += F.cross_entropy(output, target, reduction='sum').item()  # sum up batch loss
            test_loss_tensor += F.cross_entropy(output, target, reduction='sum')
            pred = output.argmax(dim=1, keepdim=True)  # get the index of the max log-probability
            correct += pred.eq(target.view_as(pred)).sum().item()
            correct_tensor += pred.eq(target.view_as(pred)).sum()
            data_len += len(data)

    test_loss /= data_len

    dist.all_reduce(test_loss_tensor, op=dist.ReduceOp.SUM)
    dist.all_reduce(correct_tensor, op=dist.ReduceOp.SUM)

    if(rank == 0):
        print("Test average loss: {}, correct predictons: {}, total: {}, accuracy: {:3f}% \n".format(test_loss_tensor.item() / len(test_loader.dataset), correct_tensor.item(), len(test_loader.dataset),
             100.0 * correct_tensor.item() / len(test_loader.dataset)))

    #print('\nTest  set: Average loss: {:.4f}, Accuracy: {}/{} ({:.4f}%)\n'.format(
    #        test_loss, correct, data_len,
    #        100. * correct / data_len))
    
    
def trainer(rank, world_size, args):
    setup(rank, world_size)
    #-----------------------------------#

    torch.manual_seed(args.seed)

    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

    train_transform = transforms.Compose([transforms.Resize((args.image_size,args.image_size)),transforms.RandomRotation(25), transforms.ToTensor()])
    train_dataset = Hanguldataset(g_target_char_txt=args.target_char_txt,ttf_dir=args.train_ttf_dir,transform=train_transform)
  
    train_sampler = torch.utils.data.distributed.DistributedSampler(
        train_dataset,
        num_replicas=world_size,
        rank=rank)

    train_loader = torch.utils.data.DataLoader(
        dataset=train_dataset,
        batch_size=args.batch_size,
        shuffle=False,            
        num_workers=0,
        pin_memory=True,
        sampler=train_sampler)    


    test_transform = transforms.Compose([transforms.Resize((args.image_size,args.image_size)), transforms.ToTensor()])
    test_dataset = Hanguldataset(g_target_char_txt=args.target_char_txt,ttf_dir=args.val_ttf_dir,transform=test_transform)

    test_sampler = torch.utils.data.distributed.DistributedSampler(
        test_dataset,
        num_replicas=world_size,
        rank=rank
    )

    test_loader = torch.utils.data.DataLoader(
        dataset=test_dataset,
        batch_size=args.batch_size,
        shuffle=False,            
        num_workers=0,
        pin_memory=True,
        sampler=test_sampler)
    
    
    model = Vit(img_size=args.image_size,patch_size=4,in_chans=1,n_classes=2350,embed_dim=128,n_heads=8,depth=8).to(rank)

    model = DDP(model, device_ids=[rank])
    

    optimizer = optim.Adam(model.parameters(), lr=args.lr)

    for epoch in range(1, args.epochs + 1):
        train(args, model, device, train_loader, optimizer, epoch, rank)
        test(model, test_loader, rank)
    #     scheduler.step()

    cleanup()


    

def main():
    # Training settings
    parser = argparse.ArgumentParser(description='PyTorch MNIST Example')
    parser.add_argument('--batch-size', type=int, default=16, metavar='N',
                        help='input batch size for training (default: 64)')
    parser.add_argument('--test-batch-size', type=int, default=16, metavar='N',
                        help='input batch size for testing (default: 1000)')
    parser.add_argument('--image_size', type=int, default=64, metavar='N',
                        help='input image size for training (default: 64)')
    parser.add_argument('--epochs', type=int, default=1000, metavar='N',
                        help='number of epochs to train (default: 200)')
    parser.add_argument('--lr', type=float, default=0.01, metavar='LR',
                        help='learning rate (default: 0.001)')
    parser.add_argument('--gpus', type=int, default=2, metavar='N',
                        help='Number of GPUs')
    parser.add_argument('--seed', type=int, default=1, metavar='S',
                        help='random seed (default: 1)')
    parser.add_argument('--log-interval', type=int, default=1, metavar='N',
                        help='how many batches to wait before logging training status')
    parser.add_argument('--save-model', action='store_true', default=False,
                        help='For Saving the current Model')
    parser.add_argument('--train_ttf_dir', default="../data/ttf_file",
                        help='train ttf file dir')
    parser.add_argument('--val_ttf_dir', default="../data/ttf_file",
                        help='val ttf file dir')
    parser.add_argument('--target_char_txt', default="../data/target.txt",
                        help='val ttf file dir')
    
    args = parser.parse_args()

    world_size = args.gpus

    if torch.cuda.device_count() > 1:
      print("쿠다 사용", torch.cuda.device_count(), "GPUs! but using ",world_size," GPUs")

    #########################################################
    mp.spawn(trainer, args=(world_size, args), nprocs=world_size, join=True)    
    #########################################################


if __name__ == '__main__':
    main()