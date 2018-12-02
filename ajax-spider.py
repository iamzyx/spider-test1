import requests
from urllib import parse
import os
from hashlib import md5
from concurrent.futures import ThreadPoolExecutor


def get_page(offset=0):
    # 构造url
    # 今日头条爬取关键字
    # offset=0&format=json&keyword=%E8%A1%97%E6%8B%8D&autoload=true&count=20&cur_tab=1&from=search_tab&pd=synthesis
    # 选定关键字后，变化的只有offest，也就是分页
    headers={
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36'
    }
    params={
        'offset':offset,
        'format':'json',
        'keyword':'街拍',
        'autoload':'true',
        'count':'20',
        'cur_tab':'1',
        'from':'search_tab',
        'pd':'synthesis'
    }
    url='https://www.toutiao.com/search_content/?'+parse.urlencode(params)
    #print(url)
    try:
        response=requests.get(url=url,headers=headers)
        return response.json()  # 返回网页的json，因为ajax的XHR下面返回的是json格式
    except requests.ConnectionError:
        return None

def get_image(json):
    for item in json.get('data'):
        title=item.get('title')
        if title is None:
            continue
        image_url=item.get('image_list')
        for i in range(len(image_url)):
            # 返回一个字典，title+url
            yield {
                'title':title,
                'url':image_url[i]['url']
            }

def save_image(get_image):
    # 存储爬取结果的目录
    dir = 'E:\\python\\python-spider-get\\'
    if os.path.exists(dir + '街拍'):
        pass
    else:
        os.mkdir(dir + '街拍')
    new_dir=os.path.join(dir,'街拍')

    for i in get_image:
        tmp = os.path.join(new_dir, i['title'])
        if os.path.exists(tmp):
            # 判断是否存在
            pass
        else:
            os.mkdir(tmp)

        filepath='{0}\{1}.jpg'.format(tmp,md5(i['url'].encode('utf-8')).hexdigest())
        if os.path.exists(filepath):
            print('{0} 存在'.format(filepath))
        else:
            with open(filepath,'wb') as f:
                a = requests.get(url='http:' + i['url']).content
                f.write(a)

if __name__=='__main__':
    '''
    json=get_page(offset=0)
    a=get_image(json)
    save_image(a)
    '''
    def main(offset):
        json=get_page(offset)
        save_image(get_image(json))

    tpe=ThreadPoolExecutor(max_workers=4)
    for offset in [x*10 for x in range(20)]:
        tpe.submit(main,offset)
    tpe.shutdown(wait=True)
