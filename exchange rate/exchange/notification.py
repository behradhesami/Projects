"""
    send notification to the phone
"""
from config import rulse    
from kavenegar import *

from config import Kavenegar_API
def send_sms(text):
    try:
        api = KavenegarAPI(Kavenegar_API)
        params = {
            'sender': '10004346',
            'receptor': rulse['notification']['reciver'],
            'message': text
        }   
        response = api.sms_send(params)
        print (str(response))
    except APIException as e: 
            print (str(e))
    except HTTPException as e: 
            print (str(e))