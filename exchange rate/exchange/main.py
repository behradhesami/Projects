
import json
import os
import requests
import pandas as pd 

from config import url,tricker,rulse
from Send_Mail import send_smtp_email
from notification import send_sms


def get_rates():
    """
    send a get requests to the tiingo.io api and get XAUUSD live rates
    :return: request.Response instance
    """

    headers = {
    'Content-Type': 'application/json'
    }

    
    requestResponse = requests.get(url, headers=headers)
    data = requestResponse.json()

    df = pd.DataFrame.from_dict(data)

    df.to_csv('{}.csv'.format("XAUUSD"))



def archive(filename, rates):
    """
    get filename and rates, save them to the specific directory
    :param filename:
    :param rates:
    :return: None

    """
    if not os.path.exists('archive'):
        os.makedirs('archive')
    
    with open(f'archive/{filename}.json', 'w') as f:
        json.dump(rates, f, indent=4)


### send rates to Email###
def send_mail(rates):
    """
    send email through smtp
    :param rates:
    :return:
    """
    subject  = 'rates'
    text = json.dumps(rates)
    send_smtp_email(subject, text)


def check_notify_rulse(rates):
    preferred = rulse['notification']['preferred']
    msg = ''
    for exc in preferred:
        if rates[exc] <= preferred[exc]['min']:
            msg+= f'{exc} reached min {rates[exc]}'
    
        if rates[exc] >= preferred[exc]['max']:
            msg+= f'{exc} reached max {rates[exc]}'

    return msg


def send_notification(msg):
    send_sms(msg)

if __name__ == "__main__":
    respond = get_rates()

    if rulse ['archive']:
        archive(tricker,respond)

    if rulse['email']['enable']:
        send_mail(respond)

    if rulse['notification']['enable']:
        notif_message = check_notify_rulse(archive(tricker,respond))
        if notif_message:
            send_notification(notif_message)