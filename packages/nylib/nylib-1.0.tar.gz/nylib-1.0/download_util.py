import requests
import threading
from multiprocessing import cpu_count
import progressbar


class downloader:
    def __init__(self, url, filepath, header=None, proxy=None):
        self.url = url
        self.num = cpu_count() * 2
        self.name = filepath
        self.header = header
        self.proxy = proxy
        r = requests.head(self.url)
        # 获取文件大小
        self.total = int(r.headers['Content-Length'])
        # print(self.total)

    # 获取每个线程下载的区间
    def get_range(self):
        ranges = []
        offset = int(self.total / self.num)
        for i in range(self.num):
            if i == self.num - 1:
                ranges.append((i * offset, ''))
            else:
                ranges.append((i * offset, (i + 1) * offset))
        return ranges  # [(0,100),(100,200),(200,"")]

    # 通过传入开始和结束位置来下载文件
    def download(self, start, end, n):
        headers = {'Range': 'Bytes=%s-%s' % (start, end), 'Accept-Encoding': '*'}
        res = requests.get(self.url, headers=headers)
        print("%s-%s download success, part %s" % (start, end, n))
        # 将文件指针移动到传入区间开始的位置
        self.fd.seek(start)
        self.fd.write(res.content)

    def multi_thread_download(self):
        self.fd = open(self.name, "wb")

        thread_list = []
        n = 0

        for ran in self.get_range():
            # 获取每个线程下载的数据块
            start, end = ran
            n += 1
            print("start part: %s" % n)
            thread = threading.Thread(target=self.download, args=(start, end, n))
            thread.start()
            thread_list.append(thread)

        for i in thread_list:
            # 设置等待，避免上一个数据块还没写入，下一数据块对文件seek，会报错
            i.join()

        self.fd.close()

    def download_progressbar(self):
        # requests.packages.urllib3.disable_warnings()

        response = requests.request("GET", self.url, stream=True, data=None, headers=self.header, proxies=self.proxy)

        total_length = int(response.headers.get("Content-Length"))
        print("total_length", total_length)
        with open(self.name, 'wb') as f:
            # widgets = ['Processed: ', progressbar.Counter(), ' lines (', progressbar.Timer(), ')']
            # pbar = progressbar.ProgressBar(widgets=widgets)
            # for chunk in pbar((i for i in response.iter_content(chunk_size=1))):
            #     if chunk:
            #         f.write(chunk)
            #         f.flush()

            widgets = ['Progress: ', progressbar.Percentage(), ' ',
                       progressbar.Bar(marker='#', left='[', right=']'), ' ', progressbar.Timer(),
                       ' ', progressbar.ETA(), ' ', progressbar.FileTransferSpeed()]
            pbar = progressbar.ProgressBar(widgets=widgets, maxval=total_length).start()
            for chunk in response.iter_content(chunk_size=1000):

                if chunk:
                    f.write(chunk)
                    f.flush()
                # print(len(chunk))
                pbar.update(len(chunk) + 1)
            pbar.finish()


if __name__ == "__main__":
    downloader("https://jaist.dl.sourceforge.net/project/liteide/x36/liteidex36.macos-qt5.9.5.zip",
               "liteide.zip").multi_thread_download()
