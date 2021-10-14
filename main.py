# Made with python3
# (C) @FayasNoushad
# Copyright permission under MIT License
# All rights reserved by FayasNoushad
# License -> https://github.com/FayasNoushad/Telegraph-Uploader-Bot-V2/blob/main/LICENSE

import os
import time
import math
import json
import string
import random
import traceback
import asyncio
import datetime
import aiofiles
from random import choice 
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from pyrogram.errors import FloodWait, InputUserDeactivated, UserIsBlocked, PeerIdInvalid, UserNotParticipant, UserBannedInChannel
from pyrogram.errors.exceptions.bad_request_400 import PeerIdInvalid
from telegraph import upload_file
from database import Database


UPDATE_CHANNEL = os.environ.get("UPDATE_CHANNEL", "")
BOT_OWNER = int(os.environ["BOT_OWNER"])
DATABASE_URL = os.environ["DATABASE_URL"]
db = Database(DATABASE_URL, "FnTelegraphBot")

Bot = Client(
    "Telegraph Uploader Bot",
    bot_token = os.environ["BOT_TOKEN"],
    api_id = int(os.environ["API_ID"]),
    api_hash = os.environ["API_HASH"],
)

START_TEXT = """**Hello {} 😌
𝙄 𝘼𝙈 𝙎𝙈𝘼𝙇𝙇 𝙈𝙀𝘿𝙄𝘼 𝙊𝙍 𝙁𝙄𝙇𝙀 𝙏𝙊 𝙏𝙀𝙇𝙀𝙂𝙍𝘼.𝙋𝙃 𝙇𝙄𝙉𝙆 𝙐𝙋𝙇𝙊𝘿𝙀𝙍 𝘽𝙊𝙏😊..**

>> `𝐈 𝐜𝐚𝐧 𝐜𝐨𝐧𝐯𝐞𝐫𝐭 𝐔𝐧𝐝𝐞𝐫 5𝐌𝐁 𝐩𝐡𝐨𝐭𝐨 𝐎𝐫 𝐕𝐢𝐝𝐞𝐨 𝐓𝐨 𝐓𝐞𝐥𝐞𝐠𝐫𝐚𝐩𝐡 𝐥𝐢𝐧𝐤...`

Made by @AD_BOTZ_2"""

HELP_TEXT = """**𝙃𝙚𝙮,𝙁𝙤𝙡𝙡𝙤𝙬 𝙏𝙝𝙚𝙨𝙚 𝙎𝙩𝙖𝙥𝙨😊:**

➠ 𝗝𝘂𝘀𝘁 𝗚𝗶𝘃𝗲 𝗠𝗲 𝗮 𝗠𝗲𝗱𝗶𝗮 𝗨𝗻𝗱𝗲𝗿 5𝗠𝗕🥰
➠ 𝗧𝗵𝗲𝗻 𝗜 𝘄𝗶𝗹𝗹 𝗗𝗼𝘄𝗻𝗹𝗼𝗮𝗱 𝗜𝘁🥰
➠ 𝗜 𝘄𝗶𝗹𝗹 𝗧𝗵𝗲𝗻 𝗨𝗽𝗹𝗼𝗮𝗱 𝗜𝘁 𝗧𝗼 𝗧𝗵𝗲 𝗧𝗲𝗹𝗲𝗴𝗿𝗮.𝗽𝗵 𝗟𝗶𝗻𝗸🥰

**😁𝙰𝚟𝚊𝚕𝚒𝚊𝚋𝚕𝚎 𝙲𝚘𝚖𝚖𝚊𝚗𝚍𝚜😁**

/start - 𝙲𝚑𝚎𝚌𝚔𝚒𝚗𝚐 𝙱𝚘𝚝 𝙾𝚗𝚕𝚒𝚗𝚎😇
/help - 𝙵𝚘𝚛 𝙼𝚘𝚛𝚎 𝙷𝚎𝚕𝚙❤️
/about - 𝙵𝚘𝚛 𝙼𝚘𝚛𝚎 𝙰𝚋𝚘𝚞𝚝😉
/status - 𝙵𝚘𝚛 𝙱𝚘𝚝 𝚄𝚙𝚍𝚊𝚝𝚎𝚜⚒️

Made by @AD_BOTZ_2"""

