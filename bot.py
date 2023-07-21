from telethon import TelegramClient, events
from decouple import config
import logging
from telethon.sessions import StringSession

logging.basicConfig(format='[%(levelname) 5s/%(asctime)s] %(name)s: %(message)s', level=logging.INFO)

print("Starting...")
# get your own values from my.telegram.org
APP_ID = config("APP_ID", default=None, cast=int)
API_HASH = config("API_HASH", default=None)
SESSION = config("SESSION")
FROM_ = config("FROM_CHANNEL")
TO_ = config("TO_CHANNEL")
# add channel or userchat id
FROM = [int(i) for i in FROM_.split()]
TO = [int(i) for i in TO_.split()]

try:
    BotzHubUser = TelegramClient(StringSession(SESSION), APP_ID, API_HASH)
    BotzHubUser.start()
except Exception as ap:
    print(f"ERROR - {ap}")
    exit(1)

# Add forward from user chat to channel by using the forward_messages method
@BotzHubUser.on(events.NewMessage(incoming=True, chats=FROM))
async def forward_userchat_to_channel(event):
    if event.message.video:
        try:
            await BotzHubUser.forward_messages(TO, event.message)
            print(f"Video forwarded from user chat {event.chat_id} to channels: {TO}")
        except Exception as e:
            print(e)

# Add forward from channel to multiple channels using the forward_messages method
@BotzHubUser.on(events.NewMessage(incoming=True, chats=FROM))
async def forward_channel_to_channels(event):
    if event.message.video:
        try:
            await BotzHubUser.forward_messages(TO, event.message)
            print(f"Video forwarded from channel {event.chat_id} to channels: {TO}")
        except Exception as e:
            print(e)

print("Bot has started.")
BotzHubUser.run_until_disconnected()
