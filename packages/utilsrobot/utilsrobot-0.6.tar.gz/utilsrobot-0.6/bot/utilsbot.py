import os
import telethon
import requests
from bot.config import Config
import functools
from telethon.errors import BadRequestError
from telethon.tl.functions.channels import EditAdminRequest, EditBannedRequest
from telethon.tl.functions.messages import UpdatePinnedMessageRequest
from telethon.tl.types import ChatAdminRights,ChatBannedRights,MessageEntityMentionName
from telethon import TelegramClient, events, functions, Button

#==================================================

bot = TelegramClient("bot", api_id=Config.API_ID, api_hash=Config.API_HASH)
utilsbot = bot.start(bot_token=Config.BOT_TOKEN)

#==================================================
def callback(sed):
    def callbacks(func):
        data = sed
        utilsbot.add_event_handler(
            func, events.callbackquery.CallbackQuery(data=data)
        )

    return callbacks

def cmd(add_cmd, is_args=False):
    def acmd(func):
        if is_args :
        	pattern = "^/" + add_cmd + "(?: |$)(.*)"
        elif is_args== "simple" :
            pattern = "^/" + add_cmd + " ?(.*)"
        elif is_args=="normal":
            pattern = "^/" + add_cmd
        else:
            pattern = "^/" + add_cmd + "$"
        utilsbot.add_event_handler(
            func, events.NewMessage(incoming=True, pattern=pattern)
        )
    return acmd

def inline():
    def ainline(func):
        utilsbot.add_event_handler(func, events.InlineQuery)
    return ainline

def is_admin():
    def decorator(func):
        @functools.wraps(func)
        async def wrapper(event):
            sed = await adminbot.get_permissions(event.chat_id, event.sender_id)
            user = event.sender_id
            if sed.is_admin:
                await func(event)
            if not user:
                pass
            if not sed.is_admin:
                await event.reply("Only Admins Can Use it.")
        return wrapper
    return decorator


def is_bot_admin():
    def decorator(func):
        @functools.wraps(func)
        async def wrapper(event):
            pep = await adminbot.get_me()
            sed = await adminbot.get_permissions(event.chat_id, pep)
            if sed.is_admin:
                await func(event)
            else:
                await event.reply("I Must Be Admin To Do This.")
        return wrapper
    return decorator


def only_groups():
    def decorator(func):
        @functools.wraps(func)
        async def wrapper(event):
            if event.is_group:
                await func(event)
            else:
                await event.reply("This Command Only Works On Groups.")
        return wrapper
    return decorator

def only_pm():
    def decorator(func):
        @functools.wraps(func)
        async def wrapper(event):
            if event.is_group:
                pass
            else:
                await func(event)

        return wrapper

    return decorator
#==================================================

is_admin = is_admin()
is_bot_admin = is_bot_admin()
only_groups = only_groups()
only_pm = only_pm()

# =================== CONSTANT ===================