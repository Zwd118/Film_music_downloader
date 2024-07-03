import os
import shutil   # 用来删除目录下所有文件
from tkinter import *
from tkinter import ttk, filedialog
import time
import requests
from fake_useragent import UserAgent
from lxml import etree  # 进行数据预处理,可以使用xpath等
import re
from concurrent.futures import ThreadPoolExecutor
import queue
import threading


class MainPage:
    def __init__(self, master):  #: tk.Tk是告诉类,我是tk.Tk里的东西,在以下编写代码时,会自动提示,不加上也无妨
        self.root = master
        # self.root = Tk()
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

        self.path_var = StringVar()
        self.films = []
        self.v = IntVar()
        self.html_primary = []
        self.line_url = ''
        self.sun_url = ''
        self.name = ''
        self.h_name = []
        self.films_name = ''
        self.time1 = time.time()
        self.name_film = None
        self.b1 = None
        self.text_pad = None
        self.button2 = None
        self.button1 = None
        self.thread_queue = None
        self.line = None
        self.text_mid_pad = None

        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36',
            'Cookie': 'recente=%5B%7B%22vod_name%22%3A%22%E7%8E%AB%E7%91%B0%E7%9A%84%E6%95%85%E4%BA%8B%22%2C%22vod_url%22%3A%22https%3A%2F%2Fwww.cqhpjn.com%2Fvodplay%2Fmeiguidegushi-1-38.html%22%2C%22vod_part%22%3A%22%E7%AC%AC38%E9%9B%86%22%7D%2C%7B%22vod_name%22%3A%22%E6%88%91%E7%9A%84%E6%84%8F%E5%A4%96%E5%AE%A4%E5%8F%8B%22%2C%22vod_url%22%3A%22https%3A%2F%2Fwww.cqhpjn.com%2Fvodplay%2Fwodeyiwaishiyou-1-2.html%22%2C%22vod_part%22%3A%22%E7%AC%AC02%E9%9B%86%22%7D%5D; Hm_lvt_f6a02b41c10d4961d9efe36e9f8fe72d=1719431521,1719460104,1719464345,1719467101; PHPSESSID=o5v18v2i3uv8oq26upi12d029l; cf_clearance=4rVNPIuPRArAWGaEntL4diSf8lBonAFYd46Z2T_6ULE-1719473867-1.0.1.1-zNQVGUMU5kHzg05DDXtdPPZkJnsTeUXlyTvZwU4Zz4MrlLXzC52cJYx1uCeOBa4NJ2Wk861IXQ68vSNoCBm1Nw; Hm_lpvt_f6a02b41c10d4961d9efe36e9f8fe72d=1719476835'
        }

        self.create_page()  # 创建新页面


    def create_page(self):
        """左边布局"""
        self.left_frame = Frame(self.root)
        self.left_frame.pack(side=LEFT, anchor=N, padx=5, pady=5)

        """左边布局 设置内容"""
        self.net_frame = LabelFrame(self.left_frame, text='设置内容', padx=5, pady=5)
        self.net_frame.pack()

        # (1)选择类型
        Label(self.net_frame, text='(1)选择类型').pack(anchor=W)
        self.film_type = ttk.Combobox(self.net_frame)  # ttk需要导入
        self.film_type['values'] = ['影视节目', '音乐歌曲', '文件传输']
        self.film_type.pack(anchor=W)
        self.film_type.current(0)  # 默认选中第一个

        # 打开文件夹,选择路径
        def get_path():
            path = filedialog.askdirectory()  # filedialog需要导入
            if path:
                self.path_var.set(path)

        # (2)存放路径 加载打开路径的图标
        image1 = PhotoImage(file="icon/open.gif").subsample(11, 11)
        # 把左右两边用一个Frame单独装起来
        frame_1 = Frame(self.net_frame, pady=10)
        frame_1.pack()
        # label靠上TOP独占一行
        Label(frame_1, text='(2)存放路径').pack(side=TOP, anchor=W)
        # 创建Button并设置图标,并且点击前面标题也一样进入文件夹选择
        # button靠右和entry同在一行上
        Button(frame_1, image=image1, command=get_path).pack(side=RIGHT, anchor=N)
        # entry靠左和button同在一行上
        entry_folder = Entry(frame_1, textvariable=self.path_var, font='Helvetica 12', width=24)
        entry_folder.pack(side=LEFT)
        self.path_var.set('D:\\video')

        # (3)线路选择
        Label(self.net_frame, text='(3)线路选择').pack(anchor=W, side='top')
        self.line = ttk.Combobox(self.net_frame)  # ttk需要导入
        self.line['values'] = ['线路一', '线路二', '线路三']
        self.line.pack(anchor=W)
        self.line.current(0)  # 默认选中第一个

        """左边布局 搜索内容"""
        search_frame = LabelFrame(self.left_frame, text='请输入名称搜索:', font=('黑体', 16), padx=5, pady=5)
        search_frame.pack(fill=X, padx=5, pady=25)

        # (1)搜索名称:
        self.frame_2 = Frame(search_frame)
        self.frame_2.pack()

        def get_film_name(line, un_url):  # name:要搜索的关键字, line:要下载网站的主页, un_url是上级传来的可下载的单片链接
            url = un_url  # 传来的格式: self.sun_url = f'{self.line_url}/vodsearch/-------------.html?wd={name}'
            # 1. 先请求影视网站主页
            resp = requests.get(url, headers=self.headers, timeout=30)
            films = []
            html_primary = []
            html_name = []
            if resp.status_code == 200:
                html = etree.HTML(resp.text)
                # 获取想要的影视剧
                html_primary = html.xpath('/html/body/div[1]/div/div[1]/div/div/div[2]/ul/li/div[1]/a/@href')
                html_name = html.xpath('/html/body/div[1]/div/div[1]/div/div/div[2]/ul/li/div[1]/a/@title')
                # html_nf1 = html.xpath('/html/body/div[1]/div/div[1]/div/div/div[2]/ul/li/div[2]/p[3]/span[4]/span[2]/text()')
                html_nf2 = html.xpath('/html/body/div[1]/div/div[1]/div/div/div[2]/ul/li/div[2]/p[3]/span[4]/text()')
                # ii = 0
                if len(html_primary) == 0:  # 再获取一遍
                    resp = requests.get(url, headers=self.headers)
                    # ii += 1
                    html = etree.HTML(resp.text)
                    html_primary = html.xpath('/html/body/div[1]/div/div[1]/div/div/div[2]/ul/li/div[1]/a/@href')
                    html_name = html.xpath('/html/body/div[1]/div/div[1]/div/div/div[2]/ul/li/div[1]/a/@title')
                    # html_nf1 = html.xpath('/html/body/div[1]/div/div[1]/div/div/div[2]/ul/li/div[2]/p[3]/span[4]/span[2]/text()')
                    html_nf2 = html.xpath('/html/body/div[1]/div/div[1]/div/div/div[2]/ul/li/div[2]/p[3]/span[4]/text()')

                if len(html_primary) != 0:
                    for ind, name in enumerate(html_name):
                        html_name[ind] = '<' + html_name[ind] + '>' + html_nf2[ind] + '年'
                    for ind, name in enumerate(html_name):
                        name = (name, ind)
                        films.append(name)
            return films, html_primary, line, html_name

        def get_film_js(va, html_primary, url_website, name):  # 获取集数
            # 先清空上次信息栏提示内容
            self.text_pad.delete('0.0', 'end')
            self.text_mid_pad.delete('0.0', 'end')

            self.time1 = time.time()
            # print(va, html_primary)
            # print('要获取的影视链接是:',html_primary[va])
            html_primary = ''.join(html_primary[va])  # 转成真正的字符串
            url_ys = url_website + html_primary  # url_website是影视网站最前链接,可能有多个,取第[0]个
            # print(url_ys)

            # 2. 把选择好的影视名链接,再次请求,得到集数链接
            re1 = requests.get(url_ys, headers=self.headers)
            if re1.status_code == 200:
                # 获取这部影视剧的各集链接
                html_re1 = etree.HTML(re1.text)
                html_js_lj = html_re1.xpath('//*[@id="playlist1"]/ul/li/a/@href')  # 集数链接
                html_dys = html_re1.xpath('//*[@id="playlist1"]/ul/li/a/text()')   # 判断是否电视剧类型
                # print(html_js_lj)
                if len(html_js_lj) == 0:  # 再获取一次
                    re1 = requests.get(url_ys, headers=self.headers)
                    html_re1 = etree.HTML(re1.text)
                    html_js_lj = html_re1.xpath('//*[@id="playlist1"]/ul/li/a/@href')  # 集数链接
                    html_dys = html_re1.xpath('//*[@id="playlist1"]/ul/li/a/text()')   # 判断是否电视剧类型
                # 3. 把集数链接再次请求,得到两个m3u8,进行拼凑成一个真实的m3u8链接
                if len(html_js_lj) == 0:
                    mjs = 1
                else:
                    mjs = len(html_js_lj)

                if '集' in html_dys[0]:
                    self.b1 = 1   # 确定是电视剧
                else:
                    self.b1 = 2   # 否则是电影

                print(f'{name}总共:{mjs}集')
                self.text_pad.insert(1.0, f'{name}总共:{mjs}集' + '\n')

                self.name_film = re.findall('<(.*?)>', self.films_name)[0]  # 取出真正的影视名字
                self.name_film = self.name_film.replace(' ', '')  # 把空格去掉
                # 删除临时的ts文件(先清空)
                shutil.rmtree(self.path_var.get() + '\\ts', ignore_errors=True)
                path_video_a = ''
                if self.b1 == 2:
                    os.makedirs(self.path_var.get() + '\\电影\\', exist_ok=True)  # 检查目录是否存在,不存在就建立
                    # self.b1 = 2
                    path_video = self.path_var.get() + '\\电影\\' + self.name_film + '.mp4'  # 电影目录
                else:
                    os.makedirs(self.path_var.get() + '\\电视剧\\' + self.name_film, exist_ok=True)  # 检查目录是否存在,不存在就建立
                    # self.b1 = 1
                    path_video = self.path_var.get() + "\\电视剧\\" + self.name_film   # + "\\第%03d集.mp4" % a1  # 生成的mp4文件要放的地方

                t = ThreadPoolExecutor(1)  # 线程池总数这台机器3比较合适,具体以后再调试
                for ind, item in enumerate(html_js_lj):
                    # 在这里可以再判断这一集是否存在于指定路径里,存在就不要再下载了!!!
                    if self.b1 == 1:
                        path_video_a = path_video + "\\第%03d集.mp4" % int(ind+1)
                    if self.b1 == 2:
                        path_video_a = path_video
                    if os.path.exists(path_video_a):
                        print(path_video_a.split('\\')[-1].split('.')[0], ', 已存在, 不再下载')
                        self.text_pad.insert('2.0', '\n' + path_video_a.split('\\')[-1].split('.')[0] + ', 已存在, 不再下载')
                        path_video_a = ''
                    else:
                        print(path_video_a.split('\\')[-1].split('.')[0], ', 正在下载...')
                        self.text_pad.insert('2.0', '\n' + path_video_a.split('\\')[-1].split('.')[0] + ', 正在下载...')
                        os.makedirs(self.path_var.get() + '\\ts\\' + str(ind + 1), exist_ok=True)  # 创建每一集的ts目录
                        t.submit(download, url_website, item, ind)  # 使用线程池
                        # download(url_website, item, ind)  # 不使用线程池
                        path_video_a = ''
                t.shutdown()
                time2 = time.time()
                print('总花费时间:' + str(time2 - self.time1)[:-12] + '秒')
                self.text_pad.insert('2.0', '已全下载完, 总花费时间:' + str(time2 - self.time1)[:-12] + '秒' + '\n')
            else:
                print('请求集数页面错误:', re1.status_code)
                self.text_pad.insert('2.0', '请求集数页面错误:', re1.status_code)

        def download(url_website, item, ind):
            url_js = url_website + item  # 每一集的链接
            re2 = requests.get(url_js, headers=self.headers)

            if re2.status_code == 200:
                if ind == 0:
                    ts_url = re.findall('"link_pre":"","url":"(.*?)","url_next":', re2.text)
                else:
                    ts_url = re.findall('html","url":"(.*?)","url_next":', re2.text)
                ii = 0
                while len(ts_url) == 0:
                    ii += 1
                    re2 = requests.get(url_js, headers=self.headers)
                    # ts_url = re.findall('index.m3u8","url_next":"(.*?)","from":', re2.text)
                    if ind == 0:
                        ts_url = re.findall('"link_pre":"","url":"(.*?)","url_next":', re2.text)
                    else:
                        ts_url = re.findall('html","url":"(.*?)","url_next":', re2.text)
                    # print(f'第{ind+1}集的第一个m3u8链接重新获取:', ii, '次')

                ts_url = ''.join(ts_url[0])  # 转成真正的字符串
                # 得到第一个m3u8链接
                ts_url = ts_url.replace('\\', '')
                m3u8_text = requests.get(ts_url, self.headers, timeout=30)  # 1分钟取不到数据就抛异常
                m3u8_text_status_code = m3u8_text.status_code
                if m3u8_text_status_code == 200:
                    m3u8_text = m3u8_text.text
                    m3u8_text = re.sub('#E.*', '', m3u8_text)
                    m3u8_text = m3u8_text.split()
                    # 得到第二个拼凑完整的有真正ts文件的m3u8链接
                    ts_url_1 = ts_url.replace('index.m3u8', '') + m3u8_text[0]
                    # print(f'第{ind + 1}集的第二个M3U8链接:', ts_url_1)
                    m3u8_text = requests.get(ts_url_1, self.headers, timeout=30).text  # 1分钟取不到数据就抛异常
                    m3u8_text = re.sub('#E.*', '', m3u8_text)
                    m3u8_text = m3u8_text.split()

                    mts = len(m3u8_text)
                    print(f'\r第{ind + 1}集ts总个数:', mts)
                    # self.text_pad.delete('2.0', 'end')
                    # self.text_pad.insert('2.0', f'第{ind + 1}集片段总个数:' + str(mts) + '\n')
                    # 至此,可以开始下载所有的ts链接到指定地方进行单集的拼凑

                    t1 = ThreadPoolExecutor(60)  # 线程池总数为mts个数的1倍,这里是要下载ts的
                    # for ind_ts, item_ts in enumerate(m3u8_text):  # m3u8_text是每一集的ts链接
                    for ind_ts in range(mts):  # m3u8_text是每一集的ts链接
                        t1.submit(download_ts, m3u8_text[ind_ts], ind_ts, ind, mts)  # 线程池:ind是第几集, ind_ts是这一集里的第几个ts, mts是总ts个数
                    t1.shutdown()
                    # 再次确定下载的ts还欠缺哪些没有下载到,补下载
                    defect_ts(m3u8_text, ind, mts)
                    # 写成一个MP4文件
                    write_mp4(ind + 1, self.b1, self.name_film, mts)  # ind+1是第几集, b1=1是电视剧=2是电影, c1(self.name_film)是影视名字,
                else:
                    print(f'请求第{ind+1}集第2个m3u8返回错误码:', m3u8_text_status_code)
                    self.text_pad.insert('2.0', f'请求第{ind+1}集第2个m3u8返回错误码:' + str(m3u8_text_status_code) + '\n')
            else:
                print(f'请求第{ind+1}集第1个m3u8返回错误码:', re2.status_code)
                self.text_pad.insert('2.0', f'请求第{ind+1}集第1个m3u8返回错误码:' + str(re2.status_code) + '\n')

        # 再次确定下载的ts还欠缺哪些没有下载到,补下载
        def defect_ts(m3u8_text, ind, mts):
            path_ts = self.path_var.get() + '\\ts\\' + str(ind + 1)
            # path_ts = self.path_var.get() + '\\ts\\' + str(ind + 1) + '\\{:04}.ts'.format(ind_ts)
            mts_dir = len(os.listdir(path_ts))   # 实际下载到的ts总数
            if mts-mts_dir != 0:
                # print(f'第{ind + 1}集ts个数差', mts - mts_dir,'个,正在补救...')
                # self.text_pad.insert('2.0', f'第{ind+1}集片段差:' + str(mts - mts_dir) + '正在补救...\n')
                t3 = ThreadPoolExecutor(10)  # 开启第三个线程池
                for i in range(mts):
                    file_path1 = path_ts + '\\%04d.ts' % i
                    if os.path.exists(file_path1) is False:
                        print(f'第{ind + 1}集片段差:', mts - mts_dir, '个,正在补下载:', file_path1.split('\\')[-1])
                        t3.submit(download_ts, m3u8_text[i], i, ind, mts)
                        # download_ts(m3u8_text[i], i, ind, mts)
                t3.shutdown()

        # 写成一个MP4文件
        def write_mp4(a1, b1, c1, mts):  # a1是第几集  b1=1电视剧=2电影, c1是影视名字, mts应有ts总数
            path_ts = self.path_var.get() + "\\ts\\" + str(a1)  # 临时存放ts文件
            mts_dir = len(os.listdir(path_ts))   # 实际下载到的ts总数
            path_video = ""
            print('正在写入:第' + str(a1) + '集...')
            if b1 == 1:
                path_video = self.path_var.get() + "\\电视剧\\" + c1 + "\\第%03d集.mp4" % a1  # 生成的mp4文件要放的地方
            if b1 == 2:
                path_video = self.path_var.get() + '\\电影\\' + c1 + '.mp4'  # 电影目录
            # 将ts目录下的所有文件保存到file_list列表中
            file_list = sorted(os.listdir(path_ts))
            # 将file_list列表写成固定格式: file_0000.ts 这样的格式保存到file_list.txt中
            with open(path_ts + "\\file_list.txt", "w+") as f:
                for file in file_list:
                    f.write("file '{}'\n".format(file))
            ffmpeg_bin_dic = 'D:\\ffmpeg\\bin\\ffmpeg -f concat -safe 0 -y -i '
            # ffmpeg_bin_dic = 'D:\\ffmpeg\\ffmpeg-2024-06-13-git-0060a368b1-essentials_build\\bin\\ffmpeg -f concat -safe 0 -y -i '
            # 写成指定的一个mp4文件
            os.system(ffmpeg_bin_dic + path_ts + '\\file_list.txt' + ' -c ' + ' copy ' + path_video + r'> nul 2> nul')
            # 删除临时的ts文件
            # os.system(r'@echo y | del ' + path_ts + r'\*.* > nul 2> nul')  # > nul 2> nul表示不在控制台输出结果提示,并且会在最后自动按Y确认删除
            # shutil.rmtree(path_ts, ignore_errors=True)  # 这句比上局好用理解
            if mts - mts_dir != 0:
                print('第', a1, '集已完成, 片段差:', mts - mts_dir, '个')
                # self.text_pad.delete('2.0', '2.14')
                self.text_pad.insert('2.0', '第' + str(a1) + '集已完成, 片段差:' + str(mts - mts_dir)+'个\n')
            else:
                print('第', a1, '集已完成, 片段完整')
                # self.text_pad.delete('2.0', '2.14')
                self.text_pad.insert('2.0', '第' + str(a1) + '集已完成, 片段完整' + '\n')

        def download_ts(item_ts, ind_ts, ind, mts):   # item_ts第ind_ts个ts的url,  ind_ts第几个ts, ind第几集, mts总共的ts个数
            # if self.line == 1:
                # 每次给个随机头,线路二可能不行
            self.headers = {'User-Agent': UserAgent().random}
            response = requests.get(item_ts, headers=self.headers, timeout=30)
            path_ts = self.path_var.get() + '\\ts\\' + str(ind + 1) + '\\{:04}.ts'.format(ind_ts)
            if response.status_code != 404:
                try:
                    with open(path_ts, 'wb') as f:  # 直接用index命名
                        f.write(response.content)
                except IOError as e:
                    print(f'Write failed: {e}')
            else:
                print('请求item_ts时错误!')
                self.text_pad.insert('2.0', '请求item_ts时错误!' + '\n')

            if os.path.exists(path_ts) is False:
                print(path_ts.split('\\')[-1], '此片段没有下载成功')
                self.text_pad.insert('2.0', path_ts.split('\\')[-1] + '此片段没有下载成功' + '\n')
            # print('\r第'+str(ind+1)+'集:' + str(ind_ts + 1) + '/' + str(mts))
            self.text_mid_pad.insert(1.0, '第'+str(ind+1)+'集:' + str(ind_ts + 1) + '/' + str(mts)+'\n')

        def worker():
            self.va = self.v.get()
            self.films_name = self.h_name[self.va]
            get_film_js(self.va, self.html_primary, self.line_url, self.films_name)
            self.button1.config(state=ACTIVE)
            self.button2.config(state=ACTIVE)

        def get_js():  # 获取集数
            self.button1.config(state=DISABLED)
            self.button2.config(state=DISABLED)
            thread = threading.Thread(target=worker)
            thread.start()
            # self.va = self.v.get()
            # get_film_js(self.va, self.html_primary, self.line_url, self.h_name[self.va])

        def get_film():  # 获取影片名字
            self.frame_2.destroy()  # 把原先搜索显示的影片内容清空
            self.name = search_name.get()
            if self.name:
                type = self.film_type.current() + 1  # (1)选择类型
                # path = self.path_var.get()  # (2)存放路径
                line = self.line.current() + 1  # (3)线路选择
                # self.films = []                       # 先清空

                if type == 1:  # 影视类型,网上搜:影视资源,会出来很多网站供选择使用于线路
                    if line == 1:  # 线路一(片库)
                        self.line_url = 'https://www.zhidiudiu.com'
                        self.sun_url = f'{self.line_url}/vodsearch/-------------.html?wd={self.name}'  # 拼成完整的可以搜索的链接
                    if line == 2:  # 线路二(全能影视)
                        # self.line_url = 'https://www.cqhpjn.com'  (这个是全网集,需要验证,未完成)
                        self.line_url = 'https://www.sjzamys.com/'
                        self.sun_url = f'{self.line_url}/vodsearch/-------------.html?wd={self.name}'  # 拼成完整的可以搜索的链接
                    if line == 3:  # 线路三(电影码头)
                        self.line_url = 'https://www.sqacfs.com/'
                        self.sun_url = f'{self.line_url}/search/-------------.html?wd={self.name}'  # 拼成完整的可以搜索的链接

                elif type == 2 and line == 1 or line == 2 or line == 3:  # 音乐类型
                    self.line_url = 'https://www.gequbao.com/s/'  # (放屁网和歌曲宝)音乐暂时三个选一样,以后找到好的,再替换上
                elif type == 3 and line == 1 or line == 2 or line == 3:  # 文件类型
                    self.line_url = ''  # (文件下载)暂时三个选一样,以后找再完善

                self.films, self.html_primary, self.line_url, self.h_name = get_film_name(self.line_url,
                                                                                          self.sun_url)  # 返回影视名字+年份 和 影视短链接 和 主页链接
                self.frame_2 = Frame(search_frame)
                if self.films:
                    for film, num in self.films:
                        b = Radiobutton(self.frame_2, text=film, variable=self.v, value=num, font=('思源宋体', 13),
                                        width=20, anchor="w")
                        b.pack()
                    button1 = Button(self.frame_2, text='开始下载', command=get_js, font=('方正兰亭黑简体', 15))
                    button1.pack(anchor=CENTER, pady=2)
                    self.button1 = button1
                else:
                    Label(self.frame_2, text='没找到,或再试一次!', font=('思源宋体', 18), fg='red').pack()
                self.frame_2.pack(anchor="w", padx=0, pady=5)

        search_name = StringVar()
        Entry(search_frame, textvariable=search_name, font=('楷体', 18), bg="Wheat").pack(pady=10, anchor=W, side=TOP)

        button2 = Button(search_frame, text='开始搜索', command=get_film, font=('方正兰亭黑简体', 15))
        button2.pack(anchor=CENTER, fill=X)
        self.button2 = button2

        """中间布局"""
        right_frame = Frame(self.root)
        right_frame.pack(side=LEFT, padx=0, pady=0, fill=Y)

        info_frame = Frame(right_frame)
        info_frame.pack()
        Label(info_frame, text='信息提示栏').pack(anchor=CENTER)

        self.text_pad = Text(info_frame, width=32, height=30)
        self.text_pad.pack(side=LEFT, fill=X)

        # send_text_bar = Scrollbar(info_frame)
        # send_text_bar.pack(side=RIGHT, fill=Y)

        Button(right_frame, text='退出', command=self.root.destroy).pack(side='bottom')

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

        self.root.mainloop()


if __name__ == '__main__':
    root = Tk()
    MainPage(root)
    # root.mainloop()
