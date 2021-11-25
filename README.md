# khakasia.arbitr.ru

readme v.1

main_news.py
This script collects news headlines from the website of the Arbitration Court of the Republic of Khakassia, 
completes them with the full news text and a direct link to the news page and sends them to the specified e-mail address.

The files should be placed in the working directory:

send_email.py - this is the module for sending emails. 
This module contains information about the recipients of the message in the form of a list that can be changed or enlarged;

main_news_settings.json - this is the settings file of the main_news.py module that contains the date of the previous news check in the form of a dictionary 
{
    "last_date": "dd.mm.yyyy"
}

settings.json is the settings file of module send_email.py which contains the settings for sending emails in the form of dictionary
{
    "sender" : "sender_adr@example.com", 
    "sender_password" : "sender's_password" 
}

Other files in the working directory are not used, but can be created for user or debugging purposes.

The error of SSL certificate checking does not affect the script operation and will be corrected.

In future versions it is planned to run the script through the terminal with the following arguments:
minimum date of news to be uploaded, address of news recipient (if it is missing in send_email.py module) and others.
