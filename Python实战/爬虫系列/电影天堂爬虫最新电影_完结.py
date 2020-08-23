import requests
from lxml import etree
import time

Base_DOMAIN = 'http://dytt8.net'
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.103 Safari/537.36',
    'Referer': 'https://www.dytt8.net/html/gndy/dyzz/index.html'
}


def get_detail_urls(url):
    response = requests.get(url, headers=headers)
    text = response.text
    ret = etree.HTML(text)
    url_list = ret.xpath("//table[@class='tbspan']//a/@href")

    # lambda等价于下面
    '''
    def abc(url):
        return Base_DOMAIN+url
    '''
    # map 等价于下面
    '''
    index=0
    for detail_url in url_list:
        detail_url=abc(detail_url)
        url_list[index]=detail_url
        index+=1
    '''
    detail_urls = map(lambda url: Base_DOMAIN + url, url_list)


    return detail_urls


# 详情页
def parse_detail_page(url):
    movie = {}
    response = requests.get(url, headers=headers)
    text = response.content.decode('gbk')
    html = etree.HTML(text)
    title = html.xpath("//div[@class='title_all']/h1/font/text()")

    movie['电影名'] = title
    zoome = html.xpath("//div[@id='Zoom']")[0]
    image_post = zoome.xpath(".//img/@src")[0]
    movie['海报'] = image_post
    download_url=zoome.xpath(".//a/@href")[1]
    movie["下载地址"]=download_url
    informations = zoome.xpath(".//text()")
    def infor_replace(infor, rule):
        return infor.replace(rule, '').strip()
    for information in informations:
        if information.startswith('◎片　　名'):
            information = infor_replace(information, '◎片　　名')
            movie["片名"] = information
        elif information.startswith('◎产　　地'):
            information = infor_replace(information, '◎产   地').replace(u'\u3000',u'')
            movie["产地"] = information
        elif information.startswith('◎类　　别'):
            information = infor_replace(information, '◎类    别').replace(u'\u3000',u'')
            movie["类别"] = information
        elif information.startswith('◎片　　长'):
            information = infor_replace(information, '◎片    长').replace(u'\u3000',u'')
            movie["片长"] = information
        elif information.startswith('◎IMDb评分'):
            information = infor_replace(information, '◎IMDb评分')
            movie["IMDB评分"] = information
        elif information.startswith('◎豆瓣评分'):
            information = infor_replace(information, '◎豆瓣评分')
            movie["豆瓣评分"] = information
        elif information.startswith('◎视频尺寸'):
            information = infor_replace(information, '◎视频尺寸')
            movie["视频尺寸"] = information
        elif information.startswith('◎导    演'):
            information = infor_replace(information, '◎导    演')
            movie["导演"] = information
    return movie


def spider(page):
    base_url = 'https://www.dytt8.net/html/gndy/dyzz/list_23_{}.html'
    movies=[]
    # 第一个for循环控制页数
    for i in range(1, page):
        url = base_url.format(i)
        movies_urls = get_detail_urls(url)
        # 第二个for 循环用于遍历每一页是电影链接
        for movie_url in movies_urls:
            movie = parse_detail_page(movie_url)
            movies.append(movie)
        return movies



if __name__ == '__main__':

    page=int(input('请输入你要爬取的总页数：'))
    a=spider(page)
    print(a)