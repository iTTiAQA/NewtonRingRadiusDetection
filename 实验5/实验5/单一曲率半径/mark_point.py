import cv2
import json
# 创建一个全局列表来存储点击的坐标
click_positions = []


# 鼠标回调函数
def mouse_callback(event, x, y, flags, param):
    global click_positions
    if event == cv2.EVENT_LBUTTONDOWN:
        # 当左键点击时，记录坐标
        click_positions.append((x, y))
        print(f"点击位置: ({x}, {y})")

        # 在图像上标记点击位置
        cv2.circle(img, (x, y), 5, (0, 0, 255), -1)
        cv2.imshow("Image", img)


# 读取图像
img_path = input("请输入图像路径: ")  # 或者直接指定路径如 "image.jpg"
img = cv2.imread(img_path)
dsize = (720, 640)
# img = cv2.resize(img, dsize,  cv2.INTER_AREA)
y_size, x_size, cha = img.shape

if img is None:
    print("无法加载图像，请检查路径是否正确")
    exit()

try:
    # 创建窗口并设置鼠标回调函数
    cv2.namedWindow("Image")
    cv2.setMouseCallback("Image", mouse_callback)

    # 显示图像
    cv2.imshow("Image", img)
    print("在图像上点击鼠标左键记录坐标，按ESC键退出...")

    while True:
        key = cv2.waitKey(1) & 0xFF
        if key == 27:  # ESC键退出
            break
except KeyboardInterrupt:
    print("已强制退出")

# 退出前打印所有记录的坐标
print("\n所有记录的点击坐标:")
for i, pos in enumerate(click_positions, 1):
    print(f"{i}. ({pos[0]}, {int(y_size/2) - pos[1]})")

# 关闭所有窗口
cv2.destroyAllWindows()

# 保存标记后的图像
# cv2.imwrite("marked_image.jpg", img)

# 将坐标保存到JSON文件
if click_positions:
    x_max = float(input("x最大值："))
    y_min = float(input("y最小值："))
    y_max = float(input("y最大值："))
    name = img_path.split('.')[0] + "_coord.json"
    data = {
        "coordinates": [
            {"id": i, "x": pos[0], "y": int(y_size / 2) - pos[1]}
            for i, pos in enumerate(click_positions, 1)
        ],
        "x_range": (0, x_max),
        "y_range": (y_min, y_max)
    }

    with open(name, "w") as f:
        json.dump(data, f, indent=4)
        print(f"文件已保存为:{name}")
