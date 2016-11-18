#TasksQueue

## 利用Queue制作任务流


## 背景：
人员：zy
由于zy是美剧《权力的游戏》忠实粉丝，希望《权力的游戏》能够在网上被大家都能观看。
收到英语水平的限制，普遍没法观看英文原版的美剧，所以zy作为忠实的爱好者，希望能进行制作中文字幕，提供给大家欣赏。

我们由此得出一个工作任务流：
    1. 从网上下载得到最新的《权力的游戏》
    2. 根据当前视频，制作字幕
    3. 上传到网盘提供给大家下载


## 开发过程
### 第一阶段：
    所有的翻译人员为zy一个人，也就是单进程。

### 第二阶段：
    随着美剧越来越多，zy一个人制作字幕翻译不过来了，但是随着美剧爱好者队伍越来越强大后，也产生了越来越多的志愿者。


## 解析过程
基础通用代码

```python
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
```

Movie类，当完成每一个流程后，会出发相应的处理，修改Movie的状态。
使用print_state()可以打印当前movie的状态。

```python
    # 工作流中的三个步骤，每一个工作流过程都需要消耗一段时间
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
```

```python
    # 任务流队列
    class ZyQueue(object):
        def __init__(self):
            self.deque = deque()

        def put(self, item):
            self.deque.append(item)

        def get(self):
            return self.deque.popleft()
```

任务流队列，会有三个队列，每个队列都类似一个生产者/消费者的过程，只有前序队列处理完相应的电影后，传递给后续队列。

    [download-queue] ---> [translate-queue] ---> [upload-queue]


```python
    class ZyProcesser(object):
        def __init__(self, func, in_queue, out_queue):
            """
            func: 该流程中，处理过程。download, translate or upload
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
```

### 第一阶段：

```python
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
```

只有zy一个人做义工，同时需要去做download、translate和upload三个过程。


### 第二阶段：
    随着越来越多的美剧加入，我们加入了多人（多线程）支持。
    
