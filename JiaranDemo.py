#!/usr/bin/env python 
# -*- coding: utf-8 -*-
"""
自动评论聖嘉然新视频的demo
"""
from Bots.VideoBot import VideoBot
from Listeners.VideoListener import VideoListener
from bilibili_api import Credential, sync
from queue import Queue
import random
import asyncio

# 聖嘉然的uid编号
jiaran_uid = 672328094

# 替换为你自己的b站登录事务记录，获取方法见 https://www.moyu.moe/bilibili-api/#/get-credential
credential = Credential(sessdata="your_sess_data_here" ,
                        bili_jct="your_bili_jct_here",
                        buvid3='your_buvid3_here' )

# 枝网发病小作文，查重率101%，欢迎补充
text_list = [
    '''👽外星人日记
地球纪年2021.7.25
今天又用陷阱捕获了不少人类。但当我看到一个叫嘉然的时候我愣住了。捕获了那么多人类，还是第一次被人类捕获了。''',

    '''“向晚，你小子被开盒了”嘉然走进房间，把手机摔在向晚的脸上，刚练完吉他的向晚满脸是汗，冰冷的手机棱角砸在脸上，白皙的脸颊微微发紫“怎么会，我相信我的顶碗人兄弟”。向晚捡起手机，打开私信评论，谩骂引入眼帘。“兄弟？呵呵，他们现在可就想要你吃官司，赔钱，毕业！”嘉然冷冷的笑着，一直被网暴的她终于也有了幸灾乐祸的机会
“不可能阿，顶碗人都是我最好的兄弟，他们不会这么做的。”向晚带着哭腔，脑海里回忆起种种过往，一起讲冷笑话一起玩游戏一起度过的美好日子。“那我不知道，反正现在舆论满天飞，他们现在都巴不得你😇，可怜我明天单播还得抗压！”嘉然一想起明天又得回到抗压的日子就气血翻涌，恨不得一巴掌扇在这个铸币大头脸上，冷哼一声:“你好自为之吧！”，独留向晚一个人瘫坐在地上，她慌忙打开手机看看评论，越看就越窒息，突然门口密码锁又解开了，是队长。“王向晚你怎么回事？！”没待向晚解释，贝拉已经一击侧踢把她踢到了墙角，向晚捂着肚子痛苦地趴在地上，“队长…我……”，“你什么你！你是不是巴不得asoul早点解散！”，“队长……真的不是我的错……我根本就…”，“还说不是你的错！你还不承认！看来今天不狠狠打你三十大棍不知道厉害了！”，“队长……我真的不是那个v……你可以查我的手机…”向晚面色苍白地说到，眼泪像断线的珠子滚落。那些污蔑自己的人不怀好意，把莫须有的东西强加到自己身上…而各种视频对比仿佛是实锤一般，一刹那，不知是委屈还是心碎，眼泪不争气地掉下来。“拉姐你相信我啊！我真的没有做任何对不起A-SOUL的事！…”''',

    '''不要做无谓的挣扎📢嘉然小姐你已经被我看中📢马上放下羞涩与我结婚📢 不要做无畏的挣扎📢嘉然小姐你已经被我看中📢马上放下羞涩与我结婚📢 不要做无畏的挣扎📢嘉然小姐你已经被我看中📢马上放下羞涩与我结婚📢嘉然小姐你已经被我看中📢马上放下羞涩与我结婚📢不要做无谓的挣扎📢嘉然小姐你已经被我看中📢马上放下羞涩与我结婚📢 不要做无畏的挣扎📢嘉然小姐你已经被我看中📢马上放下羞涩与我结婚📢 不要做无畏的挣扎📢嘉然小姐你已经被我看中📢马上放下羞涩与我结婚📢嘉然小姐你已经被我看中📢马上放下羞涩与我结婚📢不要做无谓的挣扎📢嘉然小姐你已经被我看中📢马上放下羞涩与我结婚📢 不要做无畏的挣扎📢嘉然小姐你已经被我看中📢马上放下羞涩与我结婚📢 不要做无畏的挣扎📢嘉然小姐你已经被我看中📢马上放下羞涩与我结婚📢嘉然小姐你已经被我看中📢马上放下羞涩与我结婚📢''',

    '''《祥林鼠》

“我好想做嘉然小姐的狗啊。”祥林鼠说，“可是嘉然小姐说她喜欢的是猫，我哭了。我知道既不是狗也不是猫的我为什么要哭的。因为我其实是一只老鼠。我从没奢望嘉然小姐能喜欢自己。我明白的，所有人都喜欢理解余裕上手天才打钱的萌萌的狗狗或者猫猫，没有人会喜欢阴湿带病的老鼠。等她喜欢的猫来了的时候，我就该重新滚回我的洞了吧。”

一开始，吧友们还会陪出几滴眼泪来。他就只是反复说他悲惨的《狗猫鼠》的故事，常常引了三五个易拉罐来听。但不久，大家都听得纯熟了，便是最赶潮流的梗小鬼，也不见有一点兴趣。后来所有的A友几乎都能背诵他的话，一听便厌烦得头痛。 “我好想做嘉然小姐的狗啊。”祥林鼠说。 “可是嘉然小姐说她喜欢的是猫，你哭了。你知道既不是狗也不是猫的你为什么要哭的。因为你其实是一只老鼠。”他们立即打断他的话，走开去了。

他张着口怔怔的站着，直着眼睛看他们，接着也就走了，似乎自己也觉得没趣。但他还妄想，希图从别的事，如鼠，小作文，萌萌人上，引出她的《狗猫鼠》的故事来。倘一看见正常人，他就说： “唉唉，猫已经来了，像我这样的老鼠就该重新滚回我的洞了吧……”''',
]


async def main():
    q = Queue()
    condition = asyncio.Condition()
    listener = VideoListener(jiaran_uid, q, condition, start_time=0)

    text = text_list[random.randrange(0, len(text_list))]
    bot = VideoBot(q, text, condition, credential=credential)

    listen_task = asyncio.create_task(listener.run())
    comment_task = asyncio.create_task(bot.run())

    await comment_task
    await listen_task


if __name__ == '__main__':
    asyncio.run(main())

