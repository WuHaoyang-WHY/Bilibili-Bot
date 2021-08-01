#!/usr/bin/env python 
# -*- coding: utf-8 -*-

from Listeners.Listener import Listener
from bilibili_api import sync, Credential
from bilibili_api.user import User
from queue import Queue
import time
import threading


class VideoListener(Listener):

    def __init__(self, uid: int, queue: Queue, condition: threading.Condition, start_time=time.time()):
        super().__init__(uid, queue, condition)
        self.start_time = start_time

    def run(self):
        """
        listen to user's video uploaded since start_time.
        :param start_time: video listening start time. should use a time in future
        :return: list of video dics posted after start_time
        """
        oldVideoList = None
        # every minute, fetch the video list
        while True:
            # acquire lock
            if self.condition.acquire():
                newVideoList = sync(self.user.get_videos())
                if oldVideoList is not None:
                    oldLen = len(oldVideoList["list"]["vlist"])
                    newLen = len(newVideoList["list"]["vlist"])
                    if oldLen < newLen:
                        newUploadedVideos = []
                        for i in range(newLen - oldLen):
                            newUploadedVideo = newVideoList[i]
                            if newUploadedVideo["created"] >= self.start_time:
                                newUploadedVideos.append(newUploadedVideo)
                        # add new list to the queue.
                        self.q.put(newUploadedVideos)
                        oldVideoList = newVideoList
                        # notify all the consumers(eg: Comment Bot & like Bot)
                        self.condition.notify_all()

                # release lock
                self.condition.release()

            time.sleep(60)