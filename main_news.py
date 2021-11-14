from bs4 import BeautifulSoup
import requests
import csv


CSV = 'news_khakasia.arbitr.ru.csv'
news_list_dict = []
# URL страницы поиска
#URL = 'https://khakasia.arbitr.ru'
HOST = 'https://khakasia.arbitr.ru'
URL = 'https://khakasia.arbitr.ru/?theme=courts_cecutient'


HEADERS = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.69 Safari/537.36'
    }

def get_html(url, params=''):
    request_url = requests.get(url, headers=HEADERS, params=params, verify=False)
    return request_url

def get_soup(request_url):
    soup = BeautifulSoup(request_url, 'html.parser')
    return soup

def get_content_news(soup):
    items = soup.find_all('div', class_ = "b-news-content-wrapper")
    return items

def get_news_from_content(items, news_list_dict):
    for item in items:
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

html = get_html(URL, params='')
soup = get_soup(html.text)
content = get_content_news(soup)
news = get_news_from_content(content, news_list_dict)
print(news)
save_news(news, CSV)


'''
def parser():
    html = get_html(URL)
    if html.status_code == 200:
        print('OK')
        news = get_content(html.text)
        save_news(news, CSV)
        return news
    else:
        print('Error')

def save_news(news, CSV):
    with open(CSV, 'w', encoding='utf-8')  as csvfile:
        writer = csv.writer(csvfile, delimiter=';')
        writer.writerow(['Дата', 'Заголовок', 'Ссылка'])
        for news_dict in news:
            writer.writerow( [news_dict['news_date'], news_dict['news_title'], news_dict['news_link']] )

def get_news_text(url):
    html = get_html('https://khakasia.arbitr.ru/node/16040', params='')
    tex = get_content(html.text)
    text = 'Текст новости'
    soup = BeautifulSoup(tex, 'html.parser')
    item = soup.find('div', class_ = "b-content-body-text").find_all('p').get_text()
    print(text)
    return text
    


#html = get_html(URL)
#print(html)
#print(get_content(html.text))
#save_news(parser(), CSV)
print(parser())
'''