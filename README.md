# sina_comment
用Python爬取微博评论对数据进行情感分析进行数据可视化

- 可以看到最新评论的url是`'https://m.weibo.cn/api/comments/show?id=' + 微博id + '&page=' + 页码`

![](http://upload-images.jianshu.io/upload_images/6078268-7e1ef9c132a91fc2.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

点来链接**https://m.weibo.cn/single/rcListformat=cards&id=4193705642468999&type=comment&hot=0&page=2**即为返回的json格式的数据


接下来直接上代码
```
import re
import time
import requests

uid = '4193705642468999'
url = 'https://m.weibo.cn/single/rcList?format=cards&id=' + uid + '&type=comment&hot=0&page={}'
headers = {
"Accept": "application/json, text/javascript, */*; q=0.01",
"Accept-Encoding": "gzip, deflate, br",
"Accept-Language": "zh-CN,zh;q=0.9",
"Connection": "keep-alive",
"Cookie": "你的cookie",
"Host": "m.weibo.cn",
"Referer": "https://m.weibo.cn/status/" + uid,
"User-Agent": "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.75 Mobile Safari/537.36",
"X-Requested-With": "XMLHttpRequest",
}

i = 0
comment_num = 1  # 第几条评论
while True:
res = requests.get(url=url.format(i), headers=headers)
r = res.json()
content = r[0]['card_group']
if r.status_code == 200:
    try:
        for j in range(0, len(content)):
            hot_data = content[j]
            comment_id = hot_data['user']['id']  # 用户id
            user_name = hot_data['user']['screen_name']  # 用户名
            created_at = hot_data['created_at']  # 评论时间
            comment = re.sub('<.*?>|回复<.*?>:|[\U00010000-\U0010ffff]|[\uD800-\uDBFF][\uDC00-\uDFFF]', '', hot_data['text'])  # 评论内容
            like_counts = hot_data['like_counts']  # 点赞数
            comment_num += 1
        i += 1
        time.sleep(3)
    except Exception as e:
        logger.debug(e)
else:
    break
```

#2.对数据的情感分析
![一](http://upload-images.jianshu.io/upload_images/6078268-f90f79de76779326.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)
![二](http://upload-images.jianshu.io/upload_images/6078268-9cd8dcfb191589a5.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

![](http://upload-images.jianshu.io/upload_images/6078268-c84742826a514d4d.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)
![微博 一个人说一个，追女孩的小道理 评论的情感值分布](http://upload-images.jianshu.io/upload_images/6078268-ccc433cacfe2d77d.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

顺便统计了一下出现比较多的评论(有博主为了抢热门频繁刷评论？)

1.一定要主动啊 不然等女孩子主动吗！但是主动也要适度 别让对方觉得害怕…

2.人品要好，三观要正确，责任感，孝顺善良这些内在因素也很重要

3.追某个女孩时时 只追她一个人 千万别撩别人 

4.言谈幽默风趣但不要轻佻

5.对她当女儿养吧

6.女孩子是要用来宠的，不是来跟她讲道理的。

7.多陪她聊天，多关心她，爱护她，保护她，了解她，宠她，尊重她，给她安全感

8.不要暧昧不清，不要套路

### 文末彩蛋：
**有很多男生抱怨自己追不到喜欢的姑娘，追了几个星期就放弃了。其实，要改变的是你自己，只要努力向上，让自己变得更优秀，同时对姑娘保持适当的关心和热情，坚持几个月，总有一天你就会发现，不喜欢就是不喜欢这是没有办法的事情。**


最后：祝大家狗年脱单～