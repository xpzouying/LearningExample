# -*- coding: utf8 -*-


import time
import random
from collections import deque

from utils import *


class Movie(object):
    def __init__(self, movie_name):
        self.name = movie_name
        self.state = []

    def print_state(self):
        print('State of movie: {}'.format(self.state))

    def after_download(self):
        self.state.append('downloaded')

    def after_translate(self):
        self.state.append('translated')

    def after_upload(self):
        self.state.append('uploaded')


# 1. 工作流中的三个步骤
@time_stat
def download(movie):
    time.sleep(random.randint(1, 3))
    movie.after_download()
    return movie


@time_stat
def translate(movie):
    time.sleep(random.randint(1, 2))
    movie.after_translate()
    return movie


@time_stat
def upload(movie):
    time.sleep(random.randint(1, 3))
    movie.after_upload()
    return movie


# 2. 任务流队列
class ZyQueue(object):
    """每一个工作都先推送到任务队列中，进行下一个工作流程之前，从前序任务队列取得
    """
    def __init__(self):
        self.movies = deque()

    def put(self, movie):
        self.movies.append(movie)

    def get(self):
        return self.movies.popleft()


class ZyProcesser(object):
    def __init__(self, func, in_queue, out_queue):
        """
        func: 该流程中，处理过程。
        in_queue: 任务来源的队列
        out_queue: 后一步任务队列
        """
        self.func = func
        self.in_queue = in_queue
        self.out_queue = out_queue

    def process(self):
        movie = self.in_queue.get()
        process_res = self.func(movie)
        self.out_queue.put(process_res)


# 只有zy一个苦逼操作时
def translate_movie_by_single_person(movie):
    # 1. 3个任务流队列 + 1个完成任务流的队列
    download_queue = ZyQueue()
    translate_queue = ZyQueue()
    upload_queue = ZyQueue()
    done_queue = ZyQueue()

    # 2. 产生3个处理工单
    downloader = ZyProcesser(download, download_queue, translate_queue)
    translater = ZyProcesser(translate, translate_queue, upload_queue)
    uploader = ZyProcesser(upload, upload_queue, done_queue)

    # 3. 将movie放入队列中，准备处理
    download_queue.put(movie)

    # 4. 处理流程
    downloader.process()
    translater.process()
    uploader.process()

if __name__ == '__main__':
    movie = Movie('current_movie')
    translate_movie_by_single_person(movie)
    movie.print_state()
