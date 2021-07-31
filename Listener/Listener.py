#!/usr/bin/env python 
# -*- coding: utf-8 -*-

from bilibili_api import user, Credential, sync
import time
from queue import Queue
import threading


# 监听指定用户的新视频/动态
# listen to some user's new video/dynamic
class Listener:

    def __init__(self, uid: int, queue: Queue, condition: threading.Condition, credential: Credential = None):
        self.user = user.User(uid, credential)
        # event queue
        self.q = queue
        # Rlock
        self.condition = condition
