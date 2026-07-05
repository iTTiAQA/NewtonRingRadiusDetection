import os
from traditional import analyse_sig


class BatchRename:
    def __init__(self):
        self.path = './my_data/850'  # 图片的路径

    def rename(self, if_ana, r):
        filelist = os.listdir(self.path)
        filelist.sort()
        total_num = len(filelist)  # 获取文件中有多少图片
        i = 0  # 文件命名从哪里开始（即命名从哪里开始）
        for item in filelist:
            if item.endswith('.jpg'):
                if if_ana:
                    img_path = os.path.join(self.path, item)
                    x, y, _ = analyse_sig(img_path)
                    print(f"得到数据：{x, y, _}")
                    target_name = "1-" + str(r) + "-" + str(x) + "-" + str(y) + "-" + "-ruler-"
                else:
                    target_name = "6-0.8551-100-257-0-" + str(i)
                src = os.path.join(self.path, item)
                dst = os.path.join(os.path.abspath(self.path), target_name + '.jpg')

                try:
                    os.rename(src, dst)
                    print('converting %s to %s ...' % (src, dst))
                    i = i + 1
                except Exception as e:
                    print(e)
                    print('rename dir fail\r\n')

        print('total %d to rename & converted %d jpgs' % (total_num, i))


if __name__ == '__main__':
    demo = BatchRename()  # 创建对象
    demo.rename(if_ana=True, r=0.855)  # 调用对象的方法
