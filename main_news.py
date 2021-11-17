from bs4 import BeautifulSoup
import requests
import csv
from send_email import send_notification
import json
import datetime


CSV = 'news_khakasia.arbitr.ru.csv'
news_list_dict = []
HOST = 'https://khakasia.arbitr.ru'
URL = 'https://khakasia.arbitr.ru/?theme=courts_cecutient'


HEADERS = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.69 Safari/537.36'
    }

def get_last_date():
    with open('main_news_settings.json', 'r', encoding='utf-8') as file:
        settings = json.load(file)
        last_date = settings["last_date"]
    return last_date

def get_html(url, params=''):
    request_url = requests.get(url, headers=HEADERS, params=params, verify=False)
    return request_url

def get_soup(request_url):
    soup = BeautifulSoup(request_url, 'html.parser')
    return soup

def get_content_news(soup):
    items = soup.find_all('div', class_ = "b-news-content-wrapper")
    return items

def get_news_from_content(items, news_list_dict, last_date):
    for item in items:
        date_new = item.find('h6', class_="b-news-date").get_text().strip()
        if convert_date(last_date) < convert_date(date_new):
            news_list_dict.append(
                {
                    'news_date': item.find('h6', class_="b-news-date").get_text().strip(),
                    'news_title': item.find('h2', class_="b-news-title").get_text().strip(),
                    'news_link': HOST + item.find('h2', class_="b-news-title").find('a').get('href'),
                    'news_text': get_text_news(HOST + item.find('h2', class_="b-news-title").find('a').get('href'))
                }
            )
    return news_list_dict

def get_text_news(url):
    html = get_html(url, params='')
    soup = get_soup(html.text)
    news_text = get_content_text_news(soup)
    return news_text

def get_content_text_news(soup):
    items = soup.find('div', class_ = 'b-content-body-text').get_text()
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
        text += news_dict['news_date'] + '\n' + news_dict['news_title'] + '\n' + news_dict['news_link'] + '\n' + news_dict['news_text'] + '\n\n'
    return text

def date_today():
    '''Func that returned today date'''
    today = datetime.date.today()
    return today

def write_last_data_json(new_last_date):
    with open('main_news_settings.json', 'w', encoding='utf-8') as file:
        data = {}
        data['last_date'] = new_last_date
        json.dump(data, file)

def get_current_date(soup):
    current_date = soup.find('h6', class_="b-news-date").get_text().strip()
    return current_date

def convert_date(date):
    date_list = date.split('.')
    year, month, day = int(date_list[2]), int(date_list[1]), int(date_list[0])
    return datetime.date(year, month, day)

def dates_diff(last_date, current_date):
    return convert_date(current_date) > convert_date(last_date)

def main():
    last_date = get_last_date()
    html = get_html(URL, params='')
    soup = get_soup(html.text)
    current_date = get_current_date(soup)
    if dates_diff(last_date, current_date) == True:
        content = get_content_news(soup)
        news = get_news_from_content(content, news_list_dict, last_date)


    #last_date = get_last_date()
    #html = get_html(URL, params='')
    #soup = get_soup(html.text)
    #content = get_content_news(soup)
    #news = get_news_from_content(content, news_list_dict)
        save_news(news, CSV)
    else:
        print('Новостей нет')
    #text = text_for_send(news)
    #send_notification(text)
    #new_last_date = news[0]['news_date']
    #write_last_data_json(new_last_date)


if __name__ == "__main__":
    main()


# Исправить ошибку проверки SSL
# Сделать функцию проверки даты прошлой первой новости
# Написать функцию записи новой даты новостей
# + Переписать скрипт на __main__
# Написать функцию проверки даты последней новости, полученной при предыдущей проверке, и отбирающей только новые новости
# + Написать функцию отправки новостей по электронной почте
# Написать функцию проверки по расписанию ???
# Написать функцию для работы с аргументами строки