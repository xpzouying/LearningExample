# -*- coding: utf8 -*-


import time
import random
from collections import deque
from threading import Thread

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
def download(movie):
    time.sleep(1)
    movie.after_download()
    return movie


def translate(movie):
    time.sleep(2)
    movie.after_translate()
    return movie


def upload(movie):
    time.sleep(1)
    movie.after_upload()
    return movie


# 2. 任务流队列
class ZyQueue(object):
    def __init__(self):
        self.deque = deque()

    def put(self, item):
        self.deque.append(item)

    def get(self):
        return self.deque.popleft()


# zy一个人做所有流程
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


# 招募更多的美剧爱好者一起download、upload、translate
# 引入进程类，调整更为智能
class Processer(Thread):
    def __init__(self, func, in_queue, out_queue):
        self.func = func
        self.in_queue = in_queue
        self.out_queue = out_queue

    def process(self):
        # 从前序队列中获取一部电影
        movie = self.in_queue.get()

        # 处理电影
        process_res = self.func(movie)

        # 交给后续队列
        self.out_queue.put(process_res)

    def run(self):
        self.process()


# 只有zy一个苦逼操作时
@time_stat
def translate_movie_by_single_person(movie_list):
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
    for movie in movie_list:
        download_queue.put(movie)

        # 4. 处理流程
        downloader.process()
        translater.process()
        uploader.process()


@time_stat
def translate_movie_together(movie_list):
    # 1. 3个任务流队列 + 1个完成任务流的队列
    download_queue = ZyQueue()
    translate_queue = ZyQueue()
    upload_queue = ZyQueue()
    done_queue = ZyQueue()

    # 2. 多个志愿者一起干活，分别负责download、translate、upload
    # 不需要把压力都放在我一个人身上
    movie_fans = [
        Processer(download, download_queue, translate_queue),
    ]


if __name__ == '__main__':
    movie_list = []
    movie_list.append(Movie('movie1'))
    movie_list.append(Movie('movie2'))
    translate_movie_by_single_person(movie_list)
