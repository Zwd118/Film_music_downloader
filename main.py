import threading
from tkinter import *
from tkinter import ttk, filedialog
import Controls as Ct   # 自定义类,用于控制选项及输出内容
import share


class MainPage:
    def __init__(self):
        self.root = Tk()
        width, height = 840, 840
        width_max, height_max = self.root.maxsize()  # 整个屏幕的宽高
        s_center = '%dx%d+%d+%d' % (width, height, (width_max - width) / 2, (height_max - height) / 2)  # 计算出居中位置
        self.root.geometry(s_center)  # 窗口位置,居中效果
        self.root.title('影视音乐下载管理器 V2024.06.23')  # 窗口标题
        self.root.resizable(width=True, height=True)  # 是否可以拉伸
        # 设置全局字体大小
        self.root.option_add('*Font', 'Helvetica 15')
        # 移除窗口的标题栏
        # self.root.overrideredirect(True)
        # 添加你的窗口内容
        win_frame = Frame(self.root)
        win_frame.pack(pady=10)
        label_title1 = Label(win_frame, text="影视音乐下载管理器", pady=10, font=('黑体', 20, 'bold'))
        label_title2 = Label(win_frame, text="V2024.06.23", font=('宋体', 15))
        label_title1.pack(side="left", anchor=W)
        label_title2.pack(side=RIGHT)

        self.shared = share.SharedData()   # 创建共享数据对象

        """左边布局"""
        self.left_frame = Frame(self.root)
        self.left_frame.pack(side=LEFT, anchor=N, padx=5, pady=5)

        """左边布局 之 设置内容"""
        self.net_frame = LabelFrame(self.left_frame, text='设置内容', padx=5, pady=5)
        self.net_frame.pack()

        # (1)选择类型  变量:self.film_type
        Label(self.net_frame, text='(1)选择类型').pack(anchor=W)
        self.film_type = ttk.Combobox(self.net_frame)  # ttk需要导入
        self.film_type['values'] = ['影视节目', '音乐歌曲', '文件传输']
        self.film_type.pack(anchor=W)
        self.film_type.current(0)  # 默认选中第一个

        # (2)存放路径 变量: self.path_var ,  执行get_path函数确认存放路径
        self.path_var = StringVar()
        self.path_var.set('D:\\video')

        image1 = PhotoImage(file="icon/open.gif").subsample(11, 11)
        # 把左右两边用一个Frame单独装起来
        frame_1 = Frame(self.net_frame, pady=10)
        frame_1.pack()
        # label靠上TOP独占一行
        Label(frame_1, text='(2)存放路径').pack(side=TOP, anchor=W)
        # 创建Button并设置图标,并且点击前面标题也一样进入文件夹选择
        # button靠右和entry同在一行上
        ''''存放路径按钮'''
        self.but_path = Button(frame_1, image=image1)
        self.but_path.pack(side=RIGHT, anchor=N)
        # entry靠左和button同在一行上
        entry_folder = Entry(frame_1, textvariable=self.path_var, font='Helvetica 12', width=24)
        entry_folder.pack(side=LEFT)

        # (3)线路选择 变量:self.line
        Label(self.net_frame, text='(3)线路选择').pack(anchor=W, side='top')
        self.line = ttk.Combobox(self.net_frame)  # ttk需要导入
        self.line['values'] = ['线路一', '线路二', '线路三']
        self.line.pack(anchor=W)
        self.line.current(0)  # 默认选中第一个

        """左边布局 之 搜索内容"""
        self.search_frame = LabelFrame(self.left_frame, text='请输入名称搜索:', font=('黑体', 16), padx=5, pady=5)
        self.search_frame.pack(fill=X, padx=5, pady=25)

        # (1)搜索名称: 变量:self.search_name, 执行函数get_film搜索影片名字
        self.frame_2 = Frame(self.search_frame)
        # self.frame_2.pack()

        self.search_name = StringVar()
        Entry(self.search_frame, textvariable=self.search_name, font=('楷体', 18), bg="Wheat").pack(pady=10, anchor=W, side=TOP)
        self.button2 = Button(self.search_frame, text='开始搜索', font=('方正兰亭黑简体', 15))

        """中间布局"""
        right_frame = Frame(self.root)
        right_frame.pack(side=LEFT, padx=0, pady=0, fill=Y)

        """"中间布局 之 上部分  变量:self.text_pad"""
        info_frame_top = Frame(right_frame)
        info_frame_top.pack()
        Label(info_frame_top, text='信息提示栏').pack(anchor=CENTER)

        self.text_pad = Text(info_frame_top, width=32, height=16)
        self.text_pad.pack(side=LEFT, fill=X)

        # send_text_bar = Scrollbar(info_frame)
        # send_text_bar.pack(side=RIGHT, fill=Y)

        """"中间布局 之 中间部分 变量: self.text_pad_mil"""
        info_frame_mil = Frame(right_frame)
        info_frame_mil.pack()
        Label(info_frame_mil, text='片段个数', font=('宋体', 12)).pack(anchor=CENTER)

        self.text_pad_mil = Text(info_frame_mil, width=32, height=8)
        self.text_pad_mil.pack(side=LEFT, fill=X)

        """"中间布局 之 下部分  变量: self.text_pad_bot"""
        info_frame_bot = Frame(right_frame)
        info_frame_bot.pack()
        Label(info_frame_bot, text='错误信息', fg='red', font=('楷体', 12)).pack(anchor=CENTER)

        self.text_pad_bot = Text(info_frame_bot, width=36, height=4, fg='red', font=('楷体', 15))
        self.text_pad_bot.pack(side=LEFT, fill=X)

        Button(right_frame, text='退出', command=self.root.destroy,padx=10,anchor=CENTER).pack(side='bottom',pady=10)

        """右边布局"""
        middle_frame = Frame(self.root)
        middle_frame.pack(side=RIGHT, padx=0, pady=0, fill=Y)

        inform_frame = Frame(middle_frame)
        inform_frame.pack()
        Label(inform_frame, text='片段提示栏').pack(anchor=CENTER)

        self.text_mid_pad = Text(inform_frame, width=17, height=30)
        self.text_mid_pad.pack(side=LEFT)

        send_text_bar = Scrollbar(inform_frame)
        send_text_bar.pack(side=RIGHT, fill=Y)

        ct = Ct.Controls()  # 创建自定义类对象

        def get_film():
            self.frame_2.pack()
            # 先删除frame_2里的子控件
            for widget in self.frame_2.winfo_children():
                widget.destroy()
            Label(self.frame_2, text='正在搜索...', font=('思源宋体', 18), fg='red').pack()
            thread = threading.Thread(target=ct.get_film)
            thread.start()  # 这里单独给主界面一个线程,避免界面在后边多线程池使用时卡住未响应


        self.but_path.bind("<Button-1>", ct.get_path)  # "<Button-1>",鼠标左键 绑定选择路径
        # self.button2.bind("<Button-1>", ct.get_film)   # "<Button-1>",鼠标左键 绑定搜索名称,这个按钮动画会失效,不好
        self.button2 = Button(self.search_frame, text='开始搜索', font=('方正兰亭黑简体', 15), command=get_film)
        self.button2.pack(anchor=CENTER, fill=X)
        # self.label_2 = Label(self.frame_2, text='正在搜索...', font=('思源宋体', 18), fg='red')

        # 用自定义共享模块share.py传参

        self.shared.set('film_type', self.film_type)
        self.shared.set('path_var', self.path_var)
        self.shared.set('line', self.line)
        self.shared.set('search_name', self.search_name)
        self.shared.set('frame_2', self.frame_2)
        self.shared.set('text_pad', self.text_pad)
        self.shared.set('text_mid_pad', self.text_mid_pad)
        self.shared.set('search_frame', self.search_frame)
        self.shared.set('left_frame', self.left_frame)
        self.shared.set('text_pad_mil', self.text_pad_mil)   # 中间之中间
        self.shared.set('text_pad_bot', self.text_pad_bot)   # 中间之下部
        self.shared.set('button2', self.button2)   # 中间之下部
        # self.shared.set('label_2', self.label_2)   # 中间之下部

        self.root.mainloop()  # 循环放在这里,选择路径那个图标才会显示,因为放在底下main里,还未创建图标就已经循环了,所以就显示不了图标


if __name__ == '__main__':
    MainPage()
