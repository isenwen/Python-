import random
checkcode=''
for i in range(4):
    guess=random.randint(0,3)#猜测i的值和guess的值是否相同，相同word 则赋值字母， 不同则赋值数字
    if i==guess:
        word=chr(random.randint(65,90)) #取A-Z字母
    else:
        word=random.randint(0,9)#取0-9数字
    checkcode+=str(word)
print(checkcode)