ABOUT_TEXT = """--**About Me**-- 😎

🤖 **Name :** [Telegraph Uploader](https://telegram.me/{})

👨‍💻 **Developer :** [Fayas](https://github.com/LuciferMoringStarDevil)

👨‍💻 **Editor :** [Muhammed](https://github.com/LuciferMoringStarDevil)

📢 **Channel :** [Mo Tech Channel](https://telegram.me/AD_BOTZ_2)

👥 **Group :** [Mo Tech Group](https://telegram.me/AD_BOTZ)

🌐 **Source :** [👉 Click here](https://github.com/LuciferMoringStarDevil/Telegraph-Uploader-Bot-V2)

📝 **Language :** [Python3](https://python.org)

🧰 **Framework :** [Pyrogram](https://pyrogram.org)

📡 **Server :** [Heroku](https://heroku.com)"""

FORCE_SUBSCRIBE_TEXT = "<code>Sorry Dear You Must Join My Updates Channel for using me 😌😉....</code>"

START_BUTTONS = InlineKeyboardMarkup(
        [[
        InlineKeyboardButton('🎬 For Movie 🎬', url='https://t.me/ADMOVEIAD'),
        ],[
        InlineKeyboardButton('⚙ Help ⚙', callback_data='help'),
        InlineKeyboardButton('🔰 About 🔰', callback_data='about'),
        InlineKeyboardButton('✖️ Close ✖️', callback_data='close')
        ]]
    )

HELP_BUTTONS = InlineKeyboardMarkup(
        [[
        InlineKeyboardButton('⚒️ More Botz ⚒️', url='https://t.me/AD_BOTZ_2'),
        ],[
        InlineKeyboardButton('🏘 Home 🏘', callback_data='home'),
        InlineKeyboardButton('🔰 About 🔰', callback_data='about'),
        InlineKeyboardButton('✖️ Close ✖️', callback_data='close')
        ]]
    )

ABOUT_BUTTONS = InlineKeyboardMarkup(
        [[
        InlineKeyboardButton('💠 Sapport Group 💠', url='https://t.me/AD_BOTZ'),      ],[
        InlineKeyboardButton('🏘 Home', callback_data='home'),
        InlineKeyboardButton('Help ⚙', callback_data='help'),
        InlineKeyboardButton('Close ✖️', callback_data='close')
        ]]
    )


async def send_msg(user_id, message):
	try:
		await message.copy(chat_id=user_id)
		return 200, None
	except FloodWait as e:
		await asyncio.sleep(e.x)
		return send_msg(user_id, message)
	except InputUserDeactivated:
		return 400, f"{user_id} : deactivated\n"
	except UserIsBlocked:
		return 400, f"{user_id} : user is blocked\n"
	except PeerIdInvalid:
		return 400, f"{user_id} : user id invalid\n"
	except Exception as e:
		return 500, f"{user_id} : {traceback.format_exc()}\n"


@Bot.on_callback_query()
async def cb_handler(bot, update):
    if update.data == "home":
        await update.message.edit_text(
            text=START_TEXT.format(update.from_user.mention),
            reply_markup=START_BUTTONS,
            disable_web_page_preview=True
        )
    elif update.data == "help":
        await update.message.edit_text(
            text=HELP_TEXT,
            reply_markup=HELP_BUTTONS,
            disable_web_page_preview=True
        )
    elif update.data == "about":
        await update.message.edit_text(
            text=ABOUT_TEXT.format((await bot.get_me()).username),
            reply_markup=ABOUT_BUTTONS,
            disable_web_page_preview=True
        )
    else:
        await update.message.delete()


@Bot.on_message(filters.private & filters.command(["start"]))
async def start(bot, update):
    if not await db.is_user_exist(update.from_user.id):
	    await db.add_user(update.from_user.id)
    await update.reply_text(
        text=START_TEXT.format(update.from_user.mention),
        disable_web_page_preview=True,
	reply_markup=START_BUTTONS
    )


@Bot.on_message(filters.private & filters.command(["help"]))
async def help(bot, update):
    if not await db.is_user_exist(update.from_user.id):
	    await db.add_user(update.from_user.id)
    await update.reply_text(
        text=HELP_TEXT,
      	disable_web_page_preview=True,
	reply_markup=HELP_BUTTONS
    )


@Bot.on_message(filters.private & filters.command(["about"]))
async def about(bot, update):
    if not await db.is_user_exist(update.from_user.id):
	    await db.add_user(update.from_user.id)
    await update.reply_text(
        text=ABOUT_TEXT.format((await bot.get_me()).username),
        disable_web_page_preview=True,
	reply_markup=ABOUT_BUTTONS
    )


