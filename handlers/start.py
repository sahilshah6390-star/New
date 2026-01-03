# handlers/start.py

import asyncio
from pyrogram import filters
from pyrogram.enums import ChatAction, ChatMemberStatus
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from app.client import app
from config import (
    FORCE_CHANNEL,
    FORCE_GROUP,
    START_PIC,
    FORCE_PIC,
    OWNER_USERNAME
)
from database.users import track_user


START_MSG = """<b>›› Hey {mention}</b>

Welcome to <b>Kasukabe Hosting Panel</b> 🚀

Upload and host your bots safely.
"""


async def is_joined(client, user_id: int) -> bool:
    try:
        ch = await client.get_chat_member(FORCE_CHANNEL, user_id)
        gp = await client.get_chat_member(FORCE_GROUP, user_id)

        return (
            ch.status in (ChatMemberStatus.MEMBER, ChatMemberStatus.ADMINISTRATOR, ChatMemberStatus.OWNER)
            and
            gp.status in (ChatMemberStatus.MEMBER, ChatMemberStatus.ADMINISTRATOR, ChatMemberStatus.OWNER)
        )
    except:
        return False


def force_kb():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("📢 Join Channel", url=f"https://t.me/{FORCE_CHANNEL}")],
        [InlineKeyboardButton("💬 Join Group", url=f"https://t.me/{FORCE_GROUP}")]
    ])


def home_kb():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("👑 Owner", url=f"https://t.me/{OWNER_USERNAME}")],
        [InlineKeyboardButton("❌ Close", callback_data="close")]
    ])


@app.on_message(filters.command("start") & filters.private)
async def start_cmd(client, message):
    track_user(message.from_user)

    chat_id = message.chat.id
    mention = message.from_user.mention

    await client.send_chat_action(chat_id, ChatAction.TYPING)
    await asyncio.sleep(0.5)

    if not await is_joined(client, message.from_user.id):
        await message.reply_photo(
            FORCE_PIC,
            caption="⚠️ <b>Please join channel & group to continue</b>",
            reply_markup=force_kb(),
            parse_mode="html"
        )
        return

    await message.reply_photo(
        START_PIC,
        caption=START_MSG.format(mention=mention),
        reply_markup=home_kb(),
        parse_mode="html"
    )


@app.on_callback_query(filters.regex("^close$"))
async def close_cb(client, query):
    await query.message.delete()