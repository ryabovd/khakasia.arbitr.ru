from urllib.request import urlopen
from urllib.error import HTTPError
from bs4 import BeautifulSoup
"""
import requests
import certifi
import csv
from send_email import send_notification
import json
import datetime
import sys
import re
import time
"""

def getTitle(url):
    try:
        html = urlopen(url)
    except HTTPError as e:
        return None
    try:
        bs = BeautifulSoup(html.read(), 'html.parser')
        title = bs.body.h1
    except AttributeError as e:
        return None
    return title


title = getTitle('http://www.pythonscraping.com/pages/page1.html')
if title == None:
    print('Title could not be found')
else:
    print(title)



"""
def main():
    CSV = 'news_arbitr.ru.csv'
    URLS = [
        'https://khakasia.arbitr.ru/?theme=courts_cecutient'
        ]


 #       ,'https://krasnoyarsk.arbitr.ru/?theme=courts_cecutient', 
 #       'https://tyva.arbitr.ru/?theme=courts_cecutient' 


    HEADERS = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.75 Safari/537.36',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'en-RU,en;q=0.9,ru-RU;q=0.8,ru;q=0.7,en-GB;q=0.6,en-US;q=0.5',
        'Cache-Control': 'max-age=0',
        'Connection': 'keep-alive',
        'Cookie': 'CUID=1bd29941-f819-4add-8cdc-196a51016357:H7SR4OhNgoYjlt68Qswpyg==; _ga=GA1.2.591100857.1617104623; tmr_lvid=4bb6f3a8b5c8abd536977934ac7412c1; tmr_lvidTS=1617104623140; _ym_uid=1617104623339866984; has_js=1; __utmc=24020832; is_agree_privacy_policy=true; __utmc=14300007; _ym_d=1649070092; .ASPXAUTH=CDB1380ECEED8CC69F97BBE9999EF35529B20465B5619F4C782935FC86AE952315CC157CF5088AD3069F3783667906B7A1D5AC69F5AAFC0959BEA60C78EAA2D50A0F1CC1064467C5DF7F54C9BBA7060849885773AF8E25DE91D5410690CF9474486DBF0D; pr_fp=54a7d574492b3fcfdb5da8e2382cdd9ec1f702dfb801e8d1b870ba18bdf0f3cc; rcid=10deba7b-dc3b-47c0-899e-df1091c5597c; KadLVCards=А33-37639/2020; tmr_reqNum=19; SESS46fae3028d5b7aae30c760ca4bdc7a2b=th8dlvjpokg803h5p73ts8qes7; __utma=24020832.591100857.1617104623.1649302412.1649302412.1; __utmz=24020832.1649302412.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none); _ym_isad=1; __utmb=24020832.2.10.1649302412; session-cookie=16e381b11ad0da094a413d02beb261f55b707e971825d5ea4145144789b65a0dc706fadd5705a13b62b00203493811fb; _dd_s=logs=1&id=8e962e33-81a4-404a-87c3-8bfc89fdf536&created=1649304047744&expire=1649306033034',
        'Host': 'khakasia.arbitr.ru',
        'Referer': 'https://khakasia.arbitr.ru/',
        'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="100", "Google Chrome";v="100"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'Sec-Fetch-Dest': 'document',
        'Sec-Fetch-Mode': 'navigate',
        'Sec-Fetch-Site': 'same-origin',
        'Sec-Fetch-User': '?1',
        'Upgrade-Insecure-Requests': '1'
        }
    
    settings = get_settings()
    if len(sys.argv) > 1:
        last_date = get_last_date(sys.argv[1])
    else:
        last_date = settings['last_date']
    
    for URL in URLS:
        html = get_html(URL, HEADERS)
        print(html)
        soup = get_soup(html.text)
        print(soup)
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
            adress_list = get_adress_list(settings)
            send_notification(text, subject, adress_list)
            new_last_date = news[0]['news_date']
            settings['last_date'] = new_last_date
            write_new_settings_json(settings)
        else:
            print('Новости ОТСУТСТВУЮТ\n')
    print('Работа скрипта ЗАВЕРШЕНА\n')

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
    return request_url

def get_soup(request_url):
    soup = BeautifulSoup(request_url, 'html.parser')
    print(soup)
    return soup

def get_court(soup):
    #print(soup)
    title = soup.find('h1')
    #print('TITLE', title)
#    court_match = re.search(r"(А[ a-яА-Я]+)$", title)
#    court = court_match.group(0)
    return 'title'

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
    '''That func prepared text of message and add footer with add_footer func'''
    text = ''
    for news_dict in news:
        text += news_dict['news_date'] + '\n' + news_dict['news_title'] + '\n' + news_dict['news_link'] + '\n' + news_dict['news_text'] + '\n'
    text += add_footer()
    return text

def add_footer():
    '''In that func contains text of message's footer.'''
    footer = '\nОТКАЗАТЬСЯ от получения рассылок ▼ \n\nmailto:secretary@you-right.info?subject=UNSUBSCRIBE&body=Не%20присылайте%20больше%20писем'
    return footer

def get_adress_list(settings):
    adresses = settings['adress_list'].items()
    adress_list = []
    for k, v in adresses:
#Need some fix here. What is 'k'?
        adress_list.append(v)
    return adress_list

def date_today():
    '''Func that returned today date'''
    today = datetime.date.today()
    return today

def write_new_settings_json(settings):
    with open('main_news_settings.json', 'w', encoding='utf-8') as file:
        json.dump(settings, file, indent=4, ensure_ascii=False)


if __name__ == "__main__":
    start_time = time.time()
    main()
    seconds = time.time() - start_time
    print('Время работы программы:', time.strftime("%H:%M:%S",time.gmtime(seconds)))


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
"""