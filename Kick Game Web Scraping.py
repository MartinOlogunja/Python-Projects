#import libraries

from bs4 import BeautifulSoup
import requests
import time
import datetime
import smtplib

# Connect to Website and pull in data

URL = 'https://www.kickgame.co.uk/products/air-jordan-4-retro-military-black-dh6927-111?variant=41784390025405'

headers = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36", "Accept-Encoding":"gzip, deflate", "Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8", "DNT":"1","Connection":"close", "Upgrade-Insecure-Requests":"1"}

page = requests.get(URL, headers=headers)

soup1 = BeautifulSoup(page.content, "html.parser")

soup2 = BeautifulSoup(soup1.prettify(), "html.parser")

title = soup2.find(class_="order-2 my-2 font-bold text-pt lg:text-4xl lg:my-4", ).get_text()

price = soup2.find(class_='money').get_text()

print(title)
print(price)


#Strip whitespace and print just values for Price and Title
price.strip()
price.strip()[1:]
price = price.strip()[1:]
title = title.strip()


#Create and format a Date and Timestamp 

import datetime
current_time = pd.Timestamp(datetime.datetime.now())
formatted_time = current_time.strftime('%Y-%m-%d %H:%M:%S')
print(formatted_time)

#Create a CSV and import the Product Title and Price into the CSV

import csv
header = ['Product', 'Price', 'Date & Time']
data = [title, price, formatted_time]

with open('KickGame_WebScraper.csv', 'w', newline='', encoding='UTF8') as f:
    writer = csv.writer(f)
    writer.writerow(header)
    writer.writerow(data)


#Read CSV using Pandas

import pandas as pd

df = pd.read_csv(r'/Users/marti/ATA/KickGame_WebScraper.csv')

print(df)

#Creating an email price alert when the product hits a specified price

def send_mail():
    server = smtplib.SMTP_SSL('smtp.gmail.com',465)
    server.ehlo()
    #server.starttls()
    server.ehlo()
    server.login('martinologunja@gmail.com','xxxxxxxxxxxxxx')
    
    subject = "The sneakers you wanted are below your target price! Now is your chance to buy!"
    body = "Martin, Lets get ready to rumble. Now is your chance to pick up the sneakers of your dreams. Don't mess it up! Link here: https://www.kickgame.co.uk/products/air-jordan-4-retro-military-black-dh6927-111?variant=41784390025405"
   
    msg = f"Subject: {subject}\n\n{body}"
    
    server.sendmail(
        'martinologunja@gmail.com',
        msg
     
    )


#Appending the data to the csv

with open('KickGame_WebScraper.csv', 'a+', newline='', encoding='UTF8') as f:
    writer = csv.writer(f)
    writer.writerow(data)


#Defining a function that pulls the data from the webpage and appends it to a CSV.

def check_price():
    URL = 'https://www.kickgame.co.uk/products/air-jordan-4-retro-military-black-dh6927-111?variant=41784390025405'

    headers = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36", "Accept-Encoding":"gzip, deflate", "Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8", "DNT":"1","Connection":"close", "Upgrade-Insecure-Requests":"1"}

    page = requests.get(URL, headers=headers)

    soup1 = BeautifulSoup(page.content, "html.parser")

    soup2 = BeautifulSoup(soup1.prettify(), "html.parser")

    title = soup2.find(class_="order-2 my-2 font-bold text-pt lg:text-4xl lg:my-4", ).get_text()

    price = soup2.find(class_='money').get_text()

    print(title)
    print(price)
    
    price = price.strip()[1:]
    title = title.strip()
    
    import datetime
    current_time = pd.Timestamp(datetime.datetime.now())
    formatted_time = current_time.strftime('%Y-%m-%d %H:%M:%S')
    print(formatted_time)
    
    import csv
    header = ['Product', 'Price', 'Date & Time']
    data = [title, price, formatted_time]
    
    with open('KickGame_WebScraper.csv', 'a+', newline='', encoding='UTF8') as f:
        writer = csv.writer(f)
        writer.writerow(data)
        
    if (price < 600):
        send_mail()

#Automating the function above to scrape the data every 24 hours

while(True):
    check_price()
    time.sleep(86400)

