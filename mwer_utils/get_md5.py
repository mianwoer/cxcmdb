# liuzhu
class StreamHasher():
    """哈希摘要生成器"""

    def __init__(self, liu='md5',size=4096):
        self.size = size
        # liu = liu.lower()
        self.hasher = getattr(__import__('hashlib'), liu.lower())() #反射，相当于hashlib.md5() 、 hashlib.sha1()
        # print(type(__import__('hashlib')))
        # self.hasher = getattr( , liu.lower())()

    def __call__(self, stream):
        return self.to_digest(stream)

    def to_digest(self, stream):
        """生成十六进制形式的摘要"""
        for buf in iter(lambda: stream.read(self.size), b''):
        # for buf in iter(stream.read(self.size), b''):
            self.hasher.update(buf)
            # print('调用一次')
        return self.hasher.hexdigest()


def main():
    """主函数"""
    hasher1 = StreamHasher()
    with open(r'C:\Users\zhuliu4\Desktop\go1.22.5.linux-amd64.tar.gz', 'rb') as f:
        print(hasher1.to_digest(f))
    hasher2 = StreamHasher('sha1')
    with open(r'C:\Users\zhuliu4\Desktop\go1.22.5.linux-amd64.tar.gz', 'rb') as stream:
        print(hasher2(stream))


if __name__ == '__main__':
    main()