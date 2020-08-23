###### author: isenwen #########
###### date:  2019/4/24 #########


#第 0001 题：做为 Apple Store App 独立开发者，你要搞限时促销，为你的应用生成激活码（或者优惠券），使用 Python 如何生成 200 个激活码（或者优惠券）？
'''
string.digits  输出包含数字0--9的字符串
string.ascii_letters # 包含所有字母(大写或小写)的字符串
string.ascii_lowercase # 包含所有小写字母的字符串
string.ascii_uppercase  # 包含所有大写字母的字符串
'''

import random
import string

#作用：返回A-Z &a-z &0-9
def get_str():
        numbers=string.digits
        letters=string.ascii_letters
        return numbers+letters

#作用：返回一个16位数的激活码
def get_code(str_list):
    s=''
    for i in range(17):
        letter=random.choice(str_list)
        s=s+letter
    return s #得到一个16位数的字符串

def save(s):
    with open('code.txt','a')as f:
        f.write(s+'\n')

def main():
    str_list = get_str()
    for x in range(201):
        s=get_code(str_list)
        save(s)
    print('已生成200个激活码')

if __name__ == '__main__':
    main()

