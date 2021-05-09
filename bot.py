import os
import logging
import sys

from catme import catme_bot_resp
from slack_bot import SlackBot, get_cats_api_image
from slackeventsapi import SlackEventAdapter

slack_token = os.environ.get('SLACK_BOT_TOKEN')
slack_events_token = os.environ.get('SLACK_EVENTS_TOKEN')
cats_api_token = os.environ.get('CAT_API_TOKEN')
slack_events_adapter = SlackEventAdapter(slack_events_token, '/slack/events')

def setup_custom_logger(name):
    formatter = logging.Formatter(fmt='%(asctime)s %(levelname)-8s %(message)s',
                                  datefmt='%Y-%m-%d %H:%M:%S')
    screen_handler = logging.StreamHandler(stream=sys.stdout)
    screen_handler.setFormatter(formatter)
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)
    logger.addHandler(screen_handler)
    return logger


# When a 'message' event is detected by the events adapter, forward that payload
# to this function.
@slack_events_adapter.on('message')
def message(payload):
    """Parse the message event, and if the activation string is in the text,
    simulate a coin flip and send the result.
    """
    # Get the event data from the payload
    event = payload.get('event', {})

    # Get the text from the event that came through
    text = event.get('text')

    # Check and see if the activation phrase was in the text of the message.
    # If so, execute the code to flip a coin.
    if text.lower() == '!catme':
        logger.info(f'text = {text}')
        # Execute the cats API call and post image to channel
        catme_bot_resp()


if __name__ == '__main__':
    # setup logging
    logger = setup_custom_logger('mylogger')

    # verify required API tokens
    if not slack_token or not slack_events_token:
        msg = f'slack_token is NULL ({slack_token}) or slack_events_token is NULL ({slack_events_token})'
        logger.error(msg)
        sys.exit(1)

    # run the bot listener
    slack_events_adapter.start(port=5000)
