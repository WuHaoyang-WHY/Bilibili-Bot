#!/usr/bin/env python 
# -*- coding: utf-8 -*-
from Bots.Bot import Bot
from bilibili_api import sync, Credential
from queue import Queue
from Comments.Comment import Comment
import asyncio


class VideoBot(Bot):

    def __init__(self, queue: Queue, text: str, condition: asyncio.Condition, credential: Credential = None):
        super().__init__(queue, condition, credential)
        self.comment_text = text

    async def run(self):
        while True:
            # acquire lock
            async with self.condition:
                # no resource available
                if self.q.qsize() == 0:
                    print("等待新视频发布中...\n")
                    await self.condition.wait()

                newVideoList = self.q.get()
                print("检测到" + str(len(newVideoList)) + "条新视频发布，前往评论...\n")
                for video in newVideoList:
                    await (Comment.comment_video(self.credential, self.comment_text, video["aid"]))
                    print("已评论视频" + video["title"] + "\n")
                print("评论完毕\n")