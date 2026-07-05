import os
import csv
import math

# 指定你的图片文件夹路径
folder_path = './Ideal/'
# 指定输出的CSV文件路径（注意要指定完整文件路径和文件名）
csv_file_path = './out.csv'

# 曲率半径实际值（假设）
actual_radius = 0.855

# 标尺（你可以替换为实际的标尺值）
# scale = 0.02 * 10 / 172.01
scale = 0.02 * 10 / 155.2

# 确保文件夹路径存在
if not os.path.exists(folder_path):
    print(f"文件夹 {folder_path} 不存在！")
    exit()

# 使用'with'语句来自动处理文件的打开和关闭
with open(csv_file_path, mode='w', newline='', encoding='utf-8') as csv_file:
    # 创建一个csv.writer对象
    writer = csv.writer(csv_file)

    # 写入标题行
    writer.writerow(['Name', 'Radius'])

    # 遍历文件夹中的所有文件
    for filename in os.listdir(folder_path):
        # 检查文件是否为图片（这里只检查.jpg和.png）
        if filename.lower().endswith(('.jpg', '.jpeg', '.png', '.bmp')):
            # 获取图片宽度（假设可以用某个库获得图片宽度，例：PIL库）
            # 这里先假设图片宽度为一个固定值，你可以根据实际情况修改这部分代码
            # 如果你有图片处理库（比如Pillow），可以在这里获得图片的实际宽度。

            image_width = 640  # 假设图片宽度为640像素，实际值需要根据你的图片来获取

            # 计算归一化后的曲率半径
            normalized_radius = math.log(actual_radius / ((image_width - 1) * scale))

            # 写入文件名和归一化后的曲率半径到CSV
            filename = './Ideal/' + filename
            writer.writerow([filename, normalized_radius])

print(f"图片名称和归一化后的曲率半径已写入 {csv_file_path}")
