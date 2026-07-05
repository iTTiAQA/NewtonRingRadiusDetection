import os
import csv


def create_csv_from_images(folder_path, output_csv, fixed_ruler="0.0000156847982"):
    """
    遍历指定文件夹中的 .jpg 文件，根据文件命名格式解析信息，
    并将图片路径、横坐标、纵坐标、曲率半径及固定标尺写入 CSV 文件。

    文件命名示例：6-0.8551-100-257-0-1.jpg
        - 第二部分：曲率半径 (0.8551)
        - 第三部分：横坐标 (100)
        - 第四部分：纵坐标 (257)

    Args:
        folder_path (str): 包含图片的文件夹路径。
        output_csv (str): 输出 CSV 文件路径。
        fixed_ruler (str): 固定标尺值，默认 "0.005/318.78"。
    """
    with open(output_csv, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        # 写入表头：图片位置、横坐标、纵坐标、曲率半径、标尺
        writer.writerow(["image_path", "x_center", "y_center", "radius", "ruler"])

        # 遍历文件夹内所有文件
        for filename in os.listdir(folder_path):
            if filename.lower().endswith(".jpg"):
                full_path = os.path.join(folder_path, filename)
                # 假设文件名按照 '-' 分隔，例如 "6-0.8551-100-257-0-1.jpg"
                parts = filename.split('-')
                if len(parts) < 4:
                    print(f"Skipping file {filename} due to unexpected format.")
                    continue

                try:
                    # 根据约定：parts[1] 为曲率半径，parts[2] 为横坐标，parts[3] 为纵坐标
                    radius = float(parts[1])
                    x_center = float(parts[2])
                    # 注意：如果 parts[3] 包含文件后缀，需要先去除后缀
                    y_str = parts[3]
                    if '.' in y_str:
                        # parts[3] 可能类似 "257" 或 "257.jpg"；若有点，则去掉后缀
                        y_center = float(y_str.split('.')[0])
                    else:
                        y_center = float(y_str)
                except ValueError as e:
                    print(f"Skipping file {filename} due to parse error.")
                    print(e)
                    continue

                writer.writerow([full_path, x_center, y_center, radius, fixed_ruler])

    print(f"CSV 文件已生成：{output_csv}")


# 使用示例
if __name__ == "__main__":
    # folder_path = "./enhanced_data/"  # 请替换为实际图片文件夹路径
    # output_csv = "./enhanced_data/data.csv"
    folder_path = "./data/test_ruler"  # 请替换为实际图片文件夹路径
    output_csv = "./data/test_ruler/data.csv"
    create_csv_from_images(folder_path, output_csv)
