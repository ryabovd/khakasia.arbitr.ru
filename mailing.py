from main_news import get_settings, get_adress_list
from send_email import send_notification


def mailing(mailing_text_file):
    adress_list = get_adress_list(get_settings())
    with open(file = mailing_text_file, mode= 'r', encoding='utf-8') as file:
        subject = file.readline()
        lines_list = file.readlines()
    text = ''
    for line in lines_list:
        text += line
    send_notification(text, subject, adress_list)


mailing('offer.txt')