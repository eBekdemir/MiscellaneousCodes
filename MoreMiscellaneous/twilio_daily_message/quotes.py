from twilio.rest import Client
import requests
from datetime import datetime, timedelta
import time
from win10toast import ToastNotifier
import json
import random
from dotenv import load_dotenv
import os

load_dotenv()

toaster = ToastNotifier()

def isConnected():
    try:
        requests.get('https://www.google.com/', timeout=5)
        return True
    except requests.ConnectionError:
        return False

with open(r"C:\Users\excalibur\Desktop\Codes\MoreMiscellaneous\twilio_daily_message\quotes.json", 'r', encoding='utf-8') as f:
    data = json.load(f)

account_sid = os.getenv("TWILIO_ACCOUNT_SID")
auth_token = os.getenv("TWILIO_AUTH_TOKEN")
twilio_number = os.getenv("TWILIO_NUMBER")
my_number = os.getenv("MY_TEL_NUMBER")

no_internet_sleep_time = [60, 120, 300, 600, 1800, 3600]
c = 0
while True:
    if isConnected() == False:
        toaster.show_toast("Quotes", 'No internet connection!', duration=10)
        time.sleep(no_internet_sleep_time[c])
        c = 0 if c == 5 else c+1
        
    elif datetime.now().hour >= 8 and not datetime.now().strftime("%d.%m.%Y") in data[0]['sended_dates']:
        sended = set(data[0]['sended_indexes'])
        indexes = set(range(1, len(data)-1))
        will_send = list(indexes - sended)
        if not will_send:
            data[0]['sended_indexes'] = []
            will_send = list(indexes - sended)
        mes_index = random.choice(will_send)
        
        message = '\n' + data[mes_index]['quote'] + "\n" + data[mes_index]['author']

        client = Client(account_sid, auth_token)

        message = client.messages.create(
            from_=twilio_number, 
            body=message, 
            to=my_number
        )

        toaster.show_toast("Quotes", 'Message sent!\n{}'.format(message.body), duration=20)
        
        data[0]['sended_indexes'].append(mes_index)
        data[0]['sended_dates'].append(datetime.now().strftime("%d.%m.%Y"))
        with open('quotes.json', 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=4)
        time.sleep(3600*23) # it can be like 8.56 am

    else:
        now = datetime.now()
        target = now.replace(hour=8, minute=0, second=0, microsecond=0)
        if now > target:
            target += timedelta(days=1)
        remaining = (target - now).total_seconds()

        toaster.show_toast("Quotes", 'Time until next 8 am {} seconds'.format(int(remaining)), duration=10)
        time.sleep(int(remaining) + 5)