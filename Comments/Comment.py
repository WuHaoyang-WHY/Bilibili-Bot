#!/usr/bin/env python 
# -*- coding: utf-8 -*-
import asyncio
from bilibili_api import video, Credential, comment, bvid2aid
import queue


class Comment:

    # comment the video. must need either av_id or bv_id.
    @staticmethod
    async def comment_video(credential, text, av_id=None, bv_id=None):
        if av_id is None:
            if bv_id is None:
                raise Exception("请至少提供 bvid 和 aid 中的其中一个参数。")
            # BV_ID TO AV_ID
            av_id = bvid2aid(bv_id)

            # 给视频评论
        await comment.send_comment(text=text, oid=av_id, type_=comment.ResourceType.VIDEO, credential=credential)

    # 评论动态
    @staticmethod
    async def comment_dynamic(text, credential, oid):
        await comment.send_comment(text=text, oid=oid, type_=comment.ResourceType.DYNAMIC, credential=credential)




