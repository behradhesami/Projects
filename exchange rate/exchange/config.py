
api_key = "7fbf27c8be6d3db4b94a992b7bb1700b9a533832"

tricker = "XAUUSD"
url = "https://api.tiingo.com/tiingo/fx/prices?tickers={}&resampleFreq=5min&token={}".format( tricker,api_key)

Kavenegar_API = '41616A2F766441492F3377676E3457514A4D675132666C676266586770706D6B71674E327466454D6E4F553D'
MAILGUN_APIKEY = ""

rulse = {
    'archive' : True,
    'email':{
        'receiver':'behradhesamii@gmail.com',
        'enable': False
    },

    'notification':{
        'reciver':'',
        'enable': True,
        'preferred': { 
            'XAUUSD':{'min':2312, 'max':2412}
        }
    }
    


} # type: ignore

