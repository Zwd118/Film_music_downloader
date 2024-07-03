import os
import re
import shutil
import threading
import time
from concurrent.futures import ThreadPoolExecutor
from fake_useragent import UserAgent
from lxml import etree  # 进行数据预处理,可以使用xpath等
from tkinter import *
import requests
import share


class One:
    def __init__(self):
        self.shared = share.SharedData()
        # self.film_type = self.shared.get('film_type_sure')  # 都等于1:影视
        self.line = self.shared.get('line_sure')
        self.name = self.shared.get('name')
        self.frame_2 = self.shared.get('frame_2')
        self.search_frame = self.shared.get('search_frame')
        # self.v = self.shared.get('v')
        self.button2 = self.shared.get('button2')
        self.text_pad = self.shared.get('text_pad')
        self.text_mid_pad = self.shared.get('text_mid_pad')
        self.path_var = self.shared.get('path_var')
        self.left_frame = self.shared.get('left_frame')
        self.text_pad_mil = self.shared.get('text_pad_mil')  # 中间之中间
        self.text_pad_bot = self.shared.get('text_pad_bot')  # 中间之下部
        self.v = IntVar()  # 用于影片列表
        self.headers = {
            'Referer': 'https://www.zhidiudiu.com',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36',
            'Cookie': 'PHPSESSID=vpak2pagkineb6uond2nt0ta0r; recente=%5B%7B%22vod_name%22%3A%22%E8%BF%9F%E6%97%A9%E9%81%87%E8%A7%81%E4%BD%A0%22%2C%22vod_url%22%3A%22https%3A%2F%2Fwww.zhidiudiu.com%2Fvodplay%2F66209-1-3.html%22%2C%22vod_part%22%3A%22%E7%AC%AC03%E9%9B%86%22%7D%2C%7B%22vod_name%22%3A%22%E4%B8%8D%E5%8F%AF%E5%BF%98%E6%80%80%22%2C%22vod_url%22%3A%22https%3A%2F%2Fwww.zhidiudiu.com%2Fvodplay%2F15716-1-1.html%22%2C%22vod_part%22%3A%22HD%E4%B8%AD%E5%AD%97%22%7D%2C%7B%22vod_name%22%3A%22%E8%9D%89%E7%BF%BC%22%2C%22vod_url%22%3A%22https%3A%2F%2Fwww.zhidiudiu.com%2Fvodplay%2F64833-1-1.html%22%2C%22vod_part%22%3A%22HD%22%7D%2C%7B%22vod_name%22%3A%22%E7%8E%AB%E7%91%B0%E7%9A%84%E6%95%85%E4%BA%8B%22%2C%22vod_url%22%3A%22https%3A%2F%2Fwww.zhidiudiu.com%2Fvodplay%2F63784-1-38.html%22%2C%22vod_part%22%3A%22%E7%AC%AC38%E9%9B%86%22%7D%2C%7B%22vod_name%22%3A%22%E7%B9%81%E8%8A%B1%20%E5%9B%BD%E8%AF%AD%E7%89%88%22%2C%22vod_url%22%3A%22https%3A%2F%2Fwww.zhidiudiu.com%2Fvodplay%2F12727-1-1.html%22%2C%22vod_part%22%3A%22%E7%AC%AC01%E9%9B%86%22%7D%2C%7B%22vod_name%22%3A%22%E7%89%A7%E5%B8%88%E7%A5%9E%E6%8E%A2%E7%AC%AC%E4%B9%9D%E5%AD%A3%22%2C%22vod_url%22%3A%22https%3A%2F%2Fwww.zhidiudiu.com%2Fvodplay%2F65399-1-3.html%22%2C%22vod_part%22%3A%22%E7%AC%AC03%E9%9B%86%22%7D%2C%7B%22vod_name%22%3A%22%E6%88%91%E7%9A%84%E6%84%8F%E5%A4%96%E5%AE%A4%E5%8F%8B%22%2C%22vod_url%22%3A%22https%3A%2F%2Fwww.zhidiudiu.com%2Fvodplay%2F65699-1-1.html%22%2C%22vod_part%22%3A%22%E7%AC%AC01%E9%9B%86%22%7D%2C%7B%22vod_name%22%3A%22%E4%B8%91%E9%97%BB2024%22%2C%22vod_url%22%3A%22https%3A%2F%2Fwww.zhidiudiu.com%2Fvodplay%2F64971-1-3.html%22%2C%22vod_part%22%3A%22%E7%AC%AC03%E9%9B%86%22%7D%2C%7B%22vod_name%22%3A%22%E6%97%A0%E4%BA%BA%E4%B9%8B%E5%A2%83%22%2C%22vod_url%22%3A%22https%3A%2F%2Fwww.zhidiudiu.com%2Fvodplay%2F65811-1-1.html%22%2C%22vod_part%22%3A%22%E7%AC%AC01%E9%9B%86%22%7D%2C%7B%22vod_name%22%3A%22%E5%BD%A9%E8%99%B9%E8%80%81%E7%88%B8%22%2C%22vod_url%22%3A%22https%3A%2F%2Fwww.zhidiudiu.com%2Fvodplay%2F65863-1-1.html%22%2C%22vod_part%22%3A%22HD%22%7D%5D',
            'Sec-Ch-Ua': '"Not/A)Brand";v="8", "Chromium";v="126", "Google Chrome";v="126"'
        }
        self.line_url = 'https://www.zhidiudiu.com'  # (这个是片库网)
        self.sun_url = f'{self.line_url}/vodsearch/-------------.html?wd={self.name}'  # 拼成完整的可以搜索的链接

    def get_film_name(self):  # sun_url是上级传来的可下载的单片链接
        url = self.sun_url  # 传来的格式: self.sun_url = f'{self.line_url}/vodsearch/-------------.html?wd={name}'
        # 1. 先请求影视网站主页
        resp = requests.get(url, headers=self.headers, timeout=15)
        films = []
        html_primary = []
        html_name = []
        if resp.status_code == 200:
            html = etree.HTML(resp.text)
            # html_primary获取影视名字的短链接列表:['/voddetail/12299.html',...]
            html_primary = html.xpath('/html/body/div[1]/div/div[1]/div/div/div[2]/ul/li/div[1]/a/@href')
            # html_name,得到列表:['大明王朝1566',...]
            html_name = html.xpath('/html/body/div[1]/div/div[1]/div/div/div[2]/ul/li/div[1]/a/@title')
            # html_nf2,得到列表:['2007',...]
            html_nf2 = html.xpath('/html/body/div[1]/div/div[1]/div/div/div[2]/ul/li/div[2]/p[3]/span[4]/text()')

            if len(html_primary) == 0:  # 再获取一遍
                resp = requests.get(url, headers=self.headers, timeout=15)
                html = etree.HTML(resp.text)
                # html_primary获取影视名字的短链接列表:['/voddetail/12299.html',...]
                html_primary = html.xpath('/html/body/div[1]/div/div[1]/div/div/div[2]/ul/li/div[1]/a/@href')
                # html_name,得到列表:['大明王朝1566',...]
                html_name = html.xpath('/html/body/div[1]/div/div[1]/div/div/div[2]/ul/li/div[1]/a/@title')
                # html_nf2,得到列表:['2007',...]
                html_nf2 = html.xpath('/html/body/div[1]/div/div[1]/div/div/div[2]/ul/li/div[2]/p[3]/span[4]/text()')

            if len(html_primary) != 0:
                for ind, name in enumerate(html_name):
                    html_name[ind] = '<' + html_name[ind] + '>' + html_nf2[ind] + '年'
                for ind, name in enumerate(html_name):
                    name = (name, ind)
                    films.append(name)

            # 销毁self.frame_2所有子控件
            for widget in self.frame_2.winfo_children():
                widget.destroy()

            if films:  # self.films
                for film, num in films:
                    self.b = Radiobutton(self.frame_2, text=film, variable=self.v, value=num, font=('思源宋体', 13),
                                         width=20, anchor="w")
                    self.b.pack()
                self.button1 = Button(self.frame_2, text='开始下载', command=self.get_js, font=('方正兰亭黑简体', 15))
                self.button1.pack(anchor=CENTER, pady=2)

            else:
                Label(self.frame_2, text='没找到,或再试一次!', font=('思源宋体', 18), fg='red').pack()
            self.frame_2.pack(anchor="w", padx=0, pady=5)

            """
            返回的格式为:
            films: [('<大明王朝1566>2007年', 0)] 或
                   [('<剑王朝之孤山剑藏>2020年', 0), ('<剑王朝之九境长生>2020年', 1), ('<古驰家族>2021年', 2)] 
            html_primary: ['/voddetail/12299.html'] 或
                          ['/voddetail/60109.html', '/voddetail/60107.html', '/voddetail/59201.html']  
            html_name: ['<大明王朝1566>2007年'] 或
                       ['<剑王朝之孤山剑藏>2020年', '<剑王朝之九境长生>2020年', '<古驰家族>2021年']

            films, 这个好像不用返回,没用            
            """
        self.html_primary = html_primary
        self.h_name = html_name
        # return html_primary, html_name

    def get_js(self):  # 获取集数
        self.button1.config(state=DISABLED)
        self.button2.config(state=DISABLED)
        thread = threading.Thread(target=self.worker)
        thread.start()  # 这里单独给主界面一个线程,避免界面在后边多线程池使用时卡住未响应

    def worker(self):
        self.va = self.v.get()
        self.films_name = self.h_name[self.va]
        self.get_film_js(self.va, self.html_primary, self.line_url, self.films_name)
        self.button1.config(state=ACTIVE)
        self.button2.config(state=ACTIVE)

    def get_film_js(self, va, html_primary, url_website, name):  # 获取集数
        # 先清空上次信息栏提示内容
        self.text_pad.delete('0.0', 'end')
        self.text_mid_pad.delete('0.0', 'end')
        self.text_pad_mil.delete('0.0', 'end')
        self.text_pad_bot.delete('0.0', 'end')

        self.time1 = time.time()
        # print(va, html_primary)
        # print('要获取的影视链接是:',html_primary[va])
        html_primary = ''.join(html_primary[va])  # 转成真正的字符串
        url_ys = url_website + html_primary  # url_website是影视网站最前链接,可能有多个,取第[0]个
        # print(url_ys)

        # 2. 把选择好的影视名链接,再次请求,得到集数链接
        re1 = requests.get(url_ys, headers=self.headers, timeout=15)
        if re1.status_code == 200:
            # 获取这部影视剧的各集链接
            html_re1 = etree.HTML(re1.text)
            html_js_lj = html_re1.xpath('//*[@id="playlist1"]/ul/li/a/@href')  # 集数链接
            html_dys = html_re1.xpath('//*[@id="playlist1"]/ul/li/a/text()')  # 判断是否电视剧类型
            # print(html_js_lj)
            if len(html_js_lj) == 0:  # 再获取一次
                re1 = requests.get(url_ys, headers=self.headers, timeout=15)
                html_re1 = etree.HTML(re1.text)
                html_js_lj = html_re1.xpath('//*[@id="playlist1"]/ul/li/a/@href')  # 集数链接
                html_dys = html_re1.xpath('//*[@id="playlist1"]/ul/li/a/text()')  # 判断是否电视剧类型
            # 3. 把集数链接再次请求,得到两个m3u8,进行拼凑成一个真实的m3u8链接
            if len(html_js_lj) == 0:
                mjs = 1
            else:
                mjs = len(html_js_lj)

            if '集' in html_dys[0]:
                self.b1 = 1  # 确定是电视剧
            else:
                self.b1 = 2  # 否则是电影

            print(f'{name}总共:{mjs}集')
            self.text_pad.insert(1.0, f'{name}总共:{mjs}集' + '\n')

            self.name_film = re.findall('<(.*?)>', self.films_name)[0]  # 取出真正的影视名字
            self.name_film = self.name_film.replace(' ', '')  # 把空格去掉
            # 删除临时的ts文件(先清空)
            shutil.rmtree(self.path_var.get() + '\\ts', ignore_errors=True)
            path_video_a = ''
            if self.b1 == 2:
                os.makedirs(self.path_var.get() + '\\电影\\', exist_ok=True)  # 检查目录是否存在,不存在就建立
                path_video = self.path_var.get() + '\\电影\\' + self.name_film + '.mp4'  # 电影目录
            else:
                os.makedirs(self.path_var.get() + '\\电视剧\\' + self.name_film, exist_ok=True)  # 检查目录是否存在,不存在就建立
                path_video = self.path_var.get() + "\\电视剧\\" + self.name_film  # + "\\第%03d集.mp4" % a1  # 生成的mp4文件要放的地方

            t = ThreadPoolExecutor(1)  # 线程池总数这台机器1比较合适,具体以后再调试
            for inda, item in enumerate(html_js_lj):
                # 在这里可以再判断这一集是否存在于指定路径里,存在就不要再下载了!!!
                if self.b1 == 1:
                    path_video_a = path_video + "\\第%03d集.mp4" % int(inda + 1)
                if self.b1 == 2:
                    path_video_a = path_video
                if os.path.exists(path_video_a):
                    print(path_video_a.split('\\')[-1].split('.')[0], ', 已存在, 不再下载')
                    self.text_pad.insert('2.0',
                                         '\n' + path_video_a.split('\\')[-1].split('.')[0] + ', 已存在, 不再下载')
                    path_video_a = ''
                else:
                    print(path_video_a.split('\\')[-1].split('.')[0], ', 正在下载...')
                    self.text_pad.insert('2.0', '\n' + path_video_a.split('\\')[-1].split('.')[0] + ', 正在下载...')
                    os.makedirs(self.path_var.get() + '\\ts\\' + str(inda + 1), exist_ok=True)  # 创建每一集的ts目录
                    t.submit(self.download, url_website, item, inda)  # 使用线程池
                    # download(url_website, item, ind)  # 不使用线程池
                    path_video_a = ''
            t.shutdown()
            time2 = time.time()
            print('总花费时间:' + str(time2 - self.time1)[:-12] + '秒')
            self.text_pad.insert('2.0', '已全下载完, 总花费时间:' + str(time2 - self.time1)[:-12] + '秒' + '\n\n')
            # 在ts信息栏清空告知,更直观知道全部完成了
            self.text_pad_mil.delete('1.0', 'end')
            self.text_pad_mil.insert('3.3', '已全下载完, 总花费时间:' + str(time2 - self.time1)[:-12] + '秒' + '\n')
        else:
            print('请求集数页面错误:', re1.status_code)
            self.text_pad_bot.insert('1.0', '请求集数页面错误:' + str(re1.status_code) + '\n')

    def download(self, url_website, item, ind):
        # lock = threading.Lock()  # 加上线程锁,一般就不会冲突,造成mp4文件写不进磁盘
        # lock.acquire()

        url_js = url_website + item  # 每一集的链接
        re2 = requests.get(url_js, headers=self.headers, timeout=15)

        if re2.status_code == 200:
            if ind == 0:
                ts_url = re.findall('"link_pre":"","url":"(.*?)","url_next":', re2.text)
            else:
                ts_url = re.findall('html","url":"(.*?)","url_next":', re2.text)
            ii = 0
            while len(ts_url) == 0:
                ii += 1
                re2 = requests.get(url_js, headers=self.headers, timeout=15)
                # ts_url = re.findall('index.m3u8","url_next":"(.*?)","from":', re2.text)
                if ind == 0:
                    ts_url = re.findall('"link_pre":"","url":"(.*?)","url_next":', re2.text)
                else:
                    ts_url = re.findall('html","url":"(.*?)","url_next":', re2.text)
                # print(f'第{ind+1}集的第一个m3u8链接重新获取:', ii, '次')

            ts_url = ''.join(ts_url[0])  # 转成真正的字符串
            # 得到第一个m3u8链接
            ts_url = ts_url.replace('\\', '')
            m3u8_text = requests.get(ts_url, self.headers, timeout=15)  # 1分钟取不到数据就抛异常
            m3u8_text_status_code = m3u8_text.status_code  # 赋值,因为后边提示栏要用到
            if m3u8_text_status_code == 200:
                m3u8_text = m3u8_text.text
                m3u8_text = re.sub('#E.*', '', m3u8_text)
                m3u8_text = m3u8_text.split()
                # 得到第二个拼凑完整的有真正ts文件的m3u8链接
                ts_url_1 = ts_url.replace('index.m3u8', '') + m3u8_text[0]
                # print(f'第{ind + 1}集的第二个M3U8链接:', ts_url_1)
                m3u8_text = requests.get(ts_url_1, self.headers, timeout=15).text  # 1分钟取不到数据就抛异常
                m3u8_text = re.sub('#E.*', '', m3u8_text)
                m3u8_text = m3u8_text.split()

                mts = len(m3u8_text)
                print(f'\r第{ind + 1}集ts总个数:', mts)
                # self.text_pad.delete('2.0', 'end')
                self.text_pad_mil.insert('1.0', f'第{ind + 1}集片段总个数:' + str(mts) + '\n')
                # 至此,可以开始下载所有的ts链接到指定地方进行单集的拼凑

                t1 = ThreadPoolExecutor(100)  # 线程池总数为mts个数的1倍,这里是要下载ts的
                # for ind_ts, item_ts in enumerate(m3u8_text):  # m3u8_text是每一集的ts链接
                for ind_ts in range(mts):  # m3u8_text是每一集的ts链接
                    t1.submit(self.download_ts, m3u8_text[ind_ts], ind_ts, ind,
                              mts)  # 线程池:ind是第几集, ind_ts是这一集里的第几个ts, mts是总ts个数
                t1.shutdown()
                # 再次确定下载的ts还欠缺哪些没有下载到,补下载
                self.defect_ts(m3u8_text, ind, mts)
                # 写成一个MP4文件
                self.write_mp4(ind + 1, self.b1, self.name_film,
                               mts)  # ind+1是第几集, b1=1是电视剧=2是电影, c1(self.name_film)是影视名字,
            else:
                print(f'请求第{ind + 1}集第2个m3u8返回错误码:', m3u8_text_status_code)
                self.text_pad_bot.insert('1.0',
                                         f'请求第{ind + 1}集第2个m3u8返回错误码:' + str(m3u8_text_status_code) + '\n')
        else:
            print(f'请求第{ind + 1}集第1个m3u8返回错误码:', re2.status_code)
            self.text_pad_bot.insert('1.0', f'请求第{ind + 1}集第1个m3u8返回错误码:' + str(re2.status_code) + '\n')

        # lock.release()

    # 再次确定下载的ts还欠缺哪些没有下载到,补下载
    def defect_ts(self, m3u8_text, ind, mts):
        # lock = threading.Lock()  # 加上线程锁,一般就不会冲突,造成mp4文件写不进磁盘
        # lock.acquire()

        path_ts = self.path_var.get() + '\\ts\\' + str(ind + 1)
        mts_dir = len(os.listdir(path_ts))  # 实际下载到的ts总数
        if mts - mts_dir != 0:
            t3 = ThreadPoolExecutor(30)  # 开启第三个线程池
            for i in range(mts):
                file_path1 = path_ts + '\\%04d.ts' % i
                if os.path.exists(file_path1) is False:
                    print(f'\r第{ind + 1}集片段差:', mts - mts_dir, '个,正在补下载第:', file_path1.split('\\')[-1])
                    self.text_pad_mil.delete('1.0', '1.end')
                    self.text_pad_mil.insert('1.0',
                                             f'第{ind + 1}集差:' + str(mts - mts_dir).strip() + '个,正在补下载第:' +
                                             file_path1.split('\\')[-1])
                    t3.submit(self.download_ts, m3u8_text[i], i, ind, mts)
                    # download_ts(m3u8_text[i], i, ind, mts)
            t3.shutdown()

        # lock.release()

    def download_ts(self, item_ts, ind_ts, ind, mts):  # item_ts第ind_ts个ts的url,  ind_ts第几个ts, ind第几集, mts总共的ts个数
        # lock = threading.Lock()  # 加上线程锁,一般就不会冲突,造成mp4文件写不进磁盘
        # lock.acquire()
        # if self.line == 1:
        # 每次给个随机头,线路二可能不行
        self.headers = {'User-Agent': UserAgent().random}
        response = requests.get(item_ts, headers=self.headers, timeout=15)
        path_ts = self.path_var.get() + '\\ts\\' + str(ind + 1) + '\\{:04}.ts'.format(ind_ts)
        if response.status_code != 404:
            try:
                with open(path_ts, 'wb') as f:  # 直接用index命名
                    f.write(response.content)
            except IOError as e:
                print(f'Write failed: {e}')
                self.text_pad_bot.insert('1.0', f'Write failed: {e}' + '\n')
        else:
            print('请求第' + str(ind + 1) + '集的第' + str(ind_ts) + '个ts时错误!')
            self.text_pad_bot.insert('1.0', '请求第' + str(ind + 1) + '集的第' + str(ind_ts) + '个ts时错误!' + '\n')

        if os.path.exists(path_ts) is False:
            print('第' + str(ind + 1) + '集的' + path_ts.split('\\')[-1] + '下载失败')
            self.text_pad_bot.insert('1.0', '第' + str(ind + 1) + '集的' + path_ts.split('\\')[-1] + '下载失败' + '\n')
        # print('\r第'+str(ind+1)+'集:' + str(ind_ts + 1) + '/' + str(mts))
        self.text_mid_pad.insert(1.0, '第' + str(ind + 1) + '集:' + str(ind_ts + 1) + '/' + str(mts) + '\n')

        # lock.release()

    # 写成一个MP4文件
    def write_mp4(self, a1, b1, c1, mts):  # a1是第几集  b1=1电视剧=2电影, c1是影视名字, mts应有ts总数
        # lock = threading.Lock()  # 加上线程锁,一般就不会冲突,造成mp4文件写不进磁盘
        # lock.acquire()

        path_ts = self.path_var.get() + "\\ts\\" + str(a1)  # 临时存放ts文件
        mts_dir = len(os.listdir(path_ts))  # 实际下载到的ts总数
        path_video = ""
        print('正在写入:第' + str(a1) + '集...')
        self.text_pad_mil.delete('1.0', '1.end')
        self.text_pad_mil.insert('1.0', '正在写入:第' + str(a1) + '集...')
        if b1 == 1:
            path_video = self.path_var.get() + "\\电视剧\\" + c1 + "\\第%03d集.mp4" % a1  # 生成的mp4文件要放的地方
        if b1 == 2:
            path_video = self.path_var.get() + '\\电影\\' + c1 + '.mp4'  # 电影目录
        # 将ts目录下的所有文件保存到file_list列表中
        file_list = sorted(os.listdir(path_ts))
        # 将file_list列表写成固定格式: file_0000.ts 这样的格式保存到file_list.txt中
        # with open(path_ts + "\\file_list.txt", "w+") as f:
        #     for file in file_list:
        #         f.write("file '{}'\n".format(file))
        # ffmpeg_bin_dic = 'D:\\ffmpeg\\bin\\ffmpeg -f concat -safe 0 -y -i '
        # ffmpeg_bin_dic = 'D:\\ffmpeg\\ffmpeg-2024-06-13-git-0060a368b1-essentials_build\\bin\\ffmpeg -f concat -safe 0 -y -i '
        # 写成指定的一个mp4文件
        # os.system(ffmpeg_bin_dic + path_ts + '\\file_list.txt' + ' -c ' + ' copy ' + path_video + r'> nul 2> nul')
        os.system(r'copy /b ' + path_ts + '\\*.ts ' + path_video + r'> nul 2> nul')
        # 删除临时的ts文件
        # os.system(r'@echo y | del ' + path_ts + r'\*.* > nul 2> nul')  # > nul 2> nul表示不在控制台输出结果提示,并且会在最后自动按Y确认删除
        # shutil.rmtree(path_ts, ignore_errors=True)  # 这句比上局好用理解
        if os.path.exists(path_video):  # 检测MP4文件是否生产得到
            if mts - mts_dir != 0:
                print('第', a1, '集已完成, 片段差:', mts - mts_dir, '个')
                # self.text_pad.delete('2.0', '2.14')
                self.text_pad.insert('2.0', '第' + str(a1) + '集已完成, 片段差:' + str(mts - mts_dir) + '个\n')
                self.text_pad_mil.delete('1.0', '1.end')
                self.text_pad_mil.insert('1.0', '第' + str(a1) + '集已完成, 片段差:' + str(mts - mts_dir) + '个')
            else:
                print('第', a1, '集已完成, 片段完整')
                # self.text_pad.delete('2.0', '2.14')
                self.text_pad.insert('2.0', '第' + str(a1) + '集已完成, 片段完整' + '\n')
                self.text_pad_mil.delete('1.0', '1.end')
                self.text_pad_mil.insert('1.0', '第' + str(a1) + '集已完成, 片段完整')
        else:
            print('第', a1, '集写入失败')
            self.text_pad_bot.insert('1.0', '第' + str(a1) + '集写入失败' + '\n')

        # lock.release()


