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
# add channel or user chat id
FROM = [int(i) for i in FROM_.split()]
TO = [int(i) for i in TO_.split()]

try:
    BotzHubUser = TelegramClient(StringSession(SESSION), APP_ID, API_HASH)
    BotzHubUser.start()
except Exception as ap:
    print(f"ERROR - {ap}")
    exit(1)

# Forward messages from user chats and channels to the specified destination channels
@BotzHubUser.on(events.NewMessage(chats=FROM))
async def forward_to_channels(event):
    if event.message.video:
        try:
            caption_text = event.message.caption
            for chat_id in TO:
                await BotzHubUser.send_file(chat_id, event.message.media, caption=caption_text)
                print(f"Video forwarded from {event.chat_id} to {chat_id}")
        except Exception as e:
            print(e)

print("Bot has started.")
BotzHubUser.run_until_disconnected()
