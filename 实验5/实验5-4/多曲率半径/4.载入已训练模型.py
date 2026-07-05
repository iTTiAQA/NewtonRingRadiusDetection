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

DATA_PATH = "./data/test_ruler/"
FILE_NAME = "train_radius_results_test.csv"


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


def train_transform(seed=123456):
    return T.Compose([
        T.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
    ])


dataset_seed = 42

train_data = NewtonRingDataset_ruler(
    csv_file=os.path.join(DATA_PATH, 'data.csv'),
    root_dir=DATA_PATH,
    transform=train_transform(dataset_seed)
)

batch_size = 64
train_dataloader = DataLoader(train_data, batch_size=batch_size, shuffle=True)

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
print("Using device:", device)


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


model = ResNetBasedModelRadius(backbone).to(device)
model_path = "resnet_based_model_for_radius.pth"

# 检查是否有保存的模型
if os.path.exists(model_path):
    # 2. 从本地加载已经训练好的模型
    print(f"Loading trained model from {model_path}")
    model.load_state_dict(torch.load(model_path))
    model.eval()
    print("==========模型载入完成==========")
else:
    print("模型未保存，请检查")


train_results = collect_results_radius(model, train_dataloader, device)
train_results_df = pd.DataFrame(train_results)
print(train_results_df)
train_results_df.to_csv(FILE_NAME, index=False)
