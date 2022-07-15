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
from resnet import ResNet50




torch.manual_seed(1234)
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
train_transform = transforms.Compose([transforms.Resize((128,128)), transforms.ToTensor()])
train_dataset = Hanguldataset(g_target_char_txt="../data/target.txt",ttf_dir="../data/ttf_file",transform=train_transform)

train_loader = torch.utils.data.DataLoader(
    dataset=train_dataset,
    batch_size=64,
    shuffle=False,            
    num_workers=0,
    pin_memory=True)    


test_transform = transforms.Compose([transforms.Resize((128,128)), transforms.ToTensor()])
test_dataset = Hanguldataset(g_target_char_txt="../data/target.txt",ttf_dir="../data/ttf_file",transform=test_transform)

test_loader = torch.utils.data.DataLoader(
    dataset=test_dataset,
    batch_size=64,
    shuffle=False,            
    num_workers=0,
    pin_memory=True)

batch_size = 64

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model = ResNet50(img_channel=1,num_classes=2350)
model = model.to(device)
optimizer = optim.Adam(model.parameters(), lr=0.001)

criterion = torch.nn.CrossEntropyLoss().to(device)

for epoch in range(0,100):
    model.train()
    running_loss = 0
    total_correct = 0
    for i,(img,target) in enumerate(train_loader):
        
        img = img.to(device)
        target = target.to(device)
        
        outputs = model(img)
        
        optimizer.zero_grad() # model의 gradient 값을 0으로 설정
        loss = criterion(outputs, target)
        loss.backward() # backward 함수를 호출해 gradient 계산
        optimizer.step() # 모델의 학습 파라미터 갱신
        
        running_loss += loss.item() / len(train_loader)
        
        _, predicted = torch.max(outputs, 1)
        correct = (predicted == target.to(device)).sum().item() 
        total_correct += correct
        
        if i % 20 == 0:
            print(f'[{len(train_loader)}/{i}]\t loss : {loss:.4f} \t accuracy : {correct/batch_size*100:.2f}% \t{correct}/{batch_size}')    
    

    print(f"{epoch} epoch 평균 train loss : {running_loss} \t accuracy : {total_correct/(batch_size*len(train_loader))*100:.2f}% \t {total_correct}/{batch_size*len(train_loader)}")
    print("\n")
    