@Bot.on_message(filters.media & filters.private)
async def telegraph_upload(bot, update):
    if not await db.is_user_exist(update.from_user.id):
	    await db.add_user(update.from_user.id)
    if UPDATE_CHANNEL:
        try:
            user = await bot.get_chat_member(UPDATE_CHANNEL, update.chat.id)
            if user.status == "kicked":
                await update.reply_text(text="You are banned!")
                return
        except UserNotParticipant:
            await update.reply_text(
		  text=FORCE_SUBSCRIBE_TEXT,
		  reply_markup=InlineKeyboardMarkup(
			  [[InlineKeyboardButton(text="⚙ Join Updates Channel ⚙", url=f"https://telegram.me/{UPDATE_CHANNEL}")]]
		  )
	    )
            return
        except Exception as error:
            print(error)
            await update.reply_text(text="Something wrong. Contact <a href='https://telegram.me/TheFayas'>Developer</a>.", disable_web_page_preview=True)
            return
    medianame = "./DOWNLOADS/" + "FayasNoushad/FnTelegraphBot"
    text = await update.reply_text(
        text="<code>Downloading to My Server ...</code>",
        disable_web_page_preview=True
    )
    await bot.download_media(
        message=update,
        file_name=medianame
    )
    await text.edit_text(
        text="<code>Downloading Completed. Now I am Uploading to telegra.ph Link ...</code>",
        disable_web_page_preview=True
    )
    try:
        response = upload_file(medianame)
    except Exception as error:
        print(error)
        await text.edit_text(
            text=f"Error :- {error}",
            disable_web_page_preview=True
        )
        return
    try:
        os.remove(medianame)
    except Exception as error:
        print(error)
        return
    await text.edit_text(
        text=f"<b>Link :-</b> <code>https://telegra.ph{response[0]}</code>\n\n<b>Join :-</b> @AD_BOTZ",
        disable_web_page_preview=True,
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(text="Open Link", url=f"https://telegra.ph{response[0]}"),
                    InlineKeyboardButton(text="Share Link", url=f"https://telegram.me/share/url?url=https://telegra.ph{response[0]}")
                ],
                [  
                    InlineKeyboardButton(text="⚙ Join Updates Channel ⚙", url="https://t.me/AD_BOTZ")
                ],
                [
                    InlineKeyboardButton('🎬 For Moviea 🎬', url='https://t.me/ADMOVEIAD')
                ]
            ]
        )
    )


@Bot.on_message(filters.private & filters.command("broadcast") & filters.user(BOT_OWNER) & filters.reply)
async def broadcast(bot, update):
	broadcast_ids = {}
	all_users = await db.get_all_users()
	broadcast_msg = update.reply_to_message
	while True:
	    broadcast_id = ''.join([random.choice(string.ascii_letters) for i in range(3)])
	    if not broadcast_ids.get(broadcast_id):
	        break
	out = await update.reply_text(text=f"Broadcast Started! You will be notified with log file when all the users are notified.")
	start_time = time.time()
	total_users = await db.total_users_count()
	done = 0
	failed = 0
	success = 0
	broadcast_ids[broadcast_id] = dict(total = total_users, current = done, failed = failed, success = success)
	async with aiofiles.open('broadcast.txt', 'w') as broadcast_log_file:
	    async for user in all_users:
	        sts, msg = await send_msg(user_id = int(user['id']), message = broadcast_msg)
	        if msg is not None:
	            await broadcast_log_file.write(msg)
	        if sts == 200:
	            success += 1
	        else:
	            failed += 1
	        if sts == 400:
	            await db.delete_user(user['id'])
	        done += 1
	        if broadcast_ids.get(broadcast_id) is None:
	            break
	        else:
	            broadcast_ids[broadcast_id].update(dict(current = done, failed = failed, success = success))
	if broadcast_ids.get(broadcast_id):
	    broadcast_ids.pop(broadcast_id)
	completed_in = datetime.timedelta(seconds=int(time.time()-start_time))
	await asyncio.sleep(3)
	await out.delete()
	if failed == 0:
	    await update.reply_text(text=f"broadcast completed in `{completed_in}`\n\nTotal users {total_users}.\nTotal done {done}, {success} success and {failed} failed.", quote=True)
	else:
	    await update.reply_document(document='broadcast.txt', caption=f"broadcast completed in `{completed_in}`\n\nTotal users {total_users}.\nTotal done {done}, {success} success and {failed} failed.")
	os.remove('broadcast.txt')


@Bot.on_message(filters.private & filters.command("status"), group=5)
async def status(bot, update):
    total_users = await db.total_users_count()
    text = "**Bot Status**\n"
    text += f"\n**Total Users:** `{total_users}`"
    await update.reply_text(
        text=text,
        quote=True,
        disable_web_page_preview=True
    )


Bot.run()
