import time
from On_Air_bot.src.modules import twitch_api
import requests


API_TOKEN = '<Bot_token>'
CHANNEL_ID = '<Chanel_ID>' # view -int


Unit = twitch_api.Streaminfo('<"client_id">, <"client_secret">, <"user_name">')
# < Example_class >  = twitch_api.Streaminfo( < client_id >,< client_secret >,< name_chanel >)

def send_to_telegram(text: str):
    url = "https://api.telegram.org/bot"
    url += API_TOKEN
    method = url + "/sendMessage"

    r = requests.post(method, data={
         "chat_id": CHANNEL_ID,
         "text": text
          })

    if r.status_code != 200:
        raise Exception("post_text error")


status = 0 # Current state of the stream [0 - Off,1 - OnAir]

while True:
    if Unit.stream()[0]['type'] == 'live':
        if status == 0:
            send_to_telegram('<Example message>')
            status = 1
        time.sleep(1800)
    if Unit.stream()[0]['type'] == 'Offline':
        status = 0
        time.sleep(300)
