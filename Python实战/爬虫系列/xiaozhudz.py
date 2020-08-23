import requests ,time
from lxml import etree   #从lxml库导入etree
 
 
 
#设置请求头
headers = {
    "User-Agent" : "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.88 Safari/537.36",
    "Cookie" : "BAIDUID=04210E0953548D299B0D4ECDDF05AFB1:FG=1"
}
 
all_infos = []    #设置空列表，用来装信息
for i in range(1,50):   #依次生成1-49
    url = "http://chongqing.xiaozhu.com/search-duanzufang-p" + str(i) + "-0/"  #拼接网址
    res = requests.get(url,headers=headers).text   #用requests库的get函数来访问url，并将信息转换为文本格式
    print(res)   #打印查看
    res_xpath = etree.HTML(res)   #转换为xpath格式
    urls = res_xpath.xpath('//*[@id="page_list"]/ul/li/a/@href')   #在浏览器中获得每个短租详情页的网址
    # print(urls)   #打印查看
    for url in urls:    #依次获得urls列表中的元素url
        res = requests.get(url,headers=headers).text  #注释参考上边
        print(res)
        res_xpath = etree.HTML(res)
        bed = res_xpath.xpath('//*[@id="introduce"]/li[3]/h6/text()')
        print(bed)
        bed = "".join(bed)   #将列表数据转换为str
        if bed == "共1张":    #如果 bed==“共1张”，也就是一张床的话，执行以下代码
            title = res_xpath.xpath('//*[@class="pho_info"]/h4/em/text()')
            # print(title)
            all_infos.extend(title) #list.extend可以直接将列表作为str添加到列表，此时title中只有一个元素
            address = res_xpath.xpath('//*[@class="pho_info"]/p/@title')
            # print(address)
            all_infos.extend(address)
            price = res_xpath.xpath('//*[@id="pricePart"]/div[1]/span/text()')
            # print(price)
            all_infos.extend(price)
            content = res_xpath.xpath('//*[@id="introducePart"]/div[2]/div[2]/div[1]/p/text()')
            # print(content)
            content = "".join(content)
            all_infos.append(content)
            traffic = res_xpath.xpath('//*[@id="introducePart"]/div[3]/div[2]/div[1]/p/text()')
            # print(traffic)
            traffic = "".join(traffic)
            all_infos.append(traffic)
        else:    #如果不是1张床的话
            pass   #pass 完全不考虑的了！
    #time.sleep(1)
 
for all_info in all_infos:
    with open("重庆短租.txt","a") as f: # "a"追加写入
        f.write(all_info + "\n")    #写入信息和换行
print("保存完成！")
