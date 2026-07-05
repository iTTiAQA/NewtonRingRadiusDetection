import os
import copy
import random
import math
import time
import pathlib

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

import torch
from torch import nn
import torch.optim as optim
from torch.utils.data import Dataset, DataLoader, random_split
from torchvision.io import read_image
import torchvision.transforms as T
from torchvision import models
from torchvision import transforms, models
from PIL import Image

train_path = "./data/train_less/"
test_path = "./data/test_ruler/"


# -------------------------
# 数据集定义：NewtonRingDataset_ruler
# -------------------------
class NewtonRingDataset_ruler(Dataset):
    """ 用于加载牛顿环数据集 """
    def __init__(self, csv_file, root_dir, transform=None):
        """
        Args:
            csv_file (string): CSV 文件路径，包含图像文件名、中心坐标、半径、标尺等。
            root_dir (string): 图像所在的根目录。
            transform (callable, optional): 图像转换函数。
        """
        self.data_frame = pd.read_csv(csv_file)
        self.root_dir = root_dir
        self.transform = transform

    def __len__(self):
        return len(self.data_frame)

    def __getitem__(self, idx):
        img_name = self.data_frame.iloc[idx, 0]
        img_path = img_name
        image = (1/255) * read_image(img_path).float()
        if image.shape[0] == 1:
            image = image.expand(3, -1, -1)
        radius = self.data_frame.iloc[idx, 3].astype(np.float32)
        ruler = self.data_frame.iloc[idx, -1].astype(np.float32)
        if self.transform:
            image = self.transform(image[:3, :, :])
        radius = torch.tensor([radius]).float()
        ruler = torch.tensor(ruler).float()
        return image, radius, ruler

# -------------------------
# 数据增强 & 转换
# -------------------------
# def train_transform(seed=123456):
#     random.seed(seed)
#     torch.manual_seed(seed)
#     color_jitter = T.ColorJitter(0.4, 0.4, 0.4, 0.1)
#     transform = T.Compose([
#         T.RandomApply([T.GaussianBlur(kernel_size=(5, 9), sigma=(0.1, 5))], p=0.8),
#         T.RandomApply([color_jitter], p=0.6),
#         T.RandomGrayscale(p=0.2),
#         T.Normalize(mean=[0.485, 0.456, 0.406],
#                     std=[0.229, 0.224, 0.225]),
#         # transforms.RandomHorizontalFlip(),
#         # transforms.RandomRotation(20),
#     ])
#     return transform


def train_transform(seed=123456):
    return T.Compose([
        T.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
    ])


def test_transform():
    transform = T.Compose([
        T.Normalize(mean=[0.485, 0.456, 0.406],
                    std=[0.229, 0.224, 0.225]),
        transforms.Resize((224, 224)),  # 调整图像大小
    ])
    return transform


# -------------------------
# 数据加载及划分
# -------------------------
dataset_seed = 42

train_data = NewtonRingDataset_ruler(
    csv_file=os.path.join(train_path, 'data.csv'),
    root_dir=train_path,
    transform=train_transform(dataset_seed)
)

val_test_data = NewtonRingDataset_ruler(
    csv_file=os.path.join(test_path, 'data.csv'),
    root_dir=test_path,
    transform=test_transform()
)

test_len = int((1/5) * len(val_test_data))
val_len = len(val_test_data) - test_len
val_set, test_set = random_split(val_test_data, [val_len, test_len])

batch_size = 64
train_dataloader = DataLoader(train_data, batch_size=batch_size, shuffle=True)
val_dataloader = DataLoader(val_set, batch_size=batch_size, shuffle=False)
test_dataloader = DataLoader(test_set, batch_size=batch_size, shuffle=False)

# -------------------------
# 定义基于 ResNet 的模型（只预测曲率半径）
# -------------------------
resnet = models.resnet18(pretrained=False)
backbone = nn.Sequential(*list(resnet.children())[:-1])


class ResNetBasedModelRadius(nn.Module):
    def __init__(self, backbone):
        super(ResNetBasedModelRadius, self).__init__()
        self.backbone = backbone
        self.head_radius = nn.Sequential(
            nn.Linear(512, 256),
            nn.ReLU(),
            nn.Linear(256, 128),
            nn.ReLU(),
            nn.Linear(128, 1)
        )

    def forward(self, x):
        features = self.backbone(x)
        features = torch.flatten(features, 1)
        radius = self.head_radius(features)
        return radius


