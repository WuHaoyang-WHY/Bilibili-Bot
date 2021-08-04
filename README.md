# Bilibili-Bot
# Introduction
这是方便au们自动在**视频/动态**下方第一时间进行**评论/三连**的工具，au们只需要专注创作原创发病小作文。  

其他任何b站up主同样可用 ~~(如七海Nanami)~~ 等。

本项目调用的api基于[bilibili-api](https://github.com/MoyuScript/bilibili-api)，本地使用前请安装该模块
```
$ pip install bilibili-api
```

# Getting Started
### Step 1:   
获得需要自动评论的up主的uid，打开ta的bilibili个人空间就可以看到，以嘉然为例，可爱捏：  
![image](https://user-images.githubusercontent.com/45989625/128217076-6c1f6f52-ad6d-4f09-8820-9ae1b4a1ad12.png)

### Step 2:
登录b站账号后，获取自己的登录信息（一定时间后会失效），具体方法见：[获取自己的Credential](https://www.moyu.moe/bilibili-api/#/get-credential)  
```python
# 替换为你自己的b站登录事务记录，获取方法见 https://www.moyu.moe/bilibili-api/#/get-credential
credential = Credential(sessdata="your_sess_data_here" ,
                        bili_jct="your_bili_jct_here",
                        buvid3='your_buvid3_here' )
```

### Step 2.5:
写自己的犯病小作文

### Step 3:
调用监听器与评论器，监听到up主发布视频后，触发评论器行动。  
Demo:
```python
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
```

如何调用可以参考jiaranDemo.py
