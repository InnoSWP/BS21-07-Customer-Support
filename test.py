import requests
import json
id = 459977089
text = "Привет"
data = {}
data['chat_id'] = id
data['text'] = text
keyboard = json.dumps({
            "inline_keyboard": [
                [
                    {"text": "Start", "callback_data": f'ок'},
                ]
            ]
        })
data['reply_markup'] = keyboard
requests.post(url="https://api.telegram.org/bot5505131588:AAF_LojeoLfIAlhd6UJnV36gDS-yDZei9Nw/sendMessage",
              data=data)