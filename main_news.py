from bs4 import BeautifulSoup
import requests
import certifi
import csv
from send_email import send_notification
import json
import datetime
import sys
import re


def main():
    CSV = 'news_khakasia.arbitr.ru.csv'
    URLS = [
        'https://khakasia.arbitr.ru/?theme=courts_cecutient',
        'https://krasnoyarsk.arbitr.ru/?theme=courts_cecutient', 
        'https://tyva.arbitr.ru/?theme=courts_cecutient'
        ]
    HEADERS = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.69 Safari/537.36'
        }
    
    settings = get_settings()
    if len(sys.argv) > 1:
        last_date = get_last_date(sys.argv[1])
    else:
        last_date = settings['last_date']
    
    for URL in URLS:
        html = get_html(URL, HEADERS)
        soup = get_soup(html.text)
        court = get_court(soup)
        print('\n' + court)
        print('\nПолучаем новости с {}\n'.format(last_date))
        current_date = get_current_date(soup)
        if dates_diff(last_date, current_date) == True:
            content = get_content_news(soup)
            host_match = re.match(r"(.+\/)", URL)
            HOST = host_match.group(0)
            news = get_news_from_content(content, last_date, HOST, HEADERS)
            print('\nНовости получены')
            save_news(news, CSV)
            print('Новости сохранены')
            text = text_for_send(news)
            subject = court + ' | Новости на'
            adress_list = settings['adress_list']
            send_notification(text, subject, adress_list)
            new_last_date = news[0]['news_date']
            settings['last_date'] = new_last_date
            write_new_settings_json(settings)
        else:
            print('Новости ОТСУТСТВУЮТ\n')

def get_settings():
    with open('main_news_settings.json', 'r', encoding='utf-8') as file:
        settings = json.load(file)
    return settings

def get_last_date(date_from_argv):
    pattern_date = r'^(\d\d.\d\d.\d\d\d\d)$'
    last_date = re.findall(pattern_date, date_from_argv)
    return last_date[0]

def get_html(url, HEADERS):
    #s = requests.Session()
    #s.verify = certifi.where()
    request_url = requests.get(url, HEADERS, verify=False)
    #print(request_url)
    return request_url

def get_soup(request_url):
    soup = BeautifulSoup(request_url, 'html.parser')
    return soup

def get_court(soup):
    title = soup.find('title').get_text().strip()
    court_match = re.search(r"(А[ a-яА-Я]+)$", title)
    court = court_match.group(0)
    return court

def get_current_date(soup):
    current_date = soup.find('h6', class_="b-news-date").get_text().strip()
    return current_date

def convert_date(date):
    date_list = date.split('.')
    year, month, day = int(date_list[2]), int(date_list[1]), int(date_list[0])
    return datetime.date(year, month, day)

def dates_diff(last_date, current_date):
    return convert_date(current_date) > convert_date(last_date)

def get_content_news(soup):
    items = soup.find_all('div', class_ = "b-news-content-wrapper")
    return items

def get_news_from_content(items, last_date, HOST, HEADERS):
    news_list_dict = []
    for item in items:
        date_new = item.find('h6', class_="b-news-date").get_text().strip()
        if convert_date(last_date) < convert_date(date_new):
            news_list_dict.append(
                {
                    'news_date': item.find('h6', class_="b-news-date").get_text().strip(),
                    'news_title': item.find('h2', class_="b-news-title").get_text().strip(),
                    'news_link': HOST + item.find('h2', class_="b-news-title").find('a').get('href'),
                    'news_text': get_text_news(HOST + item.find('h2', class_="b-news-title").find('a').get('href'), HEADERS)
                }
            )
    return news_list_dict

def get_text_news(url, HEADERS):
    html = get_html(url, HEADERS)
    soup = get_soup(html.text)
    news_text = get_content_text_news(soup)
    return news_text

def get_content_text_news(soup):
    items = soup.find('div', class_ = 'b-content-body-text').get_text() + '\n'
    return items

def save_news(news, CSV):
    with open(CSV, 'w', encoding='utf-8')  as csvfile:
        writer = csv.writer(csvfile, delimiter=';')
        writer.writerow(['Дата', 'Заголовок', 'Ссылка', 'Текст'])
        for news_dict in news:
            writer.writerow( [news_dict['news_date'], news_dict['news_title'], news_dict['news_link'], news_dict['news_text']] )

def text_for_send(news):
    text = ''
    for news_dict in news:
        text += news_dict['news_date'] + '\n' + news_dict['news_title'] + '\n' + news_dict['news_link'] + '\n' + news_dict['news_text'] + '\n'
    return text

def date_today():
    '''Func that returned today date'''
    today = datetime.date.today()
    return today

def write_new_settings_json(settings):
    with open('main_news_settings.json', 'w', encoding='utf-8') as file:
        json.dump(settings, file, indent=4)


if __name__ == "__main__":
    main()


# Написать вывод в консоль время выполнения скрипта
# Исправить ошибку проверки SSL
# Написать функцию для работы с аргументами строки (с какой даты, выводить в консоль, отправлять по почте)
# +Исправить функцию записи json, чтобы записывать красивые файлы
# Написать функцию проверки по расписанию ???
# +Переписать send_email.py, чтобы она брала список адресов из вне. Придумать где и как хранить список адресов или список адресов и фамилий
# +Сделать функцию проверки даты прошлой первой новости
# +Написать функцию записи новой даты новостей
# +Переписать скрипт на __main__
# +Написать функцию проверки даты последней новости, полученной при предыдущей проверке, и отбирающей только новые новости
# +Написать функцию отправки новостей по электронной почте
