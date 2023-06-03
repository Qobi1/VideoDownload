import os
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import CallbackContext
from .models import User
import requests
from VideoDownloaderBot.settings import BOT_LINK
from urllib.request import urlretrieve
# Create your views here.


async def start(update: Update, context: CallbackContext):
    user = update.effective_user
    client = User.objects.filter(user_id=user.id).first()
    if client is None:
        User.objects.create(user_id=user.id)
    await update.message.reply_text(f"Hello {user.first_name}, you can download videos from Instagram, TikTok and Youtube")
    await update.message.reply_text("Send me, link of the video")


async def url_handler(update: Update, context: CallbackContext):
    link = update.message.text
    user = update.effective_user
    client = User.objects.filter(user_id=user.id).first()
    if client is None:
        User.objects.create(user_id=user.id)
        client = User.objects.filter(user_id=user.id).first()

    # if link.startswith("https://www.youtube.com/"):
    #     url = "https://ytstream-download-youtube-videos.p.rapidapi.com/dl"
    #     querystring = {"id": "rs6Y4kZ8qtw"}
    #
    #     headers = {
    #         "X-RapidAPI-Key": "7154b8b10cmsh42f4e5b4559e2fbp162f43jsnd9ea670b0349",
    #         "X-RapidAPI-Host": "ytstream-download-youtube-videos.p.rapidapi.com"
    #     }
    #
    #     response = requests.get(url, headers=headers, params=querystring)
    #     l = []
    #     for i in response.json()['formats']:
    #         l.append(i)
    #
    #     for i in response.json()['adaptiveFormats']:
    #         l.append(i)
    #     print(l)
    #     await update.message.reply_text("Choose one", reply_markup=btn(user, list=l, type='YouTube'))

    if link.startswith("https://www.instagram.com/"):
        pass
    elif link.startswith("https://www.tiktok.com/"):
        User.objects.filter(user_id=user.id).update(state=2)
        url = "https://tiktok-full-info-without-watermark.p.rapidapi.com/vid/index"

        querystring = {"url": link}

        headers = {
            "X-RapidAPI-Key": "7154b8b10cmsh42f4e5b4559e2fbp162f43jsnd9ea670b0349",
            "X-RapidAPI-Host": "tiktok-full-info-without-watermark.p.rapidapi.com"
        }

        response = requests.get(url, headers=headers, params=querystring)
        urlretrieve(response.json()['video'][0], f'media/{user.id}.mp4')
        try:
            await context.bot.send_video(user.id, video=open(f'media/{user.id}.mp4', 'rb'), read_timeout=10000, reply_markup=btn(user, 'TikTok'), supports_streaming=True)
            os.remove(f'media/{user.id}.mp4')
        except Exception as e:
            print(e)
            os.remove(f'media/{user.id}.mp4')
            await update.message.reply_text('Ooops, an error occurred, Try again')
    else:
        await update.message.reply_text('❌Something went wrong. Try again')


async def inline_handler(update: Update, context: CallbackContext):
    user = update.effective_user
    client = User.objects.filter(user_id=user.id).first()
    query = update.callback_query
    if client.state == 2:
        urlretrieve(query.data, f'media/{query.data}.mp4')
        await context.bot.send_video(user.id, video=open(f'{query.data}.mp4', 'rb'))


def btn(user, type):
    btn = []
    if type == 'TikTok':
       btn = [[InlineKeyboardButton('Share', url=f"https://telegram.me/share/url?url={BOT_LINK}?start={user.id}")]]

    return InlineKeyboardMarkup(btn)


