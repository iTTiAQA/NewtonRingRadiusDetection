import os
from torchvision import transforms, models
from PIL import Image

# 定义数据增强变换（不转换为 Tensor，也不归一化，便于保存成图片）
augment_transform = transforms.Compose([
    transforms.Resize((224, 224)),  # 调整图像大小为224x224
    transforms.RandomHorizontalFlip(),  # 随机水平翻转图像
    transforms.RandomRotation(20),  # 随机旋转图像，角度范围在-20到20度之间
    transforms.RandomCrop(224, padding=4),  # 随机裁剪图像，裁剪后的大小为224x224，边缘填充4个像素
])


def augment_folder(src_folder, dst_folder, target_count):
    """
    从 src_folder 中读取图片，对每张图片进行数据增强，
    生成总数达到 target_count 的图片，并保存到 dst_folder 中。
    保存文件名格式：<原图片名>_XXXXX.jpg，如：image_00001.jpg
    """
    os.makedirs(dst_folder, exist_ok=True)  # 如果目标文件夹不存在，则创建目标文件夹
    image_list = sorted(os.listdir(src_folder))  # 获取源文件夹中的所有图片文件名并排序
    n_images = len(image_list)  # 获取源文件夹中图片的数量

    # 计算每张图片生成的扩充数
    base_count = target_count // n_images  # 每张图片生成的基础扩充次数
    remainder = target_count % n_images  # 前 remainder 张图片会多生成一次扩充

    print(f"Processing folder {src_folder} with {n_images} images. "
          f"Each image will be augmented {base_count} times, "
          f"with first {remainder} images getting one extra augmentation.")

    global_count = 0  # 记录所有生成图片的总数
    # 遍历源文件夹中的所有图片
    for i, img_name in enumerate(image_list):
        img_path = os.path.join(src_folder, img_name)  # 获取当前图片的完整路径
        try:
            original_img = Image.open(img_path).convert("RGB")  # 打开并转换为RGB模式
        except Exception as e:
            print(f"Error loading image {img_path}: {e}")  # 如果读取图片失败，打印错误信息
            continue

        # 计算当前图片需要生成的扩充数
        num_aug = base_count + (1 if i < remainder else 0)  # 前 remainder 张图片多生成一次
        delta_count = 50  # 每处理50张报告一次
        for j in range(num_aug):
            if i % delta_count == 0:
                print(f"已处理{i}张图像")
            aug_img = augment_transform(original_img)  # 对原始图片应用数据增强变换
            global_count += 1  # 生成图片计数加1

            # 文件名格式：原文件名_XXXXX.jpg，确保生成的文件名唯一
            save_name = f"{os.path.splitext(img_name)[0]}_{global_count:05d}.jpg"  # 原图片名 + _XXXXX
            save_path = os.path.join(dst_folder, save_name)  # 保存路径

            aug_img.save(save_path)  # 保存增强后的图片
    print(f"Completed augmentation for {src_folder}: {global_count} images saved to {dst_folder}")


def run_augmentation():
    # 源文件夹路径，存放原始图片
    src_folder1 = './data/test_ruler'

    # 目标文件夹路径，保存增强后的图片
    dst_folder = './data/train_less'

    # 每个文件夹扩充到target张图片
    target_count = 10000

    # 对两个源文件夹进行增强处理
    augment_folder(src_folder1, dst_folder, target_count)


run_augmentation()
