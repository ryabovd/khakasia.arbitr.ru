# arbitr.ru

Проект закрыт, так как после взлома сайтов арбитражных судов, была изменена структура страниц.
Но, за несколько месяцев работы, этот проект показал, что я кое-что могу сделать самостоятельно.

readme v 2.0
This script does not work because the structure and markup of arbitration pages has been changed since March 2022.
:(
In the future, perhaps the script will be rewritten to accommodate the new markup.

readme v 1.5

main_news.py
This script collects news headlines from the website of the Arbitration Court of the Republic of Khakassia, Arbitration Court of the Republic of Tyva,
Arbitration Court of the Krasnoyarsk region completes them with the full news text and a direct link to the news page and sends them to the specified e-mail address.
Letters are sent at intervals of 2+ seconds so as not to overload the mail server.

The files should be placed in the working directory:

send_email.py - this is the module for sending emails. 
This module contains information about the recipients of the message in the form of a list that can be changed or enlarged;

main_news_settings.json - this is the settings file of the main_news.py module that contains the date of the previous news check in the form of a dictionary:
{
    "last_date": "dd.mm.yyyy",
    "adress_list": {
        "name_0": "name@example.com",
        "name_1": "name@yandex.ru"
    }
}

settings.json is the settings file of module send_email.py which contains the settings for sending emails in the form of dictionary:
{
    "sender" : "sender_adr@example.com", 
    "sender_password" : "sender's_password" 
}

Other files in the working directory are not used, but can be created for user or debugging purposes.

The script can accept the date of the latest news on the site in the format dd.mm.yyyy as a command line argument.
In this case news is loaded and displayed AFTER the date specified as the argument.
For example, main_news.py 01.12.2021 will display news from 02.12.2021.

The error of SSL certificate checking does not affect the script operation and will be corrected.

In future versions it is planned to run the script through the terminal with the following arguments:
address of news recipient (if it is missing in send_email.py module) and others.



readme v 1.1

main_news.py
This script collects news headlines from the website of the Arbitration Court of the Republic of Khakassia, 
completes them with the full news text and a direct link to the news page and sends them to the specified e-mail address.

The files should be placed in the working directory:

send_email.py - this is the module for sending emails. 
This module contains information about the recipients of the message in the form of a list that can be changed or enlarged;

main_news_settings.json - this is the settings file of the main_news.py module that contains the date of the previous news check in the form of a dictionary:
{
    "last_date": "dd.mm.yyyy",
    "adress_list": [
        "name@example.com", 
        "name@yandex.ru"
    ]
}

settings.json is the settings file of module send_email.py which contains the settings for sending emails in the form of dictionary:
{
    "sender" : "sender_adr@example.com", 
    "sender_password" : "sender's_password" 
}

Other files in the working directory are not used, but can be created for user or debugging purposes.

The error of SSL certificate checking does not affect the script operation and will be corrected.

In future versions it is planned to run the script through the terminal with the following arguments:
minimum date of news to be uploaded, address of news recipient (if it is missing in send_email.py module) and others.




readme v.1

main_news.py
Этот скрипт собирает заголовки новостей с сайта Арбитражного суда Республики Хакасия, дополняет их полным текстом новости и прямой ссылкой на страницу новости и отправляет их на заданный адрес электронной почты.

В рабочем каталоге должны размещаться файлы:

send_email.py - это модуль для отправки писем. В этом модуле содержится информация о получателях сообщения в виде списка, который может быть изменен или увеличен.;

main_news_settings.json - это файл настроек модуля main_news.py который содержит дату предыдущей проверки новостей в виде словаря 
{
    "last_date": "dd.mm.yyyy"
}

settings.json -это файл настроек модуля send_email.py который содержит настройки для отправки электронных писем в виде словаря
{
    "sender" : "sender_adr@example.com", 
    "sender_password" : "sender's_password" 
}

Другие файлы в рабочем каталоге не используются, но могут создаваться для пользователя или отладки.

Ошибка проверки SSL сертификата не влияет на работу скрипта и будет устранена.

В будущих версиях планируется работа скрипта через терминал с аргументами: минимальная дата загружаемых новостей, адрес получателя новости (если он отсутствует в модуле send_email.py) и другие.
