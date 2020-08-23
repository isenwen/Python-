##### author：iwen ######
##### date：2019/4/22######



import requests
import re
import time

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.103 Safari/537.36'
}
BASE_URL='https://www.dytt8.net'


#获取每页的25个url
def get_url(url):
    ret = requests.get(url,headers=headers).content.decode('gbk')
    link_lists=re.findall(r'<a\shref="(.*?)"\sc',ret)
    detail_urls = map(lambda url:BASE_URL+url ,link_lists)
    return detail_urls#返回的是一个map  列表，直接输入的不行的 要用for XX in XX :输出

#获取每页的下载链接
def get_parse(detail_url):
    ret = requests.get(detail_url,headers=headers).content.decode('gbk')
    download_link=re.findall(r'<td\sstyle="WORD-WRAP.*?"><a.*?>(.*?)</a></td>',ret,re.DOTALL)
    return download_link

# def save(download_link):
#     with open('D:\\test\\movies.txt','a')as f:
#         f.write(str(download_link)+'\n')

def main():
    first_time=time.time()
    pages=int(input('输入你要下载的页数:'))
    for page in range(pages+1):
        url = 'https://www.dytt8.net/html/gndy/dyzz/list_23_{}.html'.format(page)
        detail_urls=get_url(url)
        for detail_url in detail_urls:
            download_link=get_parse(detail_url)
            f=open('D:\\test\\movies.txt','a')
            f.write(str(download_link)+'\n')
            print('正在保存',download_link)
            f.close()
            # save(download_link)
    last_time=time.time()
    print("保存完毕！，花费时间%s"%(last_time-first_time))


if __name__ == '__main__':
    main()
