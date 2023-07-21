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

# Remove forwarded tag from the message and forward from user chat to channel
@BotzHubUser.on(events.NewMessage(incoming=True, chats=FROM))
async def forward_userchat_to_channel(event):
    if event.message.video:
        try:
            for chat_id in TO:
                # Forward the message without the via_bot_id attribute
                await event.message.forward_to(chat_id)
                print(f"Video forwarded from user chat {event.chat_id} to channel {chat_id}")
        except Exception as e:
            print(e)

# Remove forwarded tag from the message and forward from channel to multiple channels
@BotzHubUser.on(events.NewMessage(incoming=True, chats=FROM))
async def forward_channel_to_channels(event):
    if event.message.video:
        try:
            for chat_id in TO:
                # Forward the message without the via_bot_id attribute
                await event.message.forward_to(chat_id)
                print(f"Video forwarded from channel {event.chat_id} to channel {chat_id}")
        except Exception as e:
            print(e)

print("Bot has started.")
BotzHubUser.run_until_disconnected()
