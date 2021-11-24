import json
import datetime
from main_news import *

last_date = get_last_date()


"""
def get_current_date(soup):
    current_date = soup.find('h6', class_="b-news-date").get_text().strip()
    return current_date

def convert_date(date):
    date_list = date.split('.')
    year, month, day = int(date_list[2]), int(date_list[1]), int(date_list[0])
    return datetime.date(year, month, day)

def dates_diff(last_date, current_date):
    return convert_date(current_date) > convert_date(last_date)

"""
def main():
    last_date = get_last_date()
    html = get_html(URL, params='')
    soup = get_soup(html.text)
    current_date = get_current_date(soup)
    if dates_diff == True:
        content = get_content_news(soup)
        
        current_date = convert_date(current_date)
        while current_date != convert_date(last_date):
            news = get_news_from_content(content, news_list_dict)


    #content = get_content_news(soup)
    #news = get_news_from_content(content, news_list_dict)
    #save_news(news, CSV)
    #text = text_for_send(news)
    #send_notification(text)
    #new_last_date = news[0]['news_date']
    #write_last_data_json(new_last_date)
    

    

    print('last_date', last_date)
    print('current_date', current_date)
    print(dates_diff(last_date, current_date))


if __name__ == "__main__":
    main()