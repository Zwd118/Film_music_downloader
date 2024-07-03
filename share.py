class SharedData:
    _instance = None
    _data = {}

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super().__new__(cls)
        return cls._instance

    def set(self, key, value):
        self._data[key] = value

    def get(self, key):
        return self._data.get(key)


# 使用单例
# shared_instance = SharedData()
# shared_instance.set('key', '123')
# shared_instance.set('fg', 'red')
# # 在其他模块中获取数据
# shared_instance = SharedData()
# print(shared_instance.get('key'))