def count_parameters(model):
    return sum(p.numel() for p in model.parameters() if p.requires_grad)


# -------------------------
# 设备、模型及优化器设置
# -------------------------
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
print("Using device:", device)

model = ResNetBasedModelRadius(backbone).to(device)
print("Trainable parameters:", count_parameters(model))

optimizer = optim.AdamW(model.parameters(), lr=1e-3, weight_decay=1e-2)
# scheduler = optim.lr_scheduler.ReduceLROnPlateau(optimizer, mode='min', factor=0.3, patience=10, verbose=True)


# 修改后的Huber—exp损失
class Huber_Loss(nn.Module):
    def __init__(self, tau=1.0, gamma=1.0):
        super(Huber_Loss, self).__init__()
        self.tau = tau
        self.gamma = gamma

    def forward(self, pred, target):
        diff = torch.abs(pred - target)
        loss = torch.where(
            diff < self.tau,
            0.5 * diff ** 2,
            0.5 *  (self.gamma + self.tau ** 2) * (1 - self.gamma/(self.gamma + self.tau ** 2) * torch.exp((self.tau ** 2 - diff ** 2)/ self.gamma))
        )
        return torch.mean(loss)


criterion_radius = Huber_Loss(tau=0.01, gamma=1000.0)

# -------------------------
# 训练及验证循环（只预测曲率半径）
# -------------------------
num_epochs = 100


import time

# Initialize total training time
total_start_time = time.time()

for epoch in range(num_epochs):
    epoch_start_time = time.time()  # Start time for each epoch
    model.train()
    running_loss = 0.0
    for images, radii, rulers in train_dataloader:
        images = images.to(device)
        radii = radii.to(device)
        optimizer.zero_grad()
        pred_radii = model(images)
        loss = criterion_radius(pred_radii, radii)
        loss.backward()
        optimizer.step()
        running_loss += loss.item() * images.size(0)

    epoch_loss = running_loss / len(train_dataloader.dataset)
    epoch_end_time = time.time()  # End time for each epoch
    epoch_duration = epoch_end_time - epoch_start_time  # Duration of this epoch

    print(f"Epoch {epoch + 1}/{num_epochs}, Train Loss: {epoch_loss:.4f}, Epoch Time: {epoch_duration:.2f} seconds")

    model.eval()
    val_loss = 0.0
    with torch.no_grad():
        for images, radii, rulers in val_dataloader:
            images = images.to(device)
            radii = radii.to(device)
            pred_radii = model(images)
            loss = criterion_radius(pred_radii, radii)
            val_loss += loss.item() * images.size(0)

    val_loss /= len(val_dataloader.dataset)
    print(f"Epoch {epoch + 1}/{num_epochs}, Validation Loss: {val_loss:.4f}")

# Total training time
total_end_time = time.time()
total_duration = total_end_time - total_start_time
print(f"Total Training Time: {total_duration:.2f} seconds")

torch.save(model.state_dict(), "resnet_based_model_for_radius.pth")


# -------------------------
# 收集结果：直接使用模型预测值，不进行逆归一化
# -------------------------
def collect_results_radius(model, dataloader, device):
    results = []
    model.eval()
    with torch.no_grad():
        for img, radii, rulers in dataloader:
            img = img.to(device)
            radii = radii.to(device).float()
            rulers = rulers.to(device).float()
            pred_radii = model(img)
            pred_radii = pred_radii.cpu().numpy()
            true_radii = radii.cpu().numpy()
            rulers = rulers.cpu().numpy()
            for i in range(img.size(0)):
                true_radius_val = true_radii[i]
                pred_radius_val = pred_radii[i]
                radius_err = abs(true_radius_val - pred_radius_val) / true_radius_val
                results.append({
                    'true_radius': true_radius_val,
                    'predicted_radius': pred_radius_val,
                    'radius_error': radius_err,
                    'ruler': rulers[i]
                })
    return results


train_results = collect_results_radius(model, train_dataloader, device)
train_results_df = pd.DataFrame(train_results)
print(train_results_df)
train_results_df.to_csv("train_radius_results.csv", index=False)

test_results = collect_results_radius(model, test_dataloader, device)
test_results_df = pd.DataFrame(test_results)
print(test_results_df)
test_results_df.to_csv("test_radius_results.csv", index=False)

val_results = collect_results_radius(model, val_dataloader, device)
val_results_df = pd.DataFrame(val_results)
print(val_results_df)
val_results_df.to_csv("val_radius_results.csv", index=False)
