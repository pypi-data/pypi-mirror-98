from tqdm import trange
from rich.progress import track
import time


def tqdm_test():
    for i in trange(10):
        time.sleep(1)


def rich():
    for step in track(range(30)):
        print('早起Python')
        time.sleep(0.5)


if __name__ == '__main__':
    # rich()
    tqdm_test()