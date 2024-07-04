import line
import share


class TypeOne:  # 选择类型: 影视
    def __init__(self):
        #  在共享模块中获取数据
        self.shared = share.SharedData()
        self.line = self.shared.get('line_sure')

        if self.line == 1:  # 线路一(片库)
            # self.line_one()
            self.lineOne = line.One()  # 创建线路对象
            self.lineOne.get_film_name()  # 执行类型一 + 线路一

        if self.line == 2:  # 线路二(全能影视)
            # self.line_two()
            self.lineTwo = line.Two()  # 创建线路对象
            self.lineTwo.get_film_name()  # 执行类型一 + 线路一

        if self.line == 3:  # 线路三(电影码头)
            # self.line_three()
            self.lineThree = line.Three()  # 创建线路对象
            self.lineThree.get_film_name()  # 执行类型一 + 线路一

    # def line_one(self):
    #     self.lineOne = line.One()  # 创建线路对象
    #     self.lineOne.get_film_name()  # 执行类型一 + 线路一

    # def line_two(self):
        # self.lineTwo = line.Two()  # 创建线路对象
        # self.lineTwo.get_film_name()  # 执行类型一 + 线路一

    # def line_three(self):
    #     self.lineThree = line.Three()  # 创建线路对象
    #     self.lineThree.get_film_name()  # 执行类型一 + 线路一


class TypeTwo:  # 选择类型: 音乐
    def __init__(self):
        #  在共享模块中获取数据
        self.shared = share.SharedData()
        self.line = self.shared.get('line_sure')
        print('到这里线路:', self.line)
        # self.line_url = 'https://www.gequbao.com/s/'  # (放屁网和歌曲宝)音乐暂时三个选一样,以后找到好的,再替换上
        # self.films, self.html_primary, self.line_url, self.h_name = get_film_nameyy(self.line_url,self.sun_url)  # 待完成

    def line_one(self):
        print('到这里线路1:', self.line)

    def line_two(self):
        print('到这里线路2:', self.line)

    def line_three(self):
        print('到这里线路3:', self.line)


class TypeThree:  # 选择类型: 文件
    def __init__(self):
        pass
        # self.line_url = ''  # (文件下载)暂时三个选一样,以后找再完善
        # self.films, self.html_primary, self.line_url, self.h_name = get_film_namewj(self.line_url,self.sun_url)  # 待完成

    def line_one(self):
        pass

    def line_two(self):
        pass

    def line_three(self):
        pass
