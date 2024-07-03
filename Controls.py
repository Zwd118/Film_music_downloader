from tkinter import *
from tkinter import filedialog
import share
import type


class Controls(Frame):
    def __init__(self):  # , film_type, path_var, line, frame_2, button2, text_pad, text_mid_pad, search_frame
        super().__init__()          # 这里好像用不到父类Frame的东西,去掉也无妨
        # 在共享模块中获取数据
        self.shared = share.SharedData()

    def get_path(self, event):   # 选择存放目录
        path = filedialog.askdirectory()  # filedialog需要导入
        self.path_var = self.shared.get('path_var')  # (2)路径
        if path:
            self.path_var.set(path)

    def get_film(self):  # 获取影片名字
        self.name = self.shared.get('search_name').get()  # 要搜索的影片,音乐,文件关键字
        if self.name:
            self.film_type_sure = self.shared.get('film_type').current() + 1  # (1)选择类型 最终用self.film_type_sure表示
            self.line_sure = self.shared.get('line').current() + 1  # (3)线路选择
            self.shared.set('film_type_sure', self.film_type_sure)
            self.shared.set('line_sure', self.line_sure)
            self.shared.set('name', self.name)

            if self.film_type_sure == 1:  # 影视类型 (网上搜:影视资源,会出来很多网站供选择使用于线路)
                type.TypeOne()
            elif self.film_type_sure == 2 and self.line_sure == 1 or self.line_sure == 2 or self.line_sure == 3:  # 音乐类型
                type.TypeTwo()
            elif self.film_type_sure == 3 and self.line_sure == 1 or self.line_sure == 2 or self.line_sure == 3:  # 文件类型
                type.TypeThree()
