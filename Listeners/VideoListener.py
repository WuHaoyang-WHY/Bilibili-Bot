#!/usr/bin/env python 
# -*- coding: utf-8 -*-

from Listeners.Listener import Listener
from queue import Queue
import time
import asyncio


class VideoListener(Listener):

    def __init__(self, uid: int, queue: Queue, condition: asyncio.Condition, start_time=time.time()):
        super().__init__(uid, queue, condition)
        self.start_time = start_time

    async def run(self):
        """
        listen to user's video uploaded since start_time.
        :param start_time: video listening start time. should use a time in future
        :return: list of video dics posted after start_time
        """
        oldVideoList = None
        # every minute, fetch the video list
        while True:

            print("监听新视频中..\n")
            newVideoList = await (self.user.get_videos())
            if oldVideoList is not None:
                oldLen = len(oldVideoList["list"]["vlist"])
                newLen = len(newVideoList["list"]["vlist"])
                if oldLen < newLen:
                    newUploadedVideos = []
                    for i in range(newLen - oldLen):
                        newUploadedVideo = newVideoList["list"]["vlist"][i]
                        if newUploadedVideo["created"] >= self.start_time:
                            newUploadedVideos.append(newUploadedVideo)
                        # acquire lock
                        async with self.condition:
                            # add new list to the queue.
                            self.q.put(newUploadedVideos)
                            # notify all the consumers(eg: Comment Bot & like Bot)
                            self.condition.notify_all()

            oldVideoList = newVideoList


            # 休眠一分钟再拉取视频列表。防止太频繁被b站风控封锁（如果发生可使用代理）
            time.sleep(60)