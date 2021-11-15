import datetime
import smtplib
import json


def send_notification(text):
    email = ['ryabovd@outlook.com']
    with open('settings.json', 'r', encoding='utf-8') as file:
        settings = json.load(file)
        sender = settings["sender"]
        sender_password = settings["sender_password"]
    mail_lib = smtplib.SMTP_SSL('smtp.yandex.ru', 465)
    mail_lib.login(sender, sender_password)
    for to_item in email:
        msg = 'From: %s\r\nTo: %s\r\nContent-Type: text/plain; charset="utf-8"\r\nSubject: %s\r\n\r\n' % (
            sender, to_item, 'Новости арбитражного суда Республики Хакасия на {}'.format(date_today()))
        msg += text
        mail_lib.sendmail(sender, to_item, msg.encode('utf8'))
    mail_lib.quit()


def date_today():
    '''Func that returned today date'''
    today = datetime.date.today()
    return today
