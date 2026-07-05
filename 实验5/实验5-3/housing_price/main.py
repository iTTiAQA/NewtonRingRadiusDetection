import numpy as np
import pandas as pd
import torch
from model import MLP  # 确保导入你的MLP模型


# 1. 加载训练好的模型
def load_model(model_path, input_size):
    model = MLP()  # 必须与训练时的结构一致
    model.load_state_dict(torch.load(model_path))
    model.eval()  # 设置为评估模式
    return model


# 2. 数据预处理（必须与训练时一致）
def preprocess_data(X):
    ones = np.ones((X.shape[0], 1))  # 添加偏置列
    X_processed = np.hstack((ones, X))
    return torch.from_numpy(X_processed).float()


# 3. 计算MSE
def compute_mse(model, X, y_true, device="cpu"):
    # 预处理数据
    X_tensor = preprocess_data(X).to(device)
    y_true_tensor = torch.from_numpy(y_true).float().to(device)

    # 预测
    with torch.no_grad():
        y_pred = model(X_tensor)

    # 计算MSE
    mse = torch.mean((y_pred - y_true_tensor) ** 2).item()
    return mse, y_pred.cpu().numpy()


# 示例使用
if __name__ == "__main__":
    # 加载数据（假设数据格式与训练时相同）
    df = pd.read_csv("./housing.csv", delim_whitespace=True)
    arr = df.to_numpy(dtype='float32')
    X = arr[:, :-1]  # 特征
    y = arr[:, -1:]  # 标签（保持二维）

    # 划分训练集和测试集（与训练时一致）
    np.random.seed(42)
    indices = np.random.permutation(len(X))
    train_size = int(0.9 * len(X))
    X_train, y_train = X[indices[:train_size]], y[indices[:train_size]]
    X_test, y_test = X[indices[train_size:]], y[indices[train_size:]]

    # 加载模型（假设模型输入维度=原始特征数+1（偏置项））
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    model = load_model("./checkpoint/net_weight.pth", input_size=X_train.shape[1] + 1)
    model.to(device)

    # 计算测试集MSE
    test_mse, test_pred = compute_mse(model, X_test, y_test, device)
    print(f"测试集MSE: {test_mse:.4f}")

    # 可选：打印前5个预测值与真实值对比
    print("\n预测值 vs 真实值（前5个样本）:")
    for i in range(5):
        print(f"样本{i + 1}: 预测={test_pred[i][0]:.2f}, 真实={y_test[i][0]:.2f}")

    # 可视化部分结果
    import matplotlib.pyplot as plt

    plt.scatter(y_test, test_pred, alpha=0.5)
    plt.plot([y_test.min(), y_test.max()], [y_test.min(), y_test.max()], 'r--')
    plt.xlabel("real")
    plt.ylabel("pre")
    plt.title("pre vs real")
    plt.show()
