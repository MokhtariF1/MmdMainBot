import sqlite3
import time
import requests
import threading
import config
from melipayamak import Api
from telethon import TelegramClient, Button

# تنظیمات تلگرام
TELEGRAM_API_URL = f"https://api.telegram.org/bot{config.BOT_TOKEN}/sendMessage"

# لیست ادمین‌ها
ADMINS_LIST = config.ADMINS_LIST
async def send_telegram_message(chat_id, text, ex, username):
    # payload = {
    #     'chat_id': chat_id,
    #     'text': text,
    #     'parse_mode': 'HTML'
    # }
    # requests.post(TELEGRAM_API_URL, data=payload)
    keys = None
    if ex:
        keys = [
            Button.inline("🔋تمدید اشتراک", data=str.encode("sr_inf:" + str(username)))
        ]
    cli = TelegramClient("cli", config.API_ID, config.API_HASH)
    cli.start(bot_token=config.BOT_TOKEN)
    await cli.send_message(chat_id, text, buttons=keys)
    await cli.disconnect()
async def check_services():
    conn = sqlite3.connect('bot.db')  # نام دیتابیس خود را اینجا قرار دهید
    cursor = conn.cursor()

    while True:
        cursor.execute("SELECT username, user_id, end, send_notification FROM test_account")
        services = cursor.fetchall()
        print(services)
        current_time = time.time()

        for username, user_id, end, send_notification in services:
            if end is None:
                continue
            if send_notification is None:
                continue
            else:
                if send_notification:
                    continue
            if current_time > end:
                # ارسال پیام به کاربر
                user_message = f"""❗️ پایان اشتراک تست{username}
📍 حجم یا تاریخ اعتبار این اشتراک به پایان رسیده است و این اشتراک به صورت خودکار غیرفعال گردیده است!

♻️ جهت فعالسازی مجدد اشتراک خود از دکمه زیر  اقدام به مشاهده اشتراک خود کنید.

❌ در صورت عدم تمدید اشتراک 3 روز پس از پایان مدت اعتبار اشتراک به صورت خودکار توسط ربات حذف خواهد شد
"""
                await send_telegram_message(user_id, user_message, True, username=username)
                cursor.execute(f"UPDATE test_account SET send_notification = {True} WHERE username = '{username}'")
                conn.commit()
                # ارسال پیام به ادمین‌ها
                admin_message = f"ادمین گرامی، بیش از 90 درصد از اعتبار سرویس با نام کاربری {username} مصرف شده است\nآیدی عددی کاربر: {user_id}"
                for admin_id in ADMINS_LIST:
                    await send_telegram_message(admin_id, admin_message, ex=False, username=username)

        time.sleep(60)  # هر 1 دقیقه چک کند

if __name__ == "__main__":
    service_checker_thread = threading.Thread(target=check_services)
    service_checker_thread.start()