class Two:
    def __init__(self):
        self.shared = share.SharedData()
        # self.film_type = self.shared.get('film_type_sure')  # 都等于1:影视
        self.line = self.shared.get('line_sure')
        self.name = self.shared.get('name')
        self.frame_2 = self.shared.get('frame_2')
        self.search_frame = self.shared.get('search_frame')
        # self.v = self.shared.get('v')
        self.button2 = self.shared.get('button2')
        self.text_pad = self.shared.get('text_pad')
        self.text_mid_pad = self.shared.get('text_mid_pad')
        self.path_var = self.shared.get('path_var')
        self.left_frame = self.shared.get('left_frame')
        self.text_pad_mil = self.shared.get('text_pad_mil')  # 中间之中间
        self.text_pad_bot = self.shared.get('text_pad_bot')  # 中间之下部
        self.v = IntVar()  # 用于影片列表
        self.headers = {
            'Referer': 'https://www.sjzamys.com/',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36',
            'Cookie': '_ga=GA1.1.1749885607.1719486553; PHPSESSID=2if4415d9i91v6nfcqhalrn768; recente=%5B%7B%22vod_name%22%3A%22%E5%A2%A8%E9%9B%A8%E4%BA%91%E9%97%B4%22%2C%22vod_url%22%3A%22https%3A%2F%2Fwww.sjzamys.com%2Fkp%2F101630%2F1-1.html%22%2C%22vod_part%22%3A%22%E7%AC%AC01%E9%9B%86%22%7D%2C%7B%22vod_name%22%3A%22%E5%A4%A7%E6%98%8E%E7%8E%8B%E6%9C%9D1566%22%2C%22vod_url%22%3A%22https%3A%2F%2Fwww.sjzamys.com%2Fkp%2F12283%2F2-1.html%22%2C%22vod_part%22%3A%22%E7%AC%AC01%E9%9B%86%22%7D%2C%7B%22vod_name%22%3A%22%E5%A4%A9%E9%81%93%22%2C%22vod_url%22%3A%22https%3A%2F%2Fwww.sjzamys.com%2Fkp%2F40691%2F2-1.html%22%2C%22vod_part%22%3A%22%E7%AC%AC01%E9%9B%86%22%7D%5D; _ga_0SX2ZM5WDV=GS1.1.1719748768.9.0.1719748776.0.0.0',
            # 'Sec-Ch-Ua': '"Not/A)Brand";v="8", "Chromium";v="126", "Google Chrome";v="126"'
        }

        self.line_url = 'https://www.sjzamys.com'  # (这个是免费影院, https://www.cqhpjn.com'这个是全网集,需要验证,未完成)
        self.sun_url = f'{self.line_url}/vodsearch/-------------.html?wd={self.name}'  # 拼成完整的可以搜索的链接

    def get_film_name(self):  # sun_url是上级传来的可下载的单片链接
        url = self.sun_url  # 传来的格式: self.sun_url = f'{self.line_url}/vodsearch/-------------.html?wd={name}'
        # 1. 先请求影视网站主页
        resp = requests.get(url, headers=self.headers, timeout=15)
        films = []
        html_primary = []
        html_name = []
        if resp.status_code == 200:
            html = etree.HTML(resp.text)
            # html_primary获取影视名字的短链接列表:['/voddetail/12299.html',...]
            html_primary = html.xpath('/html/body/div[1]/div/div[1]/div/div/div[2]/ul/li/div[1]/a/@href')  # 这里与one改动不一样了
            # html_name,得到列表:['大明王朝1566',...]
            html_name = html.xpath('/html/body/div[1]/div/div[1]/div/div/div[2]/ul/li/div[1]/a/@title')  # 这里与one改动不一样了
            # html_nf2,得到列表:['2007',...]
            html_nf2 = html.xpath('/html/body/div[1]/div/div[1]/div/div/div[2]/ul/li/div[2]/p[3]/span[4]/text()')  # 这里与one改动不一样了

            if len(html_primary) == 0:  # 再获取一遍
                resp = requests.get(url, headers=self.headers, timeout=15)
                html = etree.HTML(resp.text)
                # html_primary获取影视名字的短链接列表:['/voddetail/12299.html',...]
                html_primary = html.xpath('/html/body/div[1]/div/div[1]/div/div/div[2]/ul/li/div[1]/a/@href')  # 这里与one改动不一样了
                # html_name,得到列表:['大明王朝1566',...]
                html_name = html.xpath('/html/body/div[1]/div/div[1]/div/div/div[2]/ul/li/div[1]/a/@title')  # 这里与one改动不一样了
                # html_nf2,得到列表:['2007',...]
                html_nf2 = html.xpath('/html/body/div[1]/div/div[1]/div/div/div[2]/ul/li/div[2]/p[3]/span[4]/text()')  # 这里与one改动不一样了

            if len(html_primary) != 0:
                for ind, name in enumerate(html_name):
                    html_name[ind] = '<' + html_name[ind] + '>' + html_nf2[ind] + '年'
                for ind, name in enumerate(html_name):
                    name = (name, ind)
                    films.append(name)

            # 销毁self.frame_2所有子控件
            for widget in self.frame_2.winfo_children():
                widget.destroy()

            if films:  # self.films
                for film, num in films:
                    self.b = Radiobutton(self.frame_2, text=film, variable=self.v, value=num, font=('思源宋体', 13),
                                         width=20, anchor="w")
                    self.b.pack()
                self.button1 = Button(self.frame_2, text='开始下载', command=self.get_js, font=('方正兰亭黑简体', 15))
                self.button1.pack(anchor=CENTER, pady=2)

            else:
                Label(self.frame_2, text='没找到,或再试一次!', font=('思源宋体', 18), fg='red').pack()
            self.frame_2.pack(anchor="w", padx=0, pady=5)

            """
            返回的格式为:
            films: [('<大明王朝1566>2007年', 0)] 或
                   [('<剑王朝之孤山剑藏>2020年', 0), ('<剑王朝之九境长生>2020年', 1), ('<古驰家族>2021年', 2)] 
            html_primary: ['/voddetail/12299.html'] 或
                          ['/voddetail/60109.html', '/voddetail/60107.html', '/voddetail/59201.html']  
            html_name: ['<大明王朝1566>2007年'] 或
                       ['<剑王朝之孤山剑藏>2020年', '<剑王朝之九境长生>2020年', '<古驰家族>2021年']

            films, 这个好像不用返回,没用            
            """
        self.html_primary = html_primary
        self.h_name = html_name
        # return html_primary, html_name

    def get_js(self):  # 获取集数
        self.button1.config(state=DISABLED)
        self.button2.config(state=DISABLED)
        thread = threading.Thread(target=self.worker)
        thread.start()  # 这里单独给主界面一个线程,避免界面在后边多线程池使用时卡住未响应

    def worker(self):
        self.va = self.v.get()
        self.films_name = self.h_name[self.va]
        self.get_film_js(self.va, self.html_primary, self.line_url, self.films_name)
        self.button1.config(state=ACTIVE)
        self.button2.config(state=ACTIVE)

    def get_film_js(self, va, html_primary, url_website, name):  # 获取集数
        # 先清空上次信息栏提示内容
        self.text_pad.delete('0.0', 'end')
        self.text_mid_pad.delete('0.0', 'end')
        self.text_pad_mil.delete('0.0', 'end')
        self.text_pad_bot.delete('0.0', 'end')

        self.time1 = time.time()
        # print(va, html_primary)
        # print('要获取的影视链接是:',html_primary[va])
        html_primary = ''.join(html_primary[va])  # 转成真正的字符串
        url_ys = url_website + html_primary  # url_website是影视网站最前链接,可能有多个,取第[va]个
        # print('得到的子集链接:', url_ys)

        # 2. 把选择好的影视名链接,再次请求,得到集数链接
        re1 = requests.get(url_ys, headers=self.headers, timeout=15)
        if re1.status_code == 200:
            # 获取这部影视剧的各集链接
            html_re1 = etree.HTML(re1.text)
            # html_js_lj = html_re1.xpath('//*[@id="playlist1"]/ul/li/a/@href')  # 集数链接
            # 这里与one改动不一样了
            html_js_lj = html_re1.xpath('/html/body/div[1]/div/div[1]/div[2]/div/div[2]/ul/li/a/@href')  # 集数链接:/kp/12283/2-1.html
            # html_dys = html_re1.xpath('//*[@id="playlist1"]/ul/li/a/text()')  # 判断是否电视剧类型
            # 这里与one改动不一样了
            html_dys = html_re1.xpath('/html/body/div[1]/div/div[1]/div[2]/div/div[2]/ul/li[1]/a/text()')  # 判断是否电视剧类型
            # print(html_js_lj)
            if len(html_js_lj) == 0:  # 再获取一次
                re1 = requests.get(url_ys, headers=self.headers, timeout=15)
                html_re1 = etree.HTML(re1.text)
                # 这里与one改动不一样了
                html_js_lj = html_re1.xpath('/html/body/div[1]/div/div[1]/div[2]/div/div[2]/ul/li/a/@href')  # 集数链接
                # 这里与one改动不一样了
                html_dys = html_re1.xpath('/html/body/div[1]/div/div[1]/div[2]/div/div[2]/ul/li[1]/a/text()/text()')  # 判断是否电视剧类型
            # 3. 把集数链接再次请求,得到两个m3u8,进行拼凑成一个真实的m3u8链接
            if len(html_js_lj) == 0:
                mjs = 1
            else:
                mjs = len(html_js_lj)

            if '集' in html_dys[0]:
                self.b1 = 1  # 确定是电视剧
            else:
                self.b1 = 2  # 否则是电影

            print(f'{name}总共:{mjs}集')
            self.text_pad.insert(1.0, f'{name}总共:{mjs}集' + '\n')

            self.name_film = re.findall('<(.*?)>', self.films_name)[0]  # 取出真正的影视名字
            self.name_film = self.name_film.replace(' ', '')  # 把空格去掉
            # 删除临时的ts文件(先清空)
            shutil.rmtree(self.path_var.get() + '\\ts', ignore_errors=True)
            path_video_a = ''
            if self.b1 == 2:
                os.makedirs(self.path_var.get() + '\\电影\\', exist_ok=True)  # 检查目录是否存在,不存在就建立
                path_video = self.path_var.get() + '\\电影\\' + self.name_film + '.mp4'  # 电影目录
            else:
                os.makedirs(self.path_var.get() + '\\电视剧\\' + self.name_film, exist_ok=True)  # 检查目录是否存在,不存在就建立
                path_video = self.path_var.get() + "\\电视剧\\" + self.name_film  # + "\\第%03d集.mp4" % a1  # 生成的mp4文件要放的地方

            t = ThreadPoolExecutor(1)  # 线程池总数这台机器1比较合适,具体以后再调试
            for inda, item in enumerate(html_js_lj):
                # 在这里可以再判断这一集是否存在于指定路径里,存在就不要再下载了!!!
                if self.b1 == 1:
                    path_video_a = path_video + "\\第%03d集.mp4" % int(inda + 1)
                if self.b1 == 2:
                    path_video_a = path_video
                if os.path.exists(path_video_a):
                    print(path_video_a.split('\\')[-1].split('.')[0], ', 已存在, 不再下载')
                    self.text_pad.insert('2.0',
                                         '\n' + path_video_a.split('\\')[-1].split('.')[0] + ', 已存在, 不再下载')
                    path_video_a = ''
                else:
                    print(path_video_a.split('\\')[-1].split('.')[0], ', 正在下载...')
                    self.text_pad.insert('2.0', '\n' + path_video_a.split('\\')[-1].split('.')[0] + ', 正在下载...')
                    os.makedirs(self.path_var.get() + '\\ts\\' + str(inda + 1), exist_ok=True)  # 创建每一集的ts目录
                    t.submit(self.download, url_website, item, inda)  # 使用线程池
                    # download(url_website, item, ind)  # 不使用线程池
                    path_video_a = ''
            t.shutdown()
            time2 = time.time()
            print('总花费时间:' + str(time2 - self.time1)[:-12] + '秒')
            self.text_pad.insert('2.0', '已全下载完, 总花费时间:' + str(time2 - self.time1)[:-12] + '秒' + '\n\n')
            # 在ts信息栏清空告知,更直观知道全部完成了
            self.text_pad_mil.delete('1.0', 'end')
            self.text_pad_mil.insert('3.3', '已全下载完, 总花费时间:' + str(time2 - self.time1)[:-12] + '秒' + '\n')
        else:
            print('请求集数页面错误:', re1.status_code)
            self.text_pad_bot.insert('1.0', '请求集数页面错误:' + str(re1.status_code) + '\n')

    def download(self, url_website, item, ind):
        # lock = threading.Lock()  # 加上线程锁,一般就不会冲突,造成mp4文件写不进磁盘
        # lock.acquire()

        url_js = url_website + item  # 每一集的链接
        re2 = requests.get(url_js, headers=self.headers, timeout=15)

        if re2.status_code == 200:
            ts_url = re.findall('"url":"(.*?)","url_next":', re2.text)  # 这里与One有改动过
            ii = 0
            while len(ts_url) == 0 or ii >= 3:  # 若3次都获取不到就算了,返回空的ts_url
                ii += 1
                re2 = requests.get(url_js, headers=self.headers, timeout=15)
                ts_url = re.findall('"url":"(.*?)","url_next":', re2.text)  # 这里与One有改动过
            ts_url = ''.join(ts_url[0])  # 转成真正的字符串
            # 得到第一个m3u8链接
            ts_url = ts_url.replace('\\', '')
            # print(ts_url)
            m3u8_text = requests.get(ts_url, self.headers, timeout=15)  # 1分钟取不到数据就抛异常
            m3u8_text_status_code = m3u8_text.status_code  # 赋值,因为后边提示栏要用到
            if m3u8_text_status_code == 200:
                m3u8_text = m3u8_text.text
                m3u8_text = re.sub('#E.*', '', m3u8_text)
                m3u8_text = m3u8_text.split()
                # 得到第二个拼凑完整的有真正ts文件的m3u8链接
                ts_url_1 = ts_url.replace('index.m3u8', '') + m3u8_text[0]
                # print(f'第{ind + 1}集的第二个M3U8链接:', ts_url_1)
                m3u8_text = requests.get(ts_url_1, self.headers, timeout=15).text  # 1分钟取不到数据就抛异常
                m3u8_text = re.sub('#E.*', '', m3u8_text)
                m3u8_text = m3u8_text.split()

                mts = len(m3u8_text)
                print(f'\r第{ind + 1}集ts总个数:', mts)
                # self.text_pad.delete('2.0', 'end')
                self.text_pad_mil.insert('1.0', f'第{ind + 1}集片段总个数:' + str(mts) + '\n')
                # 至此,可以开始下载所有的ts链接到指定地方进行单集的拼凑

                t1 = ThreadPoolExecutor(100)  # 线程池总数为mts个数的1倍,这里是要下载ts的
                # for ind_ts, item_ts in enumerate(m3u8_text):  # m3u8_text是每一集的ts链接
                for ind_ts in range(mts):  # m3u8_text是每一集的ts链接
                    t1.submit(self.download_ts, m3u8_text[ind_ts], ind_ts, ind,
                              mts)  # 线程池:ind是第几集, ind_ts是这一集里的第几个ts, mts是总ts个数
                t1.shutdown()
                # 再次确定下载的ts还欠缺哪些没有下载到,补下载
                self.defect_ts(m3u8_text, ind, mts)
                # 写成一个MP4文件
                self.write_mp4(ind + 1, self.b1, self.name_film,
                               mts)  # ind+1是第几集, b1=1是电视剧=2是电影, c1(self.name_film)是影视名字,
            else:
                print(f'请求第{ind + 1}集第2个m3u8返回错误码:', m3u8_text_status_code)
                self.text_pad_bot.insert('1.0',
                                         f'请求第{ind + 1}集第2个m3u8返回错误码:' + str(m3u8_text_status_code) + '\n')
        else:
            print(f'请求第{ind + 1}集第1个m3u8返回错误码:', re2.status_code)
            self.text_pad_bot.insert('1.0', f'请求第{ind + 1}集第1个m3u8返回错误码:' + str(re2.status_code) + '\n')

        # lock.release()

    # 再次确定下载的ts还欠缺哪些没有下载到,补下载
    def defect_ts(self, m3u8_text, ind, mts):
        # lock = threading.Lock()  # 加上线程锁,一般就不会冲突,造成mp4文件写不进磁盘
        # lock.acquire()

        path_ts = self.path_var.get() + '\\ts\\' + str(ind + 1)
        mts_dir = len(os.listdir(path_ts))  # 实际下载到的ts总数
        if mts - mts_dir != 0:
            t3 = ThreadPoolExecutor(30)  # 开启第三个线程池
            for i in range(mts):
                file_path1 = path_ts + '\\%04d.ts' % i
                if os.path.exists(file_path1) is False:
                    print(f'\r第{ind + 1}集片段差:', mts - mts_dir, '个,正在补下载第:', file_path1.split('\\')[-1])
                    self.text_pad_mil.delete('1.0', '1.end')
                    self.text_pad_mil.insert('1.0',
                                             f'第{ind + 1}集差:' + str(mts - mts_dir).strip() + '个,正在补下载第:' +
                                             file_path1.split('\\')[-1])
                    t3.submit(self.download_ts, m3u8_text[i], i, ind, mts)
                    # download_ts(m3u8_text[i], i, ind, mts)
            t3.shutdown()

        # lock.release()

    def download_ts(self, item_ts, ind_ts, ind, mts):  # item_ts第ind_ts个ts的url,  ind_ts第几个ts, ind第几集, mts总共的ts个数
        # lock = threading.Lock()  # 加上线程锁,一般就不会冲突,造成mp4文件写不进磁盘
        # lock.acquire()
        # if self.line == 1:
        # 每次给个随机头,线路二可能不行
        self.headers = {'User-Agent': UserAgent().random}
        response = requests.get(item_ts, headers=self.headers, timeout=15)
        path_ts = self.path_var.get() + '\\ts\\' + str(ind + 1) + '\\{:04}.ts'.format(ind_ts)
        if response.status_code != 404:
            try:
                with open(path_ts, 'wb') as f:  # 直接用index命名
                    f.write(response.content)
            except IOError as e:
                print(f'Write failed: {e}')
                self.text_pad_bot.insert('1.0', f'Write failed: {e}' + '\n')
        else:
            print('请求第' + str(ind + 1) + '集的第' + str(ind_ts) + '个ts时错误!')
            self.text_pad_bot.insert('1.0', '请求第' + str(ind + 1) + '集的第' + str(ind_ts) + '个ts时错误!' + '\n')

        if os.path.exists(path_ts) is False:
            print('第' + str(ind + 1) + '集的' + path_ts.split('\\')[-1] + '下载失败')
            self.text_pad_bot.insert('1.0', '第' + str(ind + 1) + '集的' + path_ts.split('\\')[-1] + '下载失败' + '\n')
        # print('\r第'+str(ind+1)+'集:' + str(ind_ts + 1) + '/' + str(mts))
        self.text_mid_pad.insert(1.0, '第' + str(ind + 1) + '集:' + str(ind_ts + 1) + '/' + str(mts) + '\n')

        # lock.release()

    # 写成一个MP4文件
    def write_mp4(self, a1, b1, c1, mts):  # a1是第几集  b1=1电视剧=2电影, c1是影视名字, mts应有ts总数
        # lock = threading.Lock()  # 加上线程锁,一般就不会冲突,造成mp4文件写不进磁盘
        # lock.acquire()

        path_ts = self.path_var.get() + "\\ts\\" + str(a1)  # 临时存放ts文件
        mts_dir = len(os.listdir(path_ts))  # 实际下载到的ts总数
        path_video = ""
        print('正在写入:第' + str(a1) + '集...')
        self.text_pad_mil.delete('1.0', '1.end')
        self.text_pad_mil.insert('1.0', '正在写入:第' + str(a1) + '集...')
        if b1 == 1:
            path_video = self.path_var.get() + "\\电视剧\\" + c1 + "\\第%03d集.mp4" % a1  # 生成的mp4文件要放的地方
        if b1 == 2:
            path_video = self.path_var.get() + '\\电影\\' + c1 + '.mp4'  # 电影目录
        # 将ts目录下的所有文件保存到file_list列表中
        file_list = sorted(os.listdir(path_ts))
        # 将file_list列表写成固定格式: file_0000.ts 这样的格式保存到file_list.txt中
        # with open(path_ts + "\\file_list.txt", "w+") as f:
        #     for file in file_list:
        #         f.write("file '{}'\n".format(file))
        # ffmpeg_bin_dic = 'D:\\ffmpeg\\bin\\ffmpeg -f concat -safe 0 -y -i '
        # ffmpeg_bin_dic = 'D:\\ffmpeg\\ffmpeg-2024-06-13-git-0060a368b1-essentials_build\\bin\\ffmpeg -f concat -safe 0 -y -i '
        # 写成指定的一个mp4文件
        # os.system(ffmpeg_bin_dic + path_ts + '\\file_list.txt' + ' -c ' + ' copy ' + path_video + r'> nul 2> nul')
        os.system(r'copy /b ' + path_ts + '\\*.ts ' + path_video + r'> nul 2> nul')
        # 删除临时的ts文件
        # os.system(r'@echo y | del ' + path_ts + r'\*.* > nul 2> nul')  # > nul 2> nul表示不在控制台输出结果提示,并且会在最后自动按Y确认删除
        # shutil.rmtree(path_ts, ignore_errors=True)  # 这句比上局好用理解
        if os.path.exists(path_video):  # 检测MP4文件是否生产得到
            if mts - mts_dir != 0:
                print('第', a1, '集已完成, 片段差:', mts - mts_dir, '个')
                # self.text_pad.delete('2.0', '2.14')
                self.text_pad.insert('2.0', '第' + str(a1) + '集已完成, 片段差:' + str(mts - mts_dir) + '个\n')
                self.text_pad_mil.delete('1.0', '1.end')
                self.text_pad_mil.insert('1.0', '第' + str(a1) + '集已完成, 片段差:' + str(mts - mts_dir) + '个')
            else:
                print('第', a1, '集已完成, 片段完整')
                # self.text_pad.delete('2.0', '2.14')
                self.text_pad.insert('2.0', '第' + str(a1) + '集已完成, 片段完整' + '\n')
                self.text_pad_mil.delete('1.0', '1.end')
                self.text_pad_mil.insert('1.0', '第' + str(a1) + '集已完成, 片段完整')
        else:
            print('第', a1, '集写入失败')
            self.text_pad_bot.insert('1.0', '第' + str(a1) + '集写入失败' + '\n')

        # lock.release()


