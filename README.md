# catbot
A slack bot which posts random cat pix to a specified slack channel when invoked with "!catme".

To use, first get a Cats API token from https://api.thecatapi.com .  
Next, create an app on https://api.slack.com/apps and obtain a 'Bot User OAuth Token' plus the 'Signing Secret' from the "App Credentials".

The Cats API token should be referenced via the CAT_API_TOKEN environment variable.
The 'Bot User OAuth Token' is associated with the SLACK_BOT_TOKEN environment variable.
The 'Signing Secret' is associated with the SLACK_EVENTS_TOKENenvironment variable.

In Slack's 'Event Subscriptions" you will need to provide a "Request URL" which points to the URL where you intend to run the bot, with a trailing "slack/events" URI (eg. https://example.com/slack/events".  The code expects to have port 5000 exposed, or a reverse proxy (using ngrok or similar) setup to send slack channel events to the bot.

Update the "slack_channel" variable on line 7 of catme.py to your desired slack channel, then run as follows:

SLACK_EVENTS_TOKEN='token' CAT_API_TOKEN='token' SLACK_BOT_TOKEN='token' python bot.py

Running "!catme" (without the quotes) in your slack channel should result in a cat image appearing within a second or two.
