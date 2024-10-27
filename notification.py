import sqlite3
import time
import requests
import threading
import config
from melipayamak import Api
from telethon.sync import TelegramClient, Button
import asyncio


# تنظیمات تلگرام
TELEGRAM_API_URL = f"https://api.telegram.org/bot{config.BOT_TOKEN}/sendMessage"

# لیست ادمین‌ها
ADMINS_LIST = config.ADMINS_LIST
cli = TelegramClient("cli-not", config.API_ID, config.API_HASH)
cli.start(bot_token=config.BOT_TOKEN)
async def send_telegram_message(chat_id, text, username):
    # payload = {
    #     'chat_id': chat_id,
    #     'text': text,
    #     'parse_mode': 'HTML'
    # }
    # requests.post(TELEGRAM_API_URL, data=payload)
    url = f"{config.API_ADDRESS}client-info?username={username}"
    response = requests.get(url=url)
    response = response.json()
    keys = [
        [Button.inline("نام"), Button.inline(username)],
        [Button.inline("انقضا"), Button.inline(response["info"]["expire_date"])],
        [
            Button.inline("مصرف کلی"), Button.inline(response["info"]["used_traffic"])
        ],
        [
            Button.inline("پسورد"), Button.inline(response["info"]["password"])
        ]
    ]
    await cli.send_message(chat_id, text, buttons=keys)
def check_services():
    loop = asyncio.get_event_loop()
    conn = sqlite3.connect('bot.db')  # نام دیتابیس خود را اینجا قرار دهید
    cursor = conn.cursor()

    while True:
        cursor.execute("SELECT username, user_id, end, random_num, send_notification FROM services")
        services = cursor.fetchall()
        print(services)
        current_time = time.time()

        for username, user_id, end, random_num, send_notification in services:
            if end is None:
                continue
            if send_notification is None:
                continue
            else:
                if send_notification:
                    continue
            
            if current_time > end:
                # ارسال پیام به کاربر
                user_message = f"""❗️ پایان اشتراک {username}
📍 حجم یا تاریخ اعتبار این اشتراک به پایان رسیده است و این اشتراک به صورت خودکار غیرفعال گردیده است!

اطلاعات سرویس شما به شرح زیر است:👇 
"""
                loop.run_until_complete(send_telegram_message(user_id, user_message, username=username))
                cursor.execute(f"UPDATE services SET send_notification = {True} WHERE random_num = {random_num}")
                conn.commit()
                username_sms = config.sms_username
                password_sms = config.sms_password
                api = Api(username_sms,password_sms)
                sms_soap = api.sms('soap')
                to = cursor.execute(f"SELECT phone FROM users WHERE user_id = {user_id}").fetchone()[0]
                print(to)
                test = sms_soap.send_by_base_number(f"{username}", to, 239809)
                print(test)
                # ارسال پیام به ادمین‌ها
                admin_message = f"ادمین گرامی، بیش از 90 درصد از اعتبار سرویس با نام کاربری {username} مصرف شده است\nآیدی عددی کاربر: {user_id}"
                for admin_id in ADMINS_LIST:
                    loop.run_until_complete(send_telegram_message(admin_id, admin_message, username=username))

        time.sleep(60)  # هر 1 دقیقه چک کند

check_services()