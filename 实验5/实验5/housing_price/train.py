import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# 导入MLP模型类
from model import MLP

import torch.optim as optim
import torch
import torch.nn as nn
import argparse

# 命令行参数解析
parser = argparse.ArgumentParser()
parser.add_argument('--batchSize', type=int, default=4, help='input batch size')
parser.add_argument('--nEpochs', type=int, default=100, help='number of epochs to train for')
parser.add_argument('--LR', type=float, default=0.001, help='learning rate for net')
opt = parser.parse_args()

# 数据集预处理
df = pd.read_csv("./housing.csv", delim_whitespace=True)

# 转换为Numpy数组
arr = df.to_numpy(dtype='float')

# 分割特征和标签
X = arr[:, :-1]
y = np.expand_dims(arr[:, -1], 1)

# 添加偏置列
ones = np.ones((X.shape[0], 1))
X_new = np.hstack((ones, X))

# 将数据集分割为训练集和测试集
indices = np.random.permutation(X_new.shape[0])
train_indices, test_indices = indices[:int(0.9 * X_new.shape[0])], indices[int(0.9 * X_new.shape[0]):]
X_train, X_test = X_new[train_indices, :], X_new[test_indices, :]
y_train, y_test = y[train_indices, :], y[test_indices, :]

# 创建MLP模型实例
model = MLP()

# 检测是否支持GPU，如果支持，则将模型移至GPU上进行计算
device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
model.to(device)

# 设置模型为训练模式
model.train()

# 选择优化器，学习率为opt.LR
optim_model =  optim.Adam(model.parameters(), lr=opt.LR)

# 定义代价函数
criterion = nn.MSELoss()

# 将numpy数组转换为PyTorch张量，并移动到相应设备
X_train_tensor = torch.from_numpy(X_train).float().to(device)
y_train_tensor = torch.from_numpy(y_train).float().to(device)
X_test_tensor = torch.from_numpy(X_test).float().to(device)
y_test_tensor = torch.from_numpy(y_test).float().to(device)

# 训练模型
for epoch in range(opt.nEpochs):
# 在这里编写训练循环代码
    # START CODE HERE
    # 前向传播
    outputs = model(X_train_tensor)  # 获取模型预测
    loss = criterion(outputs, y_train_tensor)  # 计算损失

    # 反向传播和优化
    optim_model.zero_grad()  # 清空梯度
    loss.backward()  # 反向传播计算梯度
    optim_model.step()  # 更新参数

    # 每10个epoch打印一次训练信息
    if (epoch + 1) % 10 == 0:
        print(f'轮次 [{epoch + 1}/{opt.nEpochs}], 训练损失: {loss.item():.4f}')

    # 在测试集上评估模型性能
    with torch.no_grad():  # 禁用梯度计算
        model.eval()  # 设置模型为评估模式
        test_outputs = model(X_test_tensor)
        test_loss = criterion(test_outputs, y_test_tensor)
        model.train()  # 恢复训练模式

        if (epoch + 1) % 10 == 0:
            print(f'测试损失: {test_loss.item():.4f}')
    # END CODE HERE

# 保存训练好的模型参数
torch.save(model.state_dict(), "./checkpoint/net_weight.pth")
