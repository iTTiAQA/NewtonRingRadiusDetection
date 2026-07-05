import numpy as np
import pandas as pd

# 1.从名为housing.csv的CSV文件中读取数据，使用空白字符作为分隔符。
# 2.将数据框转换为Numpy数组，并打印数组的形状信息。
# 3.代码中缺少将特征和标签分割的部分以及将数据集分割为训练集和测试集的部分，需要在相应位置添加代码。
# 4.最后，注释中提到了使用正规方程求解θ，但是这部分代码也需要补充。

# 从CSV文件中读取数据
df = pd.read_csv("./housing.csv", delim_whitespace=True)

# 输出数据框的维度
print(f"数据维度：{df.shape}")

# 将数据框转换为Numpy数组，指定数据类型为浮点型
arr = df.to_numpy(dtype='float')
print(f"数组形状：{arr.shape}")

# 分割特征和标签
X = arr[:, :-1]
y = np.expand_dims(arr[:, -1], 1)

# 添加偏置列
ones = np.ones((X.shape[0], 1))
X_new = np.hstack((ones, X))

# 在这里添加代码将特征和标签分割开
# 通常使用80-20或70-30的比例分割，这里使用80-20
split_ratio = 0.8
split_index = int(arr.shape[0] * split_ratio)

# 随机打乱数据
np.random.seed(42)  # 设置随机种子保证可重复性
shuffled_indices = np.random.permutation(arr.shape[0])
train_indices = shuffled_indices[:split_index]
test_indices = shuffled_indices[split_index:]

# 在这里添加代码将数据集分割为训练集和测试集
X_train = X[train_indices, :]
y_train = y[train_indices]
X_test = X[test_indices, :]
y_test = y[test_indices]

print("训练集特征形状:", X_train.shape)
print("训练集标签形状:", y_train.shape)
print("测试集特征形状:", X_test.shape)
print("测试集标签形状:", y_test.shape)

# 使用正规方程求解θ
# 正规方程公式：θ = (XᵀX)⁻¹Xᵀy
# 首先需要给特征矩阵X添加一列全1的偏置项
X_train_with_bias = np.c_[np.ones((X_train.shape[0], 1)), X_train]

# 计算θ
theta = np.linalg.inv(X_train_with_bias.T.dot(X_train_with_bias)).dot(X_train_with_bias.T).dot(y_train)

print("通过正规方程计算得到的参数θ:")
print(theta)

# 可以使用θ在测试集上进行预测
X_test_with_bias = np.c_[np.ones((X_test.shape[0], 1)), X_test]
y_pred = X_test_with_bias.dot(theta)

# 计算均方误差(MSE)
mse = np.mean((y_pred - y_test) ** 2)
print("测试集上的均方误差(MSE):", mse)

# 可视化部分结果
import matplotlib.pyplot as plt

plt.scatter(y_test, y_pred, alpha=0.5)
plt.plot([y_test.min(), y_test.max()], [y_test.min(), y_test.max()], 'r--')
plt.xlabel("real")
plt.ylabel("pre")
plt.title("pre vs real")
plt.show()