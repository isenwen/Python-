from requests import post
from re import search,S

def get_trans(word):
    url = "https://m.youdao.com/translate"
    headers = {
        "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 11_0 like Mac OS X) AppleWebKit/604.1.38 (KHTML, like Gecko) Version/11.0 Mobile/15A372 Safari/604.1"}
    data = {"inputtext": word,
            "type": "AUTO"}
    cookies = {"OUTFOX_SEARCH_USER_ID":"-1223178693@10.169.0.83",
               "OUTFOX_SEARCH_USER_ID_NCOO":"1174230629.1518233",
               "YOUDAO_MOBILE_ACCESS_TYPE":"0",
               "_yd_newbanner_day":"29",
               "___rl__test__cookies":"1553824332420",
               "_yd_btn_fanyi_29":"true"}
    try:
       response = post(url, headers=headers,data=data, cookies=cookies)
       return response.text
    except:
        return ""


def parse_result(text):
    try:
        result = search(
            r'<ul id="translateResult">.*<li>(.*?)</li>.*</ul>', text, flags=S).group(1)
        return result
    except:
        print("try again!")

def main():
    print('''
    =========================================
    author: Isenwen
    date:2019-3-29
    info:有道词典翻译软件
    QQ：742729764
   ========================================== 
    
    ''')
    word=1
    while word:
        word = input('请输入你需要查询的词汇(按Q\q退出程序):\n')
        if word=='Q' or word=='q':
            exit()
        else:
            text = get_trans(word)
            result = parse_result(text)
            print('翻译结果为：\n',result)



if __name__ == '__main__':
    main()
