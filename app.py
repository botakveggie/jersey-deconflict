import pymongo
from flask import Flask, request
import telegram
from credentials import bot_token, bot_user_name,URL

TOKEN = bot_token
bot = telegram.Bot(token=TOKEN)
app = Flask(__name__)
