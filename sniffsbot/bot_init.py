import os

from dotenv import load_dotenv
from twitchio.client import Client
from twitchio.ext import commands


load_dotenv()


def bot_init():
    bot = commands.Bot(
        irc_token=os.environ['TMI_TOKEN'],
        client_id=os.environ['CLIENT_ID'],
        nick=os.environ['BOT_NICK'],
        prefix=os.environ['BOT_PREFIX'],
        initial_channels=[os.environ['CHANNEL']]
    )
    return bot, os.environ['BOT_NICK'], os.environ['CHANNEL']

def client_init():
    client = Client(
        client_id=os.environ['CLIENT_ID'],
        client_secret=os.environ['CLIENT_SECRET']
    )
    return client
