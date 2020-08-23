# coding=utf-8
import smtplib
from email.mime.text import MIMEText
import schedule
import time,requests
def get_weather():
    url='https://www.apiopen.top/weatherApi?city=%E9%87%8D%E5%BA%86'
    r=requests.get(url)
    r=r.json()['data']['forecast'][0]
    dict={
        '时间':r['date'],
        '气候':r['type'],
        '风向':r['fengxiang'],
        '最高温度':r['high'],
        '最低温度':r['low']}

    L=[]
    L.append(dict)
    print(L)
    return str(L)

def sender():
    msg_from = ''  # 发送方邮箱
    passwd = ''  # 填入发送方邮箱的授权码
    msg_to = ''  # 收件人邮箱

    subject = "每日天气"  # 主题
    content = get_weather()
    msg = MIMEText(content)
    msg['Subject'] = subject
    msg['From'] = msg_from
    msg['To'] = msg_to
    try:
        s = smtplib.SMTP_SSL("smtp.qq.com", 465)
        s.login(msg_from, passwd)
        s.sendmail(msg_from, msg_to, msg.as_string())
        print("发送成功")
    except s.SMTPException as e:
        print("发送失败")
    finally:
        s.quit()

print('promgram is running....')
schedule.every().day.at('23:14').do(sender)
while 1:
    schedule.run_pending()




