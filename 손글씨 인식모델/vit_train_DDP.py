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

from dataset import Hanguldataset
from model import Vit





def setup(rank, world_size):
    os.environ['MASTER_ADDR'] = 'localhost'
    os.environ['MASTER_PORT'] = '12355'

    # initialize the process group
    dist.init_process_group("nccl", rank=rank, world_size=world_size)
def cleanup():
    dist.destroy_process_group()


def train(args, model, device, train_loader, optimizer, epoch, rank,criterion):

    model.train()
    running_loss = 0
    total_correct = 0
    for i,(img,target) in enumerate(train_loader):
        
        img = img.to(rank)
        target = target.to(rank)
        
        outputs = model(img)
        
        
        loss = criterion(outputs, target)
        
        optimizer.zero_grad() # model의 gradient 값을 0으로 설정
        loss.backward() # backward 함수를 호출해 gradient 계산
        optimizer.step() # 모델의 학습 파라미터 업데이트

        
        running_loss += loss.item() / len(train_loader)
        
        _, predicted = torch.max(outputs, 1)
        correct = (predicted == target).sum().item() 
        total_correct += correct
        
        dist.all_reduce(loss, op=dist.ReduceOp.SUM)
        if(rank == 0):
            
            print(f'[{len(train_loader)}/{i}] step loss : {loss:.4f} \t accuracy : {correct/args.batch_size*100:.2f}% \t{correct}/{args.batch_size}')    
    
    if(rank == 0):
        print(f"{epoch} epoch train loss : {running_loss:.4f} \t accuracy : {total_correct/(args.batch_size*len(train_loader))*100:.2f}% \t {total_correct}/{args.batch_size*len(train_loader)}")
        print("\n")

    
def trainer(rank, world_size, args):
    setup(rank, world_size)
    #-----------------------------------#

    torch.manual_seed(args.seed)
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    train_transform = transforms.Compose([transforms.Resize((args.image_size,args.image_size)), transforms.ToTensor(),transforms.Normalize((0.32232735,), (0.3991284,))])
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

    test_transform = transforms.Compose([transforms.Resize((args.image_size,args.image_size)), transforms.ToTensor(),transforms.Normalize((0.32232735,), (0.3991284,))])
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
    
    
    model = Vit(img_size=args.image_size,patch_size=16,in_chans=1,n_classes=2350,embed_dim=768,n_heads=12,depth=12).to(rank)

    model = DDP(model, device_ids=[rank])
    

    optimizer = optim.Adadelta(model.parameters(), lr=args.lr)
    # optimizer = optim.NAdam(model.parameters(),  lr=args.lr)
    
    criterion = torch.nn.CrossEntropyLoss().to(rank)

    for epoch in range(1, args.epochs + 1):
        train(args, model, device, train_loader, optimizer, epoch, rank,criterion)
    #     scheduler.step()

    cleanup()


    

def main():
    # Training settings
    parser = argparse.ArgumentParser(description='PyTorch MNIST Example')
    parser.add_argument('--batch-size', type=int, default=16, metavar='N',
                        help='input batch size for training (default: 128)')
    
    parser.add_argument('--test-batch-size', type=int, default=128, metavar='N',
                        help='input batch size for testing (default: 1000)')
    
    parser.add_argument('--image_size', type=int, default=128, metavar='N',
                        help='input image size for training (default: 128)')
    
    parser.add_argument('--epochs', type=int, default=1000, metavar='N',
                        help='number of epochs to train (default: 200)')
    
    parser.add_argument('--lr', type=float, default=0.001, metavar='LR',
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


