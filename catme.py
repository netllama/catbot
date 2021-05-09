import os

from slack_bot import SlackBot, get_cats_api_image

cats_api_token = os.environ.get('CAT_API_TOKEN')
slack_token = os.environ.get('SLACK_BOT_TOKEN')
slack_channel = '#llamatest'

def catme_bot_resp():
    """catme Bot should respond in channel.
    """
    bot_icon_url = ''
    cats_url = get_cats_api_image(cats_api_token)
    if not cats_url:
        return
    slack_bot = SlackBot(slack_channel, slack_token, bot_icon_url)
    slack_bot.send_picture_as_message(cats_url)
    #slack_bot.send_message(message)
