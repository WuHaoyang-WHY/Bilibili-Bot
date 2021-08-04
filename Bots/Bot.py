#!/usr/bin/env python 
# -*- coding: utf-8 -*-
from Listeners.Listener import Listener
from bilibili_api import sync, Credential
from bilibili_api.user import User
from queue import Queue
import time
import asyncio


class Bot:

    def __init__(self, queue: Queue, condition: asyncio.Condition, credential: Credential = None):
        super().__init__()
        self.q = queue
        self.condition = condition
        self.credential = credential