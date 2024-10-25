import sqlite3
import time
import requests
import threading
import config
from melipayamak import Api

# تنظیمات تلگرام
TELEGRAM_API_URL = f"https://api.telegram.org/bot{config.BOT_TOKEN}/sendMessage"

# لیست ادمین‌ها
ADMINS_LIST = config.ADMINS_LIST

def send_telegram_message(chat_id, text):
    payload = {
        'chat_id': chat_id,
        'text': text,
        'parse_mode': 'HTML'
    }
    response = requests.post(TELEGRAM_API_URL, data=payload)
    print(response)
def check_services():
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
                user_message = f"""یادآوری تمدید اشتراک کاربر گرامی؛ حساب کاربری {username} شما در حال اتمام اعتبار است و بیش از 90% از اعتبار آن مصرف شده است. هم اکنون برای تمدید اقدام کنید.
 kooll.online"""
                send_telegram_message(user_id, user_message)
                cursor.execute(f"UPDATE test_account SET send_notification = {True} WHERE username = '{username}'")
                conn.commit()
                # ارسال پیام به ادمین‌ها
                admin_message = f"ادمین گرامی، بیش از 90 درصد از اعتبار سرویس با نام کاربری {username} مصرف شده است\nآیدی عددی کاربر: {user_id}"
                for admin_id in ADMINS_LIST:
                    send_telegram_message(admin_id, admin_message)

        time.sleep(60)  # هر 1 دقیقه چک کند

if __name__ == "__main__":
    service_checker_thread = threading.Thread(target=check_services)
    service_checker_thread.start()
