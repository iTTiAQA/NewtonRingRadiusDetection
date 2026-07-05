import torch
import torch.nn as nn


class MLP(nn.Module):
    def __init__(self):
        super(MLP, self).__init__()

        # 定义模型的全连接层结构
        self.FC = nn.Sequential(
            nn.Linear(14, 50),  # 输入维度为14，输出维度为50的全连接层
            nn.GELU(),  # GELU激活函数
            nn.Linear(50, 50),  # 输入维度为50，输出维度为50的全连接层
            nn.GELU(),  # GELU激活函数
            nn.Linear(50, 1),  # 输入维度为50，输出维度为1的全连接层
        )

    def forward(self, x):
        y_pred = self.FC(x)  # 前向传播，得到模型输出
        return y_pred

# 随机生成输入张量，形状为(505, 14)
input = torch.randn(505 ,14)
# 创建MLP模型实例
model = MLP()
# 打印模型输出的形状
print(model(input).shape)