class Three:
    def __init__(self):
        self.shared = share.SharedData()
        # self.film_type = self.shared.get('film_type_sure')  # 都等于1:影视
        self.line = self.shared.get('line_sure')
        self.name = self.shared.get('name')
        self.frame_2 = self.shared.get('frame_2')
        self.search_frame = self.shared.get('search_frame')
        # self.v = self.shared.get('v')
        self.button2 = self.shared.get('button2')
        self.text_pad = self.shared.get('text_pad')
        self.text_mid_pad = self.shared.get('text_mid_pad')
        self.path_var = self.shared.get('path_var')
        self.left_frame = self.shared.get('left_frame')
        self.text_pad_mil = self.shared.get('text_pad_mil')  # 中间之中间
        self.text_pad_bot = self.shared.get('text_pad_bot')  # 中间之下部
        self.label_2 = self.shared.get('label_2')  # 中间之下部
        self.v = IntVar()  # 用于影片列表
        self.headers = {
            # 'Referer': 'https://www.sqacfs.com/',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36',
            # 'Cookie': 'Hm_lvt_c7df3382da979c41bef005716322874e=1719486878,1719745517; PHPSESSID=k18bqv9q7dkun5i0f3trqgl8m0; recente=%5B%7B%22vod_name%22%3A%22%E5%A2%A8%E9%9B%A8%E4%BA%91%E9%97%B4%22%2C%22vod_url%22%3A%22https%3A%2F%2Fwww.sqacfs.com%2Fplay%2Fp6E33i%2F1%2F1.html%22%2C%22vod_part%22%3A%22%E7%AC%AC01%E9%9B%86%22%7D%5D; Hm_lpvt_c7df3382da979c41bef005716322874e=1719748239'
        }

        self.line_url = 'https://www.sqacfs.com'  # (这个是极速影院)
        self.sun_url = f'{self.line_url}/search/-------------.html?wd={self.name}'  # 拼成完整的可以搜索的链接

    def get_film_name(self):
        url = self.sun_url
        # 1. 先请求影视网站主页+搜索内容
        resp = requests.get(url, headers=self.headers, timeout=15)
        films = []
        html_primary = []
        html_name = []
        if resp.status_code == 200:
            html = etree.HTML(resp.text)
            # html_primary获取影视名字的短链接列表:['/voddetail/12299.html',...]
            html_primary = html.xpath('/html/body/div[1]/div/div/div[2]/ul/li/div/a/@href')  # 这里与one改动不一样了
            # html_name,得到列表:['大明王朝1566',...]
            html_name = html.xpath('/html/body/div[1]/div/div/div[2]/ul/li/div/a/@title')  # 这里与one改动不一样了
            # html_nf2,得到列表:["动作片", "国产剧", "国产剧"...]
            html_nf2 = html.xpath('/html/body/div[1]/div/div/div[2]/ul/li/div/a/span[2]/b/text()')  # 这里与one改动不一样了
            if len(html_primary) == 0:  # 再获取一遍
                resp = requests.get(url, headers=self.headers, timeout=15)
                html = etree.HTML(resp.text)
                # html_primary获取影视名字的短链接列表:['/voddetail/12299.html',...]
                html_primary = html.xpath('/html/body/div[1]/div/div/div[2]/ul/li/div/a/@href')  # 这里与one改动不一样了
                # html_name,得到列表:['大明王朝1566',...]
                html_name = html.xpath('/html/body/div[1]/div/div/div[2]/ul/li/div/a/@title')  # 这里与one改动不一样了
                # html_nf2,得到列表:['2007',...]
                html_nf2 = html.xpath('/html/body/div[1]/div/div/div[2]/ul/li/div/a/span[2]/b/text()')  # 这里与one改动不一样了

            if len(html_primary) != 0:
                for ind, name in enumerate(html_name):
                    html_name[ind] = '<' + html_name[ind] + '>' + html_nf2[ind]  # + '年' # 这里与one改动不一样了
                for ind, name in enumerate(html_name):
                    name = (name, ind)
                    films.append(name)

            # 销毁self.frame_2所有子控件
            for widget in self.frame_2.winfo_children():
                widget.destroy()

            if films:  # self.films
                for film, num in films:
                    self.b = Radiobutton(self.frame_2, text=film, variable=self.v, value=num, font=('思源宋体', 13),
                                         width=20, anchor="w")
                    self.b.pack()
                self.button1 = Button(self.frame_2, text='开始下载', command=self.get_js, font=('方正兰亭黑简体', 15))
                self.button1.pack(anchor=CENTER, pady=2)
            else:
                Label(self.frame_2, text='没找到,或再试一次!', font=('思源宋体', 18), fg='red').pack()
            self.frame_2.pack(anchor="w", padx=0, pady=5)

            """
            返回的格式为:
            films: [('<大明王朝1566>2007年', 0)] 或
                   [('<剑王朝之孤山剑藏>2020年', 0), ('<剑王朝之九境长生>2020年', 1), ('<古驰家族>2021年', 2)] 
            html_primary: ['/voddetail/12299.html'] 或
                          ['/voddetail/60109.html', '/voddetail/60107.html', '/voddetail/59201.html']  
            html_name: ['<大明王朝1566>2007年'] 或
                       ['<剑王朝之孤山剑藏>2020年', '<剑王朝之九境长生>2020年', '<古驰家族>2021年']

            films, 这个好像不用返回,没用            
            """
        self.html_primary = html_primary
        self.h_name = html_name
        # return html_primary, html_name


    def get_js(self):  # 获取集数
        self.button1.config(state=DISABLED)
        self.button2.config(state=DISABLED)
        # self.worker()
        thread = threading.Thread(target=self.worker)
        thread.start()  # 这里单独给主界面一个线程,避免界面在后边多线程池使用时卡住未响应

    def worker(self):
        self.va = self.v.get()
        self.films_name = self.h_name[self.va]
        self.get_film_js(self.va, self.html_primary, self.line_url, self.films_name)
        self.button1.config(state=ACTIVE)
        self.button2.config(state=ACTIVE)

    def get_film_js(self, va, html_primary, url_website, name):  # 获取集数
        # 先清空上次信息栏提示内容
        self.text_pad.delete('0.0', 'end')
        self.text_mid_pad.delete('0.0', 'end')
        self.text_pad_mil.delete('0.0', 'end')
        self.text_pad_bot.delete('0.0', 'end')

        self.time1 = time.time()
        # print(va, html_primary)
        # print('要获取的影视链接是:',html_primary[va])
        html_primary = ''.join(html_primary[va])  # 转成真正的字符串
        url_ys = url_website + html_primary  # url_website是影视网站最前链接,可能有多个,取第[va]个

        print('得到的子集链接:', url_ys)

        # 2. 把选择好的影视名链接,再次请求,得到集数链接
        re1 = requests.get(url_ys, headers=self.headers, timeout=15)
        if re1.status_code == 200:
            print(re1.text)
            # 获取这部影视剧的各集链接
            html_re1 = etree.HTML(re1.text)
            # 先找出播放链接是放在playlist1,还是playlist2
            playlist = re.findall(r'<div id="(.*?)" class="tab-pane fade in', re1.text)[0]
            print(playlist)
            # 这里与one改动不一样了
            html_js_lj = html_re1.xpath(f'//*[@id="{playlist}"]/ul/li/a/@href')  # 集数链接:/kp/12283/2-1.html
            # //*[@id="play-box"]/div[1]/div[2]/div/ul/li[1]/a
            # //*[@id="playlist1"]/ul/li/a  //*[@id="playlist1"]/ul/li[1]/a //*[@id="playlist2"]/ul/li[1]/a
            # 这里与one改动不一样了
            html_dys = html_re1.xpath(f'//*[@id="{playlist}"]/ul/li/a/text()')  # 判断是否电视剧类型
            # print('得到的集数链接:', html_js_lj)
            if len(html_js_lj) == 0:  # 再获取一次
                re1 = requests.get(url_ys, headers=self.headers, timeout=15)
                html_re1 = etree.HTML(re1.text)
                # 这里与one改动不一样了
                html_js_lj = html_re1.xpath(f'//*[@id="{playlist}"]/ul/li/a/@href')  # 集数链接
                # 这里与one改动不一样了
                html_dys = html_re1.xpath(f'//*[@id="{playlist}"]/ul/li/a/text()')  # 判断是否电视剧类型
            # 3. 把集数链接再次请求,得到两个m3u8,进行拼凑成一个真实的m3u8链接
            if len(html_js_lj) == 0:
                mjs = 1
            else:
                mjs = len(html_js_lj)

            if '集' in html_dys[0]:
                self.b1 = 1  # 确定是电视剧
            else:
                self.b1 = 2  # 否则是电影

            print(f'{name}总共:{mjs}集')
            self.text_pad.insert(1.0, f'{name}总共:{mjs}集' + '\n')

            self.name_film = re.findall('<(.*?)>', self.films_name)[0]  # 取出真正的影视名字
            self.name_film = self.name_film.replace(' ', '')  # 把空格去掉
            # 删除临时的ts文件(先清空)
            shutil.rmtree(self.path_var.get() + '\\ts', ignore_errors=True)
            path_video_a = ''
            if self.b1 == 2:
                os.makedirs(self.path_var.get() + '\\电影\\', exist_ok=True)  # 检查目录是否存在,不存在就建立
                path_video = self.path_var.get() + '\\电影\\' + self.name_film + '.mp4'  # 电影目录
            else:
                os.makedirs(self.path_var.get() + '\\电视剧\\' + self.name_film, exist_ok=True)  # 检查目录是否存在,不存在就建立
                path_video = self.path_var.get() + "\\电视剧\\" + self.name_film  # + "\\第%03d集.mp4" % a1  # 生成的mp4文件要放的地方

            t = ThreadPoolExecutor(1)  # 线程池总数这台机器1比较合适,具体以后再调试
            for inda, item in enumerate(html_js_lj):
                # 在这里可以再判断这一集是否存在于指定路径里,存在就不要再下载了!!!
                if self.b1 == 1:
                    path_video_a = path_video + "\\第%03d集.mp4" % int(inda + 1)
                if self.b1 == 2:
                    path_video_a = path_video
                if os.path.exists(path_video_a):
                    print(path_video_a.split('\\')[-1].split('.')[0], ', 已存在, 不再下载')
                    self.text_pad.insert('2.0',
                                         '\n' + path_video_a.split('\\')[-1].split('.')[0] + ', 已存在, 不再下载')
                    path_video_a = ''
                else:
                    print(path_video_a.split('\\')[-1].split('.')[0], ', 正在下载...')
                    self.text_pad.insert('2.0', '\n' + path_video_a.split('\\')[-1].split('.')[0] + ', 正在下载...')
                    os.makedirs(self.path_var.get() + '\\ts\\' + str(inda + 1), exist_ok=True)  # 创建每一集的ts目录
                    t.submit(self.download, url_website, item, inda)  # 使用线程池
                    # download(url_website, item, ind)  # 不使用线程池
                    path_video_a = ''
            t.shutdown()
            time2 = time.time()
            print('总花费时间:' + str(time2 - self.time1)[:-12] + '秒')
            self.text_pad.insert('2.0', '已全下载完, 总花费时间:' + str(time2 - self.time1)[:-12] + '秒' + '\n\n')
            # 在ts信息栏清空告知,更直观知道全部完成了
            self.text_pad_mil.delete('1.0', 'end')
            self.text_pad_mil.insert('3.3', '已全下载完, 总花费时间:' + str(time2 - self.time1)[:-12] + '秒' + '\n')
        else:
            print('请求集数页面错误:', re1.status_code)
            self.text_pad_bot.insert('1.0', '请求集数页面错误:' + str(re1.status_code) + '\n')

    def download(self, url_website, item, ind):
        # lock = threading.Lock()  # 加上线程锁,一般就不会冲突,造成mp4文件写不进磁盘
        # lock.acquire()

        url_js = url_website + item  # 每一集的链接
        url_js = url_js.replace('/2/', '/1/')  # 把每一集里的/2/改为/1/
        print(f'第{ind + 1}集的链接', url_js)
        re2 = requests.get(url_js, headers=self.headers, timeout=15)
        if re2.status_code == 200:
            # print(re2.text)
            # "url":"(.*?),"url_next":"
            ts_url = re.findall('"url":"(.*?)","url_next":', re2.text)  # 这里与One有改动过
            ii = 0
            while len(ts_url) == 0 or ii >= 3:  # 若3次都获取不到就算了,返回空的ts_url
                ii += 1
                re2 = requests.get(url_js, headers=self.headers, timeout=15)
                ts_url = re.findall('"url":"(.*?)","url_next":', re2.text)  # 这里与One有改动过
            ts_url = ''.join(ts_url[0])  # 转成真正的字符串
            # 得到第一个m3u8链接
            ts_url = ts_url.replace('\\', '')

            print(f'第{ind + 1}集得到的第一个m3u8链接:', ts_url)  # https://v4.tlkqc.com/wjv4/202406/03/NY9tkqprPc76/video/index.m3u8

            m3u8_text = requests.get(ts_url, self.headers, timeout=15)  # 1分钟取不到数据就抛异常
            m3u8_text_status_code = m3u8_text.status_code  # 赋值,因为后边提示栏要用到
            if m3u8_text_status_code == 200:
                m3u8_text = m3u8_text.text
                # print('纯m3u8:', m3u8_text)
                m3u8_text = re.sub('#E.*', '', m3u8_text)
                m3u8_text = m3u8_text.split()       # /20220401/3Y8sevui/2000kb/hls/index.m3u8

                if 'index.m3u8?' in m3u8_text[0]:
                    m3u8_text = m3u8_text[0].split('?')[0]
                    m1 = m3u8_text.split('/')
                    m3 = ''
                    ii = 0
                    for im in m1:
                        ii += 1
                        if ii >= 4:
                            m3 += '/' + im
                    # print('第一次m3u8', m3)
                    # 得到第二个拼凑完整的有真正ts文件的m3u8链接
                    ts_url_1 = ts_url.replace('/index.m3u8', '') + m3   # u8_text[0]
                    ts_url_2 = ts_url_1.replace('/index.m3u8', '')      # 做为下边m3u8前缀用
                else:
                    ts_url_1 = ts_url.replace('index.m3u8', m3u8_text[0])
                    ts_url_2 = ts_url_1.replace('/index.m3u8', '')      # 做为下边m3u8前缀用
                print(f'第{ind + 1}集的第二个M3U8链接:', ts_url_1)

                m3u8_text = requests.get(ts_url_1, self.headers, timeout=15).text  # 1分钟取不到数据就抛异常
                m3u8_text = re.sub('#E.*', '', m3u8_text)
                m3u8_text = m3u8_text.split()

                # if self.b1 == 2:  # 电影采用拼接前部分
                if 'http' not in m3u8_text[0]:  # 如果ts没有http开头,那么就要拼接前缀给他
                    m3u8_new = []
                    for m3 in m3u8_text:
                        m3 = ts_url_2 + '/' + m3.split('/')[-1]
                        m3u8_new.append(m3)
                    m3u8_text = m3u8_new
                # print('真正的m3u8-TS:', m3u8_text)
                mts = len(m3u8_text)
                print(f'\r第{ind + 1}集ts总个数:', mts)
                # self.text_pad.delete('2.0', 'end')
                self.text_pad_mil.insert('1.0', f'第{ind + 1}集片段总个数:' + str(mts) + '\n')
                # 至此,可以开始下载所有的ts链接到指定地方进行单集的拼凑

                t1 = ThreadPoolExecutor(100)  # 线程池总数为mts个数的1倍,这里是要下载ts的
                # for ind_ts, item_ts in enumerate(m3u8_text):  # m3u8_text是每一集的ts链接
                for ind_ts in range(mts):  # m3u8_text是每一集的ts链接
                    t1.submit(self.download_ts, m3u8_text[ind_ts], ind_ts, ind,
                              mts)  # 线程池:ind是第几集, ind_ts是这一集里的第几个ts, mts是总ts个数
                t1.shutdown()
                # 再次确定下载的ts还欠缺哪些没有下载到,补下载
                self.defect_ts(m3u8_text, ind, mts)
                # 写成一个MP4文件
                self.write_mp4(ind + 1, self.b1, self.name_film,
                               mts)  # ind+1是第几集, b1=1是电视剧=2是电影, c1(self.name_film)是影视名字,
            else:
                print(f'请求第{ind + 1}集第2个m3u8返回错误码:', m3u8_text_status_code)
                self.text_pad_bot.insert('1.0',
                                         f'请求第{ind + 1}集第2个m3u8返回错误码:' + str(m3u8_text_status_code) + '\n')
        else:
            print(f'请求第{ind + 1}集第1个m3u8返回错误码:', re2.status_code)
            self.text_pad_bot.insert('1.0', f'请求第{ind + 1}集第1个m3u8返回错误码:' + str(re2.status_code) + '\n')

        # lock.release()

    # 再次确定下载的ts还欠缺哪些没有下载到,补下载
    def defect_ts(self, m3u8_text, ind, mts):
        # lock = threading.Lock()  # 加上线程锁,一般就不会冲突,造成mp4文件写不进磁盘, 写的不是同一个文件,应该不用加锁
        # lock.acquire()

        path_ts = self.path_var.get() + '\\ts\\' + str(ind + 1)
        mts_dir = len(os.listdir(path_ts))  # 实际下载到的ts总数
        if mts - mts_dir != 0:
            t3 = ThreadPoolExecutor(10)  # 开启第三个线程池
            for i in range(mts):
                file_path1 = path_ts + '\\%04d.ts' % i
                if os.path.exists(file_path1) is False:
                    print(f'\r第{ind + 1}集片段差:', mts - mts_dir, '个,正在补下载第:', file_path1.split('\\')[-1])
                    self.text_pad_mil.delete('1.0', '1.end')
                    self.text_pad_mil.insert('1.0',
                                             f'第{ind + 1}集差:' + str(mts - mts_dir).strip() + '个,正在补下载第:' +
                                             file_path1.split('\\')[-1])
                    t3.submit(self.download_ts, m3u8_text[i], i, ind, mts)
                    # download_ts(m3u8_text[i], i, ind, mts)
            t3.shutdown()

        # lock.release()

    def download_ts(self, item_ts, ind_ts, ind, mts):  # item_ts第ind_ts个ts的url,  ind_ts第几个ts, ind第几集, mts总共的ts个数
        # lock = threading.Lock()  # 加上线程锁,一般就不会冲突,造成mp4文件写不进磁盘
        # lock.acquire()
        # if self.line == 1:
        # 每次给个随机头,线路二可能不行
        self.headers = {'User-Agent': UserAgent().random}
        response = requests.get(item_ts, headers=self.headers, timeout=15)
        path_ts = self.path_var.get() + '\\ts\\' + str(ind + 1) + '\\{:04}.ts'.format(ind_ts)
        if response.status_code != 404:
            try:
                with open(path_ts, 'wb') as f:  # 直接用index命名
                    f.write(response.content)
            except IOError as e:
                print(f'Write failed: {e}')
                self.text_pad_bot.insert('1.0', f'Write failed: {e}' + '\n')
        else:
            print('请求第' + str(ind + 1) + '集的第' + str(ind_ts) + '个ts时错误!')
            self.text_pad_bot.insert('1.0', '请求第' + str(ind + 1) + '集的第' + str(ind_ts) + '个ts时错误!' + '\n')

        if os.path.exists(path_ts) is False:
            print('第' + str(ind + 1) + '集的' + path_ts.split('\\')[-1] + '下载失败')
            self.text_pad_bot.insert('1.0', '第' + str(ind + 1) + '集的' + path_ts.split('\\')[-1] + '下载失败' + '\n')
        # print('\r第'+str(ind+1)+'集:' + str(ind_ts + 1) + '/' + str(mts))
        self.text_mid_pad.insert(1.0, '第' + str(ind + 1) + '集:' + str(ind_ts + 1) + '/' + str(mts) + '\n')

        # lock.release()

    # 写成一个MP4文件
    def write_mp4(self, a1, b1, c1, mts):  # a1是第几集  b1=1电视剧=2电影, c1是影视名字, mts应有ts总数
        # lock = threading.Lock()  # 加上线程锁,一般就不会冲突,造成mp4文件写不进磁盘
        # lock.acquire()

        path_ts = self.path_var.get() + "\\ts\\" + str(a1)  # 临时存放ts文件
        mts_dir = len(os.listdir(path_ts))  # 实际下载到的ts总数
        path_video = ""
        print('正在写入:第' + str(a1) + '集...')
        self.text_pad_mil.delete('1.0', '1.end')
        self.text_pad_mil.insert('1.0', '正在写入:第' + str(a1) + '集...')
        if b1 == 1:
            path_video = self.path_var.get() + "\\电视剧\\" + c1 + "\\第%03d集.mp4" % a1  # 生成的mp4文件要放的地方
        if b1 == 2:
            path_video = self.path_var.get() + '\\电影\\' + c1 + '.mp4'  # 电影目录
        # 将ts目录下的所有文件保存到file_list列表中
        file_list = sorted(os.listdir(path_ts))
        # 将file_list列表写成固定格式: file_0000.ts 这样的格式保存到file_list.txt中
        # with open(path_ts + "\\file_list.txt", "w+") as f:
        #     for file in file_list:
        #         f.write("file '{}'\n".format(file))
        # ffmpeg_bin_dic = 'D:\\ffmpeg\\bin\\ffmpeg -f concat -safe 0 -y -i '
        # ffmpeg_bin_dic = 'D:\\ffmpeg\\ffmpeg-2024-06-13-git-0060a368b1-essentials_build\\bin\\ffmpeg -f concat -safe 0 -y -i '
        # 写成指定的一个mp4文件
        # os.system(ffmpeg_bin_dic + path_ts + '\\file_list.txt' + ' -c ' + ' copy ' + path_video + r'> nul 2> nul')
        os.system(r'copy /b ' + path_ts + '\\*.ts ' + path_video + r'> nul 2> nul')
        # 删除临时的ts文件
        # os.system(r'@echo y | del ' + path_ts + r'\*.* > nul 2> nul')  # > nul 2> nul表示不在控制台输出结果提示,并且会在最后自动按Y确认删除
        # shutil.rmtree(path_ts, ignore_errors=True)  # 这句比上局好用理解
        if os.path.exists(path_video):  # 检测MP4文件是否生产得到
            if mts - mts_dir != 0:
                print('第', a1, '集已完成, 片段差:', mts - mts_dir, '个')
                # self.text_pad.delete('2.0', '2.14')
                self.text_pad.insert('2.0', '第' + str(a1) + '集已完成, 片段差:' + str(mts - mts_dir) + '个\n')
                self.text_pad_mil.delete('1.0', '1.end')
                self.text_pad_mil.insert('1.0', '第' + str(a1) + '集已完成, 片段差:' + str(mts - mts_dir) + '个')
            else:
                print('第', a1, '集已完成, 片段完整')
                # self.text_pad.delete('2.0', '2.14')
                self.text_pad.insert('2.0', '第' + str(a1) + '集已完成, 片段完整' + '\n')
                self.text_pad_mil.delete('1.0', '1.end')
                self.text_pad_mil.insert('1.0', '第' + str(a1) + '集已完成, 片段完整')
        else:
            print('第', a1, '集写入失败')
            self.text_pad_bot.insert('1.0', '第' + str(a1) + '集写入失败' + '\n')

        # lock.release()