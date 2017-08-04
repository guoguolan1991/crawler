# coding:utf-8
import requests
import json
import chardet

headers = {
    'Accept': '*/*',
    'Accept-Encoding': 'gzip, deflate, sdch, br',
    'Accept-Language': 'zh-CN,zh;q=0.8',
    'Connection': 'keep-alive',
    'Host': 'club.jd.com',
    'Referer': 'https://item.jd.com/3867555.html',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36',
    'Cookie': '',
}

def crawler(page, score):
    url = 'https://club.jd.com/comment/productPageComments.action?' \
          'callback=fetchJSON_comment98vv12621&' \
          'productId=4099139&' \
          'score=0&' \
          'sortType=5&' \
          'page={}&' \
          'pageSize=10&' \
          'isShadowSku=0&' \
          'fold=1'.format(page)
    res = requests.get(url, headers=headers)
    # .content.replace('fetchJSON_comment98vv12621(', '').replace(');', '')
    res.encoding = chardet.detect(res.content)['encoding']
    result = json.loads(res.text.replace('fetchJSON_comment98vv12621(', '').replace(');', ''))
    return result['comments']

pageLen = 100
score = 5
file_object = open('comments.txt', 'w')

for s in range(score):
    for page in range(pageLen):
        result = crawler(page, s)
        print('score: %d, pageLen: %d' % (s, page))
        for item in result:
            file_object.write(json.dumps(json.loads(json.dumps(item)), ensure_ascii=False).encode('utf-8') + '\n')
            # print item
file_object.close()

