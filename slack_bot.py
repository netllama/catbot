# import related library
import requests
from slack import WebClient
from slack.errors import SlackApiError
from slackeventsapi import SlackEventAdapter

class SlackBot:
    # payload sample
    payload = {
        "channel": "",
        "blocks": [

        ],
        "icon_url": "",
    }

    # the constructor of the class. It takes the channel name, slack bot taken, and bot avatar
    # as input parameters.
    def __init__(self, channel, token, bot_icon):
        self.channel = channel
        self.token = token
        self.bot_icon = bot_icon
    
    # set the channel
    def __decide_channel(self):
        self.payload["channel"] = self.channel

    # use the input message to change the payload content. this method will remove previous
    # message to prevent duplicate. 
    def decide_message(self, message):
        m = {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": (
                        message
                    )
                }
            }
        for item in self.payload["blocks"]:
            self.payload["blocks"].remove(item)
        self.payload["blocks"].append(m)

    # use input url of picture to change the payload content.
    # this method will remove previous message to prevent duplicate.
    def decide_picture_as_message(self, pic_url):
        for item in self.payload["blocks"]:
            self.payload["blocks"].remove(item)
        accessory = dict(type="image", image_url=pic_url, alt_text="image")
        self.payload["blocks"].append(accessory)

    # decide slack app's avatar
    def __decide_bot_icon(self, url):
        self.payload["icon_url"] = url

    # craft and return the entire message payload as a dictionary.
    def __get_message_payload(self):
        self.__decide_channel()
        return self.payload

    # use slack api to send message 
    def send_message(self, decide_message):
        slack_web_client = WebClient(self.token)
        self.decide_message(decide_message)
        self.__decide_bot_icon(self.bot_icon)
        message = self.__get_message_payload()
        slack_web_client.chat_postMessage(**message)

    # use slack api to send picture's url as picture message
    def send_picture_as_message(self, decide_picture_as_message):
        slack_web_client = WebClient(self.token)
        self.__decide_bot_icon(self.bot_icon)
        self.decide_picture_as_message(decide_picture_as_message)
        message = self.__get_message_payload()
        slack_web_client.chat_postMessage(**message)


def get_cats_api_image(cats_api_token):
    """Query Cats API for image.

    cats_api_token: (str) API token
    returns cat_url: (str) URL of cat image from API
    """
    cat_url = None
    if not cats_api_token:
        print('cats_api_token is NULL')
        return cat_url
    base_url = 'https://api.thecatapi.com/v1/images/search'
    headers = {'x-api-key': cats_api_token}
    params = {'size': 'small', 'order': 'RANDOM', 'limit': 1}
    try:
        req = requests.get(base_url, params=params, headers=headers)
    except Exception as err:
        print(f'cats API request failed:\t{err}')
        return cat_url
    if req.status_code != requests.status_codes.codes.ALL_OK:
        print(f'cats API returned unexpected status ({req.status_code})')
        return cat_url
    payload = req.json()
    if payload:
        cat_url = payload[0]['url']
    else:
        print('nothing returned from cats API')
    return cat_url
