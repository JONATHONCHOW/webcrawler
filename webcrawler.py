# -*- coding: utf-8 -*-
import requests
from lxml import etree
import os
import pandas as pd

def get_html(url):
    headers = {'User-Agent':'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.121 Mobile Safari/537.36'}
    try:
        html = requests.get(url,headers = headers)
        html.encoding = html.apparent_encoding
        if html.status_code == 200:
            print('成功获取源代码')
    except Exception as e :
        print('获取代码失败:s% ' % e)
    return html.text

def parse_html(html):
    movies = []
    imgurls = []
    html = etree.HTML(html)
    lis = html.xpath("//ol[@class='grid_view']/li")
    for li in lis:
        rank = li.xpath(".//div[@class='pic']/em/text()")[0]
        name = li.xpath(".//a/span[@class='title']/text()")[0]  #提取电影名称数组
        director_actor = li.xpath(".//div[@class='bd']/p/text()")[0].strip()  #提取导演演员等信息，strip()清除空格
        info = li.xpath(".//div[@class='bd']/p/text()")[1].strip()   #xpath谓语用法
        rating_score = li.xpath(".//div[@class='star']/span[2]/text()")[0]
        rating_num = li.xpath(".//div[@class='star']/span[4]/text()")[0]
        try:
            introduce = li.xpath(".//p[@class='quote']/span/text()")[0]
        except:
            introduce = ""
        imgurl = li.xpath(".//img/@src")[0]


        movie = {'rank':rank,'name':name,'director_actor':director_actor,'info':info,'rating_score':rating_score,'rating_num':rating_num,'introduce':introduce}   #以列表形式输出
        movies.append(movie)
        imgurls.append(imgurl)
    return movies,imgurls

def downloading(url,movie):
    if 'movieposter' in os.listdir('douban250/'):
        pass
    else:
        os.mkdir('douban250/movieposter/')
    os.chdir('douban250/movieposter/')
    img = requests.get(url).content
    with open(movie['rank']+'.jpg','wb') as f:
        print("正在下载：%s" % url)
        f.write(img)
    os.chdir('..')
    os.chdir('..')

if __name__ == '__main__':
    movies1 = []
    imgurls1 = []
    for i in range(10):
        url = 'https://movie.douban.com/top250?start=' + str(i * 25) + '&filter='
        html = get_html(url)
        movies2, imgurls2 = parse_html(html)
        print(len(movies2), len(imgurls2))
        movies1.extend(movies2)
        imgurls1.extend(imgurls2)
        print(len(imgurls1), len(movies1))
    for i in range(250):
        downloading(imgurls1[i], movies1[i])

    os.chdir('douban250/')
    moviedata = pd.DataFrame(movies1)
    moviedata.to_csv('movie.csv')