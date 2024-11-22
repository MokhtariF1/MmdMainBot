import os
from calendar import month

from telethon import TelegramClient, events, Button

from datetime import datetime, timedelta

from telethon.tl.functions.channels import GetFullChannelRequest

import config

from sqlite3 import connect

import requests

from random import randint

from datetime import datetime

from config import iphone_plan_names
from functions import get_iphone_service
from melipayamak import Api

import jdatetime

import time

import pytz

import functions



if config.PROXY is False:

    proxy = None

else:

    proxy = ("socks5", "127.0.0.1", 2080)

print("connecting...")

bot = TelegramClient("bot", config.API_ID, config.API_HASH, proxy=proxy)

bot.start(bot_token=config.BOT_TOKEN)

print("connected!")



db = connect("bot.db")

cur = db.cursor()

bot_text = config.TEXT

back = Button.text(bot_text["back"], resize=1)

home_keys = [
    [

        Button.text(bot_text["test_account"]),

    ],

    [

        Button.text(bot_text["new_service"]),
        Button.text(bot_text["service_extension"]),
    ],


    [

        Button.text(bot_text["wallet"]),
        Button.text(bot_text["my_services"]),

    ],

    [

        Button.text(bot_text["get_buy"]),

        Button.text(bot_text["account"]),

    ],

    [
        Button.text(bot_text["download_app"]),

    ]

]

admin_keys = [

    [

        Button.text(bot_text["test_account"]),

    ],

    [

        Button.text(bot_text["new_service"]),
        Button.text(bot_text["service_extension"]),
    ],


    [

        Button.text(bot_text["wallet"]),
        Button.text(bot_text["my_services"]),

    ],

    [


        Button.text(bot_text["account"]),
        Button.text(bot_text["get_buy"]),

    ],

    [
        Button.text(bot_text["download_app"]),

    ],
    [

        Button.text(bot_text["panel"]),

    ],

]

@bot.on(events.NewMessage(pattern="/start", incoming=True))

async def start(event):
    print("/start")
    user_id = event.sender_id

    join, entity = await config.join_check(user_id, bot)

    if join is False:

        full_info = await bot(GetFullChannelRequest(entity))

        chat_title = full_info.chats[0].title

        channel_username = full_info.chats[0].username

        if channel_username is None:

            channel_username = full_info.full_chat.exported_invite.link

        else:

            channel_username = f'https://t.me/{channel_username}'

        key = [

            [Button.url(text=chat_title, url=channel_username)],

            [Button.url(bot_text["Membership_Confirmation"], url=f"{config.BOT_ID}?start=check")]

        ]

        await event.reply(bot_text["pls_join"], buttons=key)

        return

    if config.lock_bot == 1:

        if user_id not in config.ADMINS_LIST:

            find_user = cur.execute(f"SELECT * FROM users WHERE user_id = {user_id}").fetchone()

            if find_user is None:

                access_code = randint(100, 999)

                data = (user_id, 0, None, False, False, access_code, False)

                cur.execute(f"INSERT INTO users VALUES (?,?,?,?,?,?,?)", data)

                db.commit()

                await event.reply(bot_text["access_code"].format(access_code=access_code))

            else:

                is_ban = config.is_ban(user_id)

                if is_ban:

                    await event.reply(bot_text["you_banned"])

                    return

                user = cur.execute(f"SELECT * FROM users WHERE user_id = {user_id}").fetchone()

                if user[2] is None:

                    keys = [

                        [

                            Button.request_phone(bot_text["phone_share"], resize=1)

                        ],

                        [

                            Button.text(bot_text["back"])

                        ]

                    ]

                    await event.reply(bot_text["select"], buttons=keys)

                    return

                user_access = find_user[6]

                access_code = find_user[5]

                if user_access:

                    await event.reply(bot_text["select"], buttons=home_keys)

                else:

                    await event.reply(bot_text["access_code"].format(access_code=access_code))

        else:

            find_user = cur.execute(f"SELECT * FROM users WHERE user_id = {user_id}").fetchone()

            if find_user is None:

                access_code = randint(100, 999)

                data = (user_id, 0, None, False, False, access_code, True)

                cur.execute(f"INSERT INTO users VALUES (?,?,?,?,?,?,?)", data)

                db.commit()

                user = cur.execute(f"SELECT * FROM users WHERE user_id = {user_id}").fetchone()

                if user[2] is None:

                    keys = [

                        [

                            Button.request_phone(bot_text["phone_share"], resize=1)

                        ],

                        [

                            Button.text(bot_text["back"])

                        ]

                    ]

                    await event.reply(bot_text["select"], buttons=keys)

                    return

                await event.reply(bot_text["select"], buttons=admin_keys)

            else:

                user = cur.execute(f"SELECT * FROM users WHERE user_id = {user_id}").fetchone()

                if user[2] is None:

                    keys = [

                        [

                            Button.request_phone(bot_text["phone_share"], resize=1)

                        ],

                        [

                            Button.text(bot_text["back"])

                        ]

                    ]

                    await event.reply(bot_text["select"], buttons=keys)

                    return

                await event.reply(bot_text["select"], buttons=admin_keys)

    else:

        find_user = cur.execute(f"SELECT * FROM users WHERE user_id = {user_id}").fetchone()

        if find_user is None:

            access_code = randint(100, 999)

            data = (user_id, 0, None, False, False, access_code, True)

            cur.execute(f"INSERT INTO users VALUES (?,?,?,?,?,?,?)", data)

            db.commit()

            user = cur.execute(f"SELECT * FROM users WHERE user_id = {user_id}").fetchone()

            if user[2] is None:

                keys = [
                    [

                        Button.request_phone(bot_text["phone_share"], resize=1)

                    ],

                    [

                        Button.text(bot_text["back"])

                    ]

                ]

                await event.reply(bot_text["select"], buttons=keys)

                return

            if user_id in config.ADMINS_LIST:

                await event.reply(bot_text["select"], buttons=admin_keys)

            else:

                await event.reply(bot_text["select"], buttons=home_keys)

        else:

            user = cur.execute(f"SELECT * FROM users WHERE user_id = {user_id}").fetchone()

            if user[2] is None:

                keys = [

                    [

                        Button.request_phone(bot_text["phone_share"], resize=1)

                    ],

                    [

                        Button.text(bot_text["back"])

                    ]

                ]

                await event.reply(bot_text["select"], buttons=keys)

                return

            if user_id in config.ADMINS_LIST:

                await event.reply(bot_text["select"], buttons=admin_keys)

            else:

                await event.reply(bot_text["select"], buttons=home_keys)

@bot.on(events.NewMessage(incoming=True))
async def message(event):

    user_id = event.sender_id

    is_ban = config.is_ban(user_id)

    if is_ban:

        await event.reply(bot_text["you_banned"])

        return

    try:

        phone_number = event.original_update.message.media.phone_number

        user = find_user = cur.execute(f"SELECT * FROM users WHERE user_id = {user_id}").fetchone()

        if user is not None:

            if user[2] is None:

                if config.is_iran_phone_number(phone_number=phone_number):

                    cur.execute(f"UPDATE users SET phone = {phone_number} WHERE user_id = {user_id}")

                    db.commit()

                    await event.reply(bot_text["phone_ok"], buttons=back)

                else:

                    await event.reply(bot_text["phone_no"], buttons=back)

    except AttributeError:

        pass

    user = cur.execute(f"SELECT * FROM users WHERE user_id = {user_id}").fetchone()
    if user is not None:
        if user[2] is None:

            keys = [

                [

                    Button.request_phone(bot_text["phone_share"], resize=1)

                ],

                [

                    Button.text(bot_text["back"])

                ]

            ]

            await event.reply(bot_text["select"], buttons=keys)

            return

    text = event.raw_text

    if text == bot_text["account"]:

        user = cur.execute(f"SELECT * FROM users WHERE user_id = {user_id}").fetchone()

        if user[2] is None:

            keys = [

                [

                    Button.request_phone(bot_text["phone_share"], resize=1)

                ],

                [

                    Button.text(bot_text["back"])

                ]

            ]

            await event.reply(bot_text["select"], buttons=keys)

        else:

            keys_account = [

                [
                    Button.text(bot_text["info"], resize=1)
                ],

                [

                    back

                ]

            ]

            await event.reply(bot_text["select"], buttons=keys_account)

    elif text == bot_text["install_help"]:

        keys = [

            [

                Button.inline(bot_text["android"], b'android_help')

            ],

            [

                Button.inline(bot_text["windows"], b'windows_help')

            ],

            [

                Button.inline(bot_text["mac"], b'mac_help')

            ],

            [

                Button.inline(bot_text["ios"], b'ios_help')

            ],

            [

                Button.inline(bot_text["linux"], b'soon')

            ],

        ]

        await event.reply(bot_text["for_install"], buttons=keys)

    elif text == bot_text["get_buy"]:

        key = Button.url(bot_text["support_text"], url="https://t.me/CONNECT_HELP")

        await event.reply(bot_text["get_buy_text"], buttons=key)

    elif text == bot_text["download_app"]:

        keys = [

            [

                Button.inline(bot_text["android"], b'down_android')

            ],

            [

                Button.inline(bot_text["windows"], b'down_windows')

            ],

            [

                Button.inline(bot_text["mac"], b'down_mac')

            ],

            [

                Button.inline(bot_text["ios"], b'down_ios')

            ],

            [

                Button.inline(bot_text["linux"], b'soon')

            ],

        ]

        await event.reply(bot_text["download_help"], buttons=keys)

    elif text == bot_text["panel"]:

        if user_id in config.ADMINS_LIST:

            keys = [

                [Button.text(bot_text["all_send"], resize=1)],

                [

                    Button.text(bot_text["ban_user"], resize=1),

                    Button.text(bot_text["active_test"], resize=1),

                    Button.text(bot_text["get_access"])

                ],

                [

                    Button.text(bot_text["down_inventory"]),

                    Button.text(bot_text["up_inventory"]),

                    Button.text(bot_text["user_info_panel"])

                ],
                [
                    Button.text(bot_text["change_iphone"])
                ],
                [

                    back

                ]

            

            ]

            await event.reply(bot_text["select"], buttons=keys)
    elif text == bot_text["change_iphone"]:
        async with bot.conversation(user_id, timeout=1000) as conv:
            await conv.send_message(bot_text["enter_serv_username"])
            username_panel = await conv.get_response()
            username_panel = username_panel.raw_text
            find_service = cur.execute(f"SELECT * FROM services WHERE username = '{username_panel}'").fetchone()
            if find_service is None:
                await conv.send_message(bot_text["service_not_found"])
            else:
                url = f"{config.panel_api_address}?method=data_user&name={username_panel}&ADMIN=SpeedConnect"
                response = requests.get(url)
                response = response.json()
                total = int(response["total"]) * 1000
                size = response["size"]
                update_value_size = int(total) - int(size)
                expire = functions.calculate_date_difference(response["date_buy"], response["day"]) * 86400
                username, sub = await functions.get_iphone_service(expire, functions.mega_to_bytes(update_value_size))
                random_num = randint(1000000, 9999999)
                # متغیر شروع با زمان فعلی
                service_name = config.iphone_plan_names[int(find_service[3])]
                start_time = time.time()

                # تبدیل زمان به فرمت datetime

                start_datetime = datetime.fromtimestamp(start_time)

                # شرط برای اضافه کردن روز

                if "1 ماهه" in service_name:

                    condition = 'add_32_days'  # می‌توانید این مقدار را به 'add_64_days' یا 'add_99_days' تغییر دهید

                elif "2 ماهه" in service_name:

                    condition = 'add_64_days'

                elif "3 ماهه" in service_name:

                    condition = 'add_99_days'

                else:

                    print("نیست")

                if condition == 'add_32_days':

                    new_datetime = start_datetime + timedelta(days=32)

                elif condition == 'add_64_days':

                    new_datetime = start_datetime + timedelta(days=64)

                elif condition == 'add_99_days':

                    new_datetime = start_datetime + timedelta(days=99)

                else:

                    new_datetime = start_datetime  # در صورت عدم تطابق، زمان اولیه را برمی‌گرداند

                # تبدیل زمان جدید به timestamp

                new_timestamp = new_datetime.timestamp()
                cur.execute(
                    f"INSERT INTO iphone_services VALUES ({user_id}, '{username}', '{sub}', '{service_num}', {random_num}, {start_time}, {new_timestamp})")
                db.commit()
                print(username, sub)
                delete_user = f"{config.panel_api_address}?method=delete_user&name={username_panel}&ADMIN=SpeedConnect"
                response = requests.get(delete_user)
                print(response.json())
                text = f"""اشتراک اختصاصی شما حذف شد و اشتراک آیفون برای شما ساخته شد
                لینک اشتراک آیفون شما:
                {sub}
                نام کاربری اشتراک آیفون شما:
                {username}
                """
                await event.reply(text)
    elif text == bot_text["user_info_panel"]:
        if user_id in config.ADMINS_LIST:
            async with bot.conversation(user_id, timeout=1000) as conv:

                await conv.send_message(bot_text["enter_user_id"])

                while True:

                    try:

                        user_id_ = await conv.get_response()

                        if user_id_.raw_text == bot_text["back"]:

                            return

                        user_id_ = int(user_id_.raw_text)

                        find_user = cur.execute(f"SELECT * FROM users WHERE user_id = {user_id_}").fetchone()

                        if find_user is not None:

                            user_get = await bot.get_entity(user_id_)

                            user_full_name = user_get.first_name if user_get.last_name is None else user_get.first_name + user_get.last_name

                            username_ = "❌" if user_get.username is None else user_get.username

                            user_phone = find_user[2]

                            user_inventory = find_user[1]

                            service_count = cur.execute(f"SELECT * FROM services WHERE user_id = {user_id_}").fetchall()

                            service_count_ = len(service_count)

                            keys_user_info = [

                                [

                                    Button.inline(bot_text["user_services"], str.encode("user_services:" + str(user_id_)))

                                ]

                            ]

                            await bot.send_message(user_id, bot_text["user_info_content"].format(user_name=user_full_name, username=username_, user_phone=user_phone, user_inventory=user_inventory, service_count=service_count_), buttons=keys_user_info)

                            break

                        else:

                            await conv.send_message(bot_text["user_not_found"])

                    except ValueError:

                        await conv.send_message(bot_text["just_num"])

    elif text == bot_text["get_access"]:

        if user_id in config.ADMINS_LIST:

            async with bot.conversation(user_id, timeout=1000) as conv:

                await conv.send_message(bot_text["enter_access_code"])

                while True:

                    try:

                        user_id_ = await conv.get_response()

                        if user_id_.raw_text == bot_text["back"]:

                            return

                        user_id_ = int(user_id_.raw_text)

                        print(user_id_)

                        find_user = cur.execute(f"SELECT * FROM users WHERE access_code = {user_id_}").fetchone()

                        print(find_user)

                        if find_user is not None:

                            cur.execute(f"UPDATE users SET has_access = {True} WHERE access_code = {user_id_}")

                            db.commit()

                            await event.reply(bot_text["su_get_access"])

                            break

                        else:

                            await conv.send_message(bot_text["user_not_found"])

                    except ValueError:

                        await conv.send_message(bot_text["just_num"])            

    elif text == bot_text["back"]:

        if user_id in config.ADMINS_LIST:

            await event.reply(bot_text["start"], buttons=admin_keys)

        else:

            await event.reply(bot_text["start"], buttons=home_keys)

    elif text == bot_text["info"]:

        user = cur.execute(f"SELECT * FROM users WHERE user_id = {user_id}").fetchone()

        user_phone = user[2]

        user_inventory = user[1]

        if user_phone is None:

            keys = [

                [

                    Button.request_phone(bot_text["phone_share"], resize=1)

                ],

                [

                    Button.text(bot_text["back"])

                ]

            ]

            await event.reply(bot_text["select"], buttons=keys)

            return
        services = len(cur.execute(f"SELECT * FROM services WHERE user_id = {user_id}").fetchall())
        suc_pay = len(cur.execute(f"SELECT * FROM pay WHERE user_id = {user_id} AND confirmation = {True}").fetchall())
        no_pay = len(cur.execute(f"SELECT * FROM pay WHERE user_id = {user_id} AND confirmation = {False}").fetchall())
        full_text = bot_text["user_info_text"].format(user_id=user_id, phone=user_phone, inventory=user_inventory, sr=services, ok_pay=suc_pay, no_pay=no_pay)

        await event.reply(full_text, buttons=back)

    elif text == bot_text["charge_account"]:

        user = cur.execute(f"SELECT * FROM users WHERE user_id = {user_id}").fetchone()

        if user[2] is None:

            keys = [

                [

                    Button.request_phone(bot_text["phone_share"], resize=1)

                ],

                [

                    Button.text(bot_text["back"])

                ]

            ]

            await event.reply(bot_text["select"], buttons=keys)

            return

        charge_keys = [

            [

                Button.text(bot_text["zibal"]),

                Button.text(bot_text["cart"])

            ],

            [

                back

            ]

        ]

        await event.reply(bot_text["charge_text"], buttons= charge_keys)

    elif text == bot_text["new_service"]:
        select_keys = [
            [
                Button.inline(bot_text["new_service"], b"serv_new")
            ],
            [
                Button.inline(bot_text["iphone_account"], b"buy_iphone_account")
            ]
        ]
        await event.reply(bot_text["select"], buttons=select_keys)

    elif text == bot_text["test_account"]:

        find_tests = cur.execute(f"SELECT * FROM test_account WHERE user_id = {user_id}").fetchall()

        if len(find_tests) == 0:

            loading = await event.reply(bot_text["loading_test_account"])

            username_test = None

            password_test = None
            end = time.time() + 86400
            test_num = randint(1000, 9999)

            cur.execute(f"INSERT INTO test_account VALUES ({user_id}, '{username_test}', '{password_test}', {test_num}, {end}, {False})")

            db.commit()

            url = f"{config.API_ADDRESS}get-service/?number=1&user_id={user_id}"

            response = requests.get(url=url)

            response = response.json()

            if response["status"] == 200:

                username_test, password_test = response["username"], response["password"]

                cur.execute(f"UPDATE test_account SET username = '{username_test}', password = '{password_test}' WHERE test_num = {test_num}")

                db.commit()

                await bot.delete_messages(user_id, loading.id)

                full_text = f"اکانت تست با موفقیت ساخته شد✅\nمشخصات سرویس:\nنام کاربری:{username_test}\nرمز عبور:{password_test}"

                await event.reply(full_text)

            else:

                cur.execute(f"DELETE FROM test_account WHERE test_num = {test_num}")

                await event.reply(bot_text["cant_make_service"])

        else:

            user_can_test = cur.execute(f"SELECT can_test FROM users WHERE user_id = {user_id}").fetchone()[0]

            if user_can_test:

                loading = await event.reply(bot_text["loading_test_account"])

                test_num = randint(1000, 9999)

                username_test = None

                password_test = None
                end = time.time() + 86400
                cur.execute(f"INSERT INTO test_account VALUES ({user_id}, '{username_test}', '{password_test}', {test_num}, {end}, {False})")

                db.commit()

                url = f"{config.API_ADDRESS}get-service/?number=1&user_id={user_id}"

                response = requests.get(url=url)

                response = response.json()
                print(response)
                if response["status"] == 200:

                    cur.execute(f"UPDATE users SET can_test = {False} WHERE user_id = {user_id}")

                    db.commit()

                    username_test, password_test = response["username"], response["password"]

                    cur.execute(f"UPDATE test_account SET username = '{username_test}', password = '{password_test}' WHERE test_num = {test_num}")

                    db.commit()

                    await bot.delete_messages(user_id, loading.id)

                    full_text = f"اکانت تست با موفقیت ساخته شد✅\nمشخصات سرویس:\nنام کاربری:{username_test}\nرمز عبور:{password_test}"

                    await event.reply(full_text)

                else:

                    cur.execute(f"DELETE FROM test_account WHERE test_num = {test_num}")

                    await event.reply(bot_text["cant_make_service"])

            else:

                await event.reply(bot_text["before_test"])

    elif text == bot_text["zibal"]:

        user = cur.execute(f"SELECT * FROM users WHERE user_id = {user_id}").fetchone()

        if user[2] is None:

            keys = [

                [

                    Button.request_phone(bot_text["phone_share"], resize=1)

                ],

                [

                    Button.text(bot_text["back"])

                ]

            ]

            await event.reply(bot_text["select"], buttons=keys)

            return

        async with bot.conversation(user_id, timeout=1000) as conv:

            # pay_type_keys = [

            #     [Button.inline(bot_text["wallet"], b'wallet')],

            #     [Button.inline(bot_text["direct"], b'direct')],

            #     [Button.inline(bot_text["cancel"], b'cancel')]

            # ]

            # ask_pay = await conv.send_message(bot_text["ask_pay_type"], buttons=pay_type_keys)

            # pay_type = await conv.wait_event(events.CallbackQuery())

            # if pay_type.data == b'wallet':

            #     pay_type = "wallet"

            # elif pay_type.data == b'direct':

            #     pay_type = "direct"

            # elif pay_type.data == b'cancel':

            #     await bot.delete_messages(user_id, ask_pay.id)

            #     await event.reply(bot_text["canceled"])

            #     return

            # else:

            #     await event.reply(bot_text["action_not_found"])

            #     return

            pay_type = "direct"

            await conv.send_message(bot_text["enter_amount"])

            while True:

                try:

                    amount = await conv.get_response()

                    amount = amount.raw_text

                    if amount == bot_text["back"]:

                        await conv.cancel_all()

                    if int(amount) < 10000:

                        await conv.send_message(bot_text["small_amount"])

                    elif int(amount) > 5000000:

                        await conv.send_message(bot_text["big_amount"])

                    else:

                        break

                except ValueError:

                    await conv.send_message(bot_text["just_num"])

            await conv.send_message(bot_text["name"])

            name = await conv.get_response()

            if name.media is not None:

                await conv.send_message(bot_text["dont_image"])

                return

            if name.raw_text == bot_text["back"]:

                return

            phone = cur.execute(f"SELECT phone FROM users WHERE user_id = {user_id}").fetchone()[0]

            url = 'https://gateway.zibal.ir/v1/request'

            data = {

                'merchant': config.merchant,

                'amount': int(amount) * 10,

                'callbackUrl': "https://kooll.online/",

                'description': name.raw_text,

                'mobile': phone

            }

            head = {

                "Content-Type": "application/json",

            }

            response = requests.post(url, json=data, headers=head)

            response = response.json()

            if response["result"] != 100:

                await event.reply(bot_text["zibal_problem"])

            else:

                track_id = response["trackId"]

                cur.execute(f"INSERT INTO pay VALUES ({user_id}, {amount}, '{name.raw_text}', '{phone}', '{None}', '{None}', 'zibal', {track_id}, '{pay_type}', {False}, '{None}')")

                db.commit()

                key = [

                    [

                        Button.url(bot_text["pay_url"].format(amount=amount), f"https://gateway.zibal.ir/start/{track_id}")

                    ],

                    [

                        Button.inline(bot_text["zibal_confirmation"], str.encode("zibal_conf:" + str(track_id)))

                    ]

                ]

                find_user_phone = cur.execute(f"SELECT phone From users WHERE user_id = {user_id}").fetchone()[0]

                await event.reply(bot_text["zibal_ok"].format(amount=int(amount), phone=find_user_phone), buttons=key)

    elif text == bot_text["cart"]:

        user = cur.execute(f"SELECT * FROM users WHERE user_id = {user_id}").fetchone()

        if user[2] is None:

            keys = [

                [

                    Button.request_phone(bot_text["phone_share"], resize=1)

                ],

                [

                    Button.text(bot_text["back"])

                ]

            ]

            await event.reply(bot_text["select"], buttons=keys)

            return

        async with bot.conversation(user_id, timeout=1000) as conv:

            # pay_type_keys = [

            #     [Button.inline(bot_text["wallet"], b'wallet')],

            #     [Button.inline(bot_text["direct"], b'direct')],

            #     [Button.inline(bot_text["cancel"], b'cancel')]

            # ]

            # ask_pay = await conv.send_message(bot_text["ask_pay_type"], buttons=pay_type_keys)

            # pay_type = await conv.wait_event(events.CallbackQuery())

            # if pay_type.data == b'wallet':

            #     pay_type = "wallet"

            # elif pay_type.data == b'direct':

            #     pay_type = "direct"

            # elif pay_type.data == b'cancel':

            #     await bot.delete_messages(user_id, ask_pay.id)

            #     await event.reply(bot_text["canceled"])

            #     return

            # else:

            #     await event.reply(bot_text["action_not_found"])

            #     return

            pay_type = "wallet"

            await conv.send_message(bot_text["enter_amount"])

            while True:

                try:

                    amount = await conv.get_response()

                    amount = amount.raw_text

                    if amount == bot_text["back"]:

                        await conv.cancel_all()

                    if int(amount) < 10000:

                        await conv.send_message(bot_text["small_amount"])

                    elif int(amount) > 5000000:

                        await conv.send_message(bot_text["big_amount"])

                    else:

                        break

                except ValueError:

                    await conv.send_message(bot_text["just_num"])

            await conv.send_message(bot_text["name"])

            name = await conv.get_response()

            if name.media is not None:

                await conv.send_message(bot_text["dont_image"])

                return

            if name.raw_text == bot_text["back"]:

                return

            phone = cur.execute(f"SELECT phone FROM users WHERE user_id = {user_id}").fetchone()[0]

            await conv.send_message(bot_text["cart_pay_created"].format(amount=int(amount), cart=config.CART))

            while True:

                image = await conv.get_response()

                if image.media is not None:

                    path = await image.download_media()

                    break

                else:

                    if image.raw_text == bot_text["back"]:

                        return

                    await conv.send_message(bot_text["just_media"])

            code = randint(1000, 9999)

            cur.execute(f"INSERT INTO pay VALUES ({user_id}, {amount}, '{name.raw_text}', {phone}, '{None}', {code}, 'cart', '{None}', 'wallet', {False}, '{path}')")

            db.commit()

            for admin in config.ADMINS_LIST:

                find_pay = cur.execute(f"SELECT * FROM pay WHERE code = {code}").fetchone()

                phone = find_pay[3]

                desc = find_pay[2]

                pay_type = find_pay[8]

                now = datetime.now()

                iran_timezone = pytz.timezone('Asia/Tehran')

                iran_time = now.astimezone(iran_timezone)

                now_hms = iran_time.strftime("%H-%M-%S")

                now_hms = str(now_hms).split("-")

                now_hms = now_hms[0] + ":" + now_hms[1] + ":" + now_hms[2]

                now_string_ = jdatetime.date.fromgregorian(day=iran_time.day, month=iran_time.month, year=iran_time.year)

                now_string = str(now_string_).split("-")

                year, month, day = now_string[0], now_string[1], now_string[2]

                month_s = {

                    "01": "فروردین",

                    "02": "اردیبهشت",

                    "03": "خرداد",

                    "04": "تیر",

                    "05": "مرداد",

                    "06": "شهریور",

                    "07": "مهر",

                    "08": "آبان",

                    "09": "آذر",

                    "10": "دی",

                    "11": "بهمن",

                    "12": "اسفند"

                }

                time_s = f"{day} {month_s[month]} {year}"

                fa_pay_type = {

                    "direct": bot_text["direct"],

                    "wallet": bot_text["wallet"]

                }

                conf_keys = [

                    Button.inline(bot_text["cart_conf"], str.encode("cart_conf:" + str(code))),

                    Button.inline(bot_text["cart_not_conf"], str.encode("cart_not_conf:" + str(code))),

                ]

                await bot.send_message(admin, bot_text["new_pay_cart"].format(user_id=user_id, name=desc, phone=phone, time=now_hms, date=time_s, code=code, amount=int(amount), pay_type=fa_pay_type[pay_type]), file=path, buttons=conf_keys)

            await conv.send_message(bot_text["cart_send_admin"])

    elif text == bot_text["wallet"]:
        # key = [
        #
        #     [
        #         Button.inline(bot_text["charge_wallet"], data=b'charge_wallet')
        #     ],
        #
        # ]
        #
        # await event.reply(bot_text["select"], buttons=key)
        keys = [

            [

                Button.inline(bot_text["pay_link_cart"], b'cart_pay')

            ],

            [

                Button.inline(bot_text["pay_link_zibal"], b'pay_zibal')

            ],

        ]
        user_inventory = cur.execute(f"SELECT inventory FROM users WHERE user_id = {user_id}").fetchone()[0]
        await event.reply(bot_text["pay_war"].format(inventory=user_inventory), buttons=keys)
    elif text == bot_text["pay_history"]:

        history = cur.execute(f"SELECT * FROM pay WHERE user_id = {user_id} AND confirmation = {True}").fetchall()

        keys = []

        for pay in history:

            pay_code = pay[5]

            key = [

                Button.inline(str(pay_code), str.encode("get_info:" + str(pay_code)))

            ]

            keys.append(key)

        await event.reply(bot_text["select"], buttons=keys)

    elif text == bot_text["my_services"]:
        keys = [
            [
                Button.text(bot_text["vip_info"])
            ],
            [
                Button.text(bot_text["iphone_info"])
            ],
            [back]
        ]
        await event.reply(bot_text["select"], buttons=keys)
    elif text == bot_text["vip_info"]:
        history = cur.execute(f"SELECT * FROM services WHERE user_id = {user_id}").fetchall()

        if len(history) == 0:

            key = Button.inline(bot_text["go_buy"], b'new_service_go')

            await event.reply(bot_text["not_service"], buttons=key)

            return

        keys = []

        for service in history:

            serv_code = service[3]

            random_num = service[4]

            service_name = service[1]        

            key = [

                Button.inline(str(service_name), str.encode("gt_service:" + str(serv_code) + ":" + str(random_num)))

            ]

            keys.append(key)

        await event.reply(bot_text["select"], buttons=keys)
    elif text == bot_text["iphone_info"]:
        history = cur.execute(f"SELECT * FROM iphone_services WHERE user_id = {user_id}").fetchall()

        if len(history) == 0:

            key = Button.inline(bot_text["go_buy"], b'new_service_go')

            await event.reply(bot_text["not_service"], buttons=key)

            return

        keys = []

        for service in history:

            serv_code = service[3]

            random_num = service[4]

            service_name = service[1]

            key = [

                Button.inline(str(service_name), str.encode("iphone_gt_service:" + str(serv_code) + ":" + str(random_num)))

            ]

            keys.append(key)

        await event.reply(bot_text["select"], buttons=keys)
    elif text == bot_text["down_inventory"]:

        if user_id in config.ADMINS_LIST:

            async with bot.conversation(user_id, timeout=1000) as conv:

                await conv.send_message(bot_text["enter_user_id"])

                while True:

                    try:

                        user_id_ = await conv.get_response()

                        if user_id_.raw_text == bot_text["back"]:

                            return

                        user_id_ = int(user_id_.raw_text)

                        find_user = cur.execute(f"SELECT * FROM users WHERE user_id = {user_id_}").fetchone()

                        if find_user is not None:

                            await conv.send_message(bot_text["enter_amount"])

                            while True:

                                try:

                                    amount = await conv.get_response()

                                    amount = amount.raw_text

                                    amount = int(amount)

                                    if amount == bot_text["back"]:

                                        return

                                    user_inventory = int(cur.execute(f"SELECT inventory FROM users WHERE user_id = {user_id_}").fetchone()[0])

                                    if user_inventory - amount < 0:

                                        await conv.send_message(bot_text["user_null_inventory"])

                                    else:

                                        user_inventory -= amount

                                        cur.execute(f"UPDATE users SET inventory = {user_inventory} WHERE user_id = {user_id_}")

                                        await conv.send_message(bot_text["su_down"])

                                        return

                                except ValueError:

                                    await conv.send_message(bot_text["just_num"])

                        else:

                            await conv.send_message(bot_text["user_not_found"])

                    except ValueError:

                        await conv.send_message(bot_text["just_num"])

    elif text == bot_text["up_inventory"]:

        if user_id in config.ADMINS_LIST:

            async with bot.conversation(user_id, timeout=1000) as conv:

                await conv.send_message(bot_text["enter_user_id"])

                while True:

                    try:

                        user_id_ = await conv.get_response()

                        if user_id_.raw_text == bot_text["back"]:

                            return

                        user_id_ = int(user_id_.raw_text)

                        find_user = cur.execute(f"SELECT * FROM users WHERE user_id = {user_id_}").fetchone()

                        if find_user is not None:

                            await conv.send_message(bot_text["enter_amount"])

                            while True:

                                try:

                                    amount = await conv.get_response()

                                    amount = amount.raw_text

                                    amount = int(amount)

                                    if amount == bot_text["back"]:

                                        return

                                    user_inventory = int(cur.execute(f"SELECT inventory FROM users WHERE user_id = {user_id_}").fetchone()[0])

                                    user_inventory += amount

                                    cur.execute(f"UPDATE users SET inventory = {user_inventory} WHERE user_id = {user_id_}")

                                    await conv.send_message(bot_text["su_up"])

                                    return

                                except ValueError:

                                    await conv.send_message(bot_text["just_num"])

                        else:

                            await conv.send_message(bot_text["user_not_found"])

                    except ValueError:

                        await conv.send_message(bot_text["just_num"])

    elif text == bot_text["ban_user"]:

        if user_id in config.ADMINS_LIST:

            async with bot.conversation(user_id, timeout=1000) as conv:

                await conv.send_message(bot_text["enter_user_id"])

                while True:

                    try:

                        user_id_ = await conv.get_response()

                        if user_id_.raw_text == bot_text["back"]:

                            return

                        user_id_ = int(user_id_.raw_text)

                        find_user = cur.execute(f"SELECT * FROM users WHERE user_id = {user_id_}").fetchone()

                        if find_user is not None:

                            cur.execute(f"UPDATE users SET is_ban = {True} WHERE user_id = {user_id_}")

                            db.commit()

                            await event.reply(bot_text["user_banned"])

                            break

                        else:

                            await conv.send_message(bot_text["user_not_found"])

                    except ValueError:

                        await conv.send_message(bot_text["just_num"])

    elif text == bot_text["active_test"]:

        if user_id in config.ADMINS_LIST:

            async with bot.conversation(user_id, timeout=1000) as conv:

                await conv.send_message(bot_text["enter_user_id"])

                while True:

                    try:

                        user_id_ = await conv.get_response()

                        if user_id_.raw_text == bot_text["back"]:

                            return

                        user_id_ = int(user_id_.raw_text)

                        find_user = cur.execute(f"SELECT * FROM users WHERE user_id = {user_id_}").fetchone()

                        if find_user is not None:

                            cur.execute(f"UPDATE users SET can_test = {True} WHERE user_id = {user_id_}")

                            db.commit()

                            await event.reply(bot_text["test_activated"])

                            break

                        else:

                            await conv.send_message(bot_text["user_not_found"])

                    except ValueError:

                        await conv.send_message(bot_text["just_num"])

    elif text == bot_text["all_send"]:

        if user_id in config.ADMINS_LIST:

            async with bot.conversation(user_id, timeout=1000) as conv:

                await conv.send_message(bot_text["question_image"])

                image_msg = await conv.get_response()

                image_path = None

                if image_msg.media is not None:

                    image_path = await image_msg.download_media()

                    await conv.send_message(bot_text["question_text"])

                    text = await conv.get_response()

                    q_text = text.message

                else:

                    if image_msg.message == bot_text["back"]:

                        key = [

                            Button.text(bot_text["back"], resize=1)

                        ]

                        await bot.send_message(user_id, bot_text['canceled'], buttons=key)

                        return

                    else:

                        q_text = image_msg.message

                users = cur.execute(f"SELECT user_id FROM users").fetchall()

                for user in users:

                    user_id_ = user[0]

                    try:

                        r = await bot.send_message(user_id_, q_text, file=image_path)
                        await bot.pin_message(user_id_, r.id)
                    except:

                        continue

@bot.on(events.CallbackQuery(pattern="cart_conf:"))

async def cart_conf(event):

    user_id = event.sender_id

    is_ban = config.is_ban(user_id)

    if is_ban:

        await event.reply(bot_text["you_banned"])

        return

    user = cur.execute(f"SELECT * FROM users WHERE user_id = {user_id}").fetchone()

    if user[2] is None:

        keys = [

            [

                Button.request_phone(bot_text["phone_share"], resize=1)

            ],

            [

                Button.text(bot_text["back"])

            ]

        ]

        await event.reply(bot_text["select"], buttons=keys)

        return

    if user_id in config.ADMINS_LIST:

        code = event.data.decode().split(":")[1]

        pay = cur.execute(f"SELECT * FROM pay WHERE code = {code}").fetchone()

        if pay is None:

            await bot.send_message(user_id, bot_text["pay_not_found"])

            return

        if pay[9]:

            await bot.send_message(user_id, bot_text["pay_before_conf"])

            return

        now = datetime.now()

        iran_timezone = pytz.timezone('Asia/Tehran')

        iran_time = now.astimezone(iran_timezone)

        now_hms = iran_time.strftime("%H-%M-%S")

        now_string_ = jdatetime.date.fromgregorian(day=iran_time.day, month=iran_time.month, year=iran_time.year)

        now_hms = str(now_hms).split("-")

        now_hms = now_hms[0] + ":" + now_hms[1] + ":" + now_hms[2]

        cur.execute(f"""UPDATE pay SET confirmation = {True}, date_time = '{str(now_string_) + " " + now_hms}' WHERE code = {code}""")

        db.commit()

        for admin in config.ADMINS_LIST:

            await bot.send_message(admin, bot_text["admin_pay_conf"].format(code=code))

        pay_user_id = pay[0]

        pay_amount = pay[1]

        pay_desc = pay[2]

        pay_phone = pay[3]

        pay_type = pay[8]

        pay_date = str(now_string_)

        pay_time = str(now_hms)
        
        if pay_type == "wallet":

            user_inventory = cur.execute(f"SELECT inventory FROM users WHERE user_id = {pay_user_id}").fetchone()[0]

            user_inventory += pay_amount

            cur.execute(f"UPDATE users SET inventory = {user_inventory} WHERE user_id = {pay_user_id}")

            db.commit()

        now_string = str(now_string_).split("-")

        year, month, day = now_string[0], now_string[1], now_string[2]

        month_s = {

            "01": "فروردین",

            "02": "اردیبهشت",

            "03": "خرداد",

            "04": "تیر",

            "05": "مرداد",

            "06": "شهریور",

            "07": "مهر",

            "08": "آبان",

            "09": "آذر",

            "10": "دی",

            "11": "بهمن",

            "12": "اسفند"

        }

        time_s = f"{day} {month_s[month]} {year}"

        fa_pay_type = {

            "direct": bot_text["direct"],

            "wallet": bot_text["wallet"]

        }

        print(pay_user_id)

        await bot.send_message(pay_user_id, bot_text["user_pay_conf"].format(amount=int(pay_amount), amount_two=int(pay_amount), name=pay_desc, phone=pay_phone, pay_type=fa_pay_type[pay_type], time=pay_time, date=time_s, code=code))



@bot.on(events.CallbackQuery(pattern="zibal_conf:"))

async def zibal_conf(event):

    user_id = event.sender_id

    is_ban = config.is_ban(user_id)

    if is_ban:

        await event.reply(bot_text["you_banned"])

        return

    user = cur.execute(f"SELECT * FROM users WHERE user_id = {user_id}").fetchone()

    if user[2] is None:

        keys = [

            [

                Button.request_phone(bot_text["phone_share"], resize=1)

            ],

            [

                Button.text(bot_text["back"])

            ]

        ]

        await event.reply(bot_text["select"], buttons=keys)

        return

    track_id = event.data.decode().split(":")[1]

    check_url = "https://gateway.zibal.ir/v1/inquiry"

    body = {

        "merchant": config.merchant,

        "trackId": track_id,

    }

    head = {

        "Content-Type": "application/json"

    }

    check_pay = requests.post(check_url, json=body, headers=head)

    check_pay = check_pay.json()

    if check_pay["status"] == 2:

        conf_url = "https://gateway.zibal.ir/v1/verify"

        body = {

            "merchant": config.merchant,

            "trackId": track_id,

        }

        head = {

            "Content-Type": "application/json"

        }

        conf_pay = requests.post(conf_url, json=body, headers=head)

        conf_pay = conf_pay.json()

        if conf_pay["status"] == 1:

            code = randint(1000, 9999)

            now = datetime.now()

            iran_timezone = pytz.timezone('Asia/Tehran')

            # تبدیل زمان و تاریخ فعلی به منطقه زمانی ایران

            iran_time = now.astimezone(iran_timezone)

            now_hms = iran_time.strftime("%H-%M-%S")

            now_string_ = jdatetime.date.fromgregorian(day=iran_time.day, month=iran_time.month, year=iran_time.year)

            now_string = str(now_string_).split("-")

            year, month, day = now_string[0], now_string[1], now_string[2]

            month_s = {

                "01": "فروردین",

                "02": "اردیبهشت",

                "03": "خرداد",

                "04": "تیر",

                "05": "مرداد",

                "06": "شهریور",

                "07": "مهر",

                "08": "آبان",

                "09": "آذر",

                "10": "دی",

                "11": "بهمن",

                "12": "اسفند"

            }

            time_s = f"{day} {month_s[month]} {year}"

            find_user = cur.execute(f"SELECT * FROM users WHERE user_id = {user_id}").fetchone()

            now_hms = str(now_hms).split("-")

            now_hms = now_hms[0] + ":" + now_hms[1] + ":" + now_hms[2]

            cur.execute(f"""UPDATE pay SET date_time = '{str(now_string_) + " " + now_hms}', code = {code}, confirmation={True} WHERE track_id = {track_id}""")

            find_pay = cur.execute(f"SELECT * FROM pay WHERE code = {code}").fetchone()

            pay_type = find_pay[8]

            user_inventory = find_user[1]

            fa_pay_type = {

                "wallet": "کیف پول",

                "direct": "مستقیم"

            }

            if pay_type == "wallet":

                user_inventory += int(conf_pay["amount"]) // 10

                cur.execute(f"UPDATE users SET inventory = {user_inventory} WHERE user_id = {user_id}")

                db.commit()

                await event.reply(bot_text["zibal_pay_ok_wallet"].format(time=now_hms, code=code, amount_two=int(conf_pay["amount"]) // 10, inventory=user_inventory, date=time_s, pay_type=fa_pay_type[find_pay[8]], amount=int(conf_pay["amount"]) // 10))

            else:

                await event.reply(bot_text["zibal_pay_ok"].format(time=now_hms, code=code, amount_two=int(conf_pay["amount"]) // 10, inventory=user_inventory, date=time_s, pay_type=fa_pay_type[find_pay[8]]))

            await bot.delete_messages(user_id, event.original_update.msg_id)

            for admin in config.ADMINS_LIST:

                phone = find_pay[3]

                desc = find_pay[2]

                fa_pay_type = {

                    "wallet": "کیف پول",

                    "direct": "مستقیم",

                }

                await bot.send_message(admin, bot_text["new_pay_zibal"].format(user_id=user_id, name=desc, phone=phone, time=now_hms, date=time_s, code=code, amount=int(conf_pay["amount"]) // 10, pay_type=fa_pay_type[pay_type]))

        else:

            await event.reply(bot_text["zibal_conf_problem"])

    else:

        await event.reply(bot_text["zibal_not_pay"])



@bot.on(events.CallbackQuery(data=b'wallet_with_draw'))

async def wallet_with_draw(event):

    user_id = event.sender_id

    is_ban = config.is_ban(user_id)

    if is_ban:

        await event.reply(bot_text["you_banned"])

        return

    async with bot.conversation(user_id, timeout=1000) as conv:

        await conv.send_message(bot_text["enter_amount"])

        while True:

            try:

                amount = await conv.get_response()

                amount = amount.raw_text

                amount = int(amount)

                if amount == bot_text["back"]:

                    await conv.cancel_all()

                else:

                    break

            except ValueError:

                await conv.send_message(bot_text["just_num"])

        user_inventory = cur.execute(f"SELECT inventory FROM users WHERE user_id = {user_id}").fetchone()[0]

        if user_inventory - amount < 0:

            await event.reply(bot_text["none_inventory"])

            return

        now = datetime.now()

        iran_timezone = pytz.timezone('Asia/Tehran')

        iran_time = now.astimezone(iran_timezone)

        now_hms = iran_time.strftime("%H-%M-%S")

        now_string_ = jdatetime.date.fromgregorian(day=iran_time.day, month=iran_time.month, year=iran_time.year)

        now_hms = str(now_hms).split("-")

        now_hms = now_hms[0] + ":" + now_hms[1] + ":" + now_hms[2]

        now_string = str(now_string_).split("-")

        year, month, day = now_string[0], now_string[1], now_string[2]

        month_s = {

            "01": "فروردین",

            "02": "اردیبهشت",

            "03": "خرداد",

            "04": "تیر",

            "05": "مرداد",

            "06": "شهریور",

            "07": "مهر",

            "08": "آبان",

            "09": "آذر",

            "10": "دی",

            "11": "بهمن",

            "12": "اسفند"

        }

        time_s = f"{day} {month_s[month]} {year}"

        code = randint(1000, 9999)

        cur.execute(f"""INSERT INTO pay VALUES ({user_id}, {amount}, 'خالی', 'خالی', '{str(now_string_) + " " + now_hms}', {code}, 'cart', '{None}', 'direct', {True}, '{None}')""")

        cur.execute(f"""UPDATE users SET inventory = {user_inventory - amount} WHERE user_id = {user_id}""")

        db.commit()

        await event.reply(bot_text["wallet_with_draw"].format(amount=amount, amount_two=amount, pay_type="مستقیم", name="خالی", phone="خالی", date=time_s, time=now_hms, code=code))

# @bot.on(events.CallbackQuery(data=b'charge_wallet'))
#
# async def charge_wallet(event):
#
#     user_id = event.sender_id
#
#     is_ban = config.is_ban(user_id)
#
#     if is_ban:
#
#         await event.reply(bot_text["you_banned"])
#
#         return
#
#     # async with bot.conversation(user_id, timeout=1000) as conv:
#
#     #     await conv.send_message(bot_text["enter_amount"])
#
#     #     while True:
#
#     #         try:
#
#     #             amount = await conv.get_response()
#
#     #             amount = amount.raw_text
#
#     #             if amount == bot_text["back"]:
#
#     #                 await conv.cancel_all()
#
#     #             if int(amount) < 10000:
#
#     #                 await conv.send_message(bot_text["small_amount"])
#
#     #             elif int(amount) > 5000000:
#
#     #                 await conv.send_message(bot_text["big_amount"])
#
#     #             else:
#
#     #                 break
#
#     #         except ValueError:
#
#     #             await conv.send_message(bot_text["just_num"])
#
#     # who = "new" if config.lock_bot != 1 else "hamkaran"
#
#     # # keys = [
#
#     # #     [
#
#     # #         Button.url(bot_text["pay_link_cart"], f"https://t.me/{config.pay_bot_username}?start=pay=cart={amount}={who}")
#
#     # #     ],
#
#     # #     [
#
#     # #         Button.url(bot_text["pay_link_zibal"], f"https://t.me/{config.pay_bot_username}?start=pay=zibal={amount}={who}")
#
#     # #     ],
#
#     # # ]
#     keys = [
#
#         [
#
#             Button.inline(bot_text["pay_link_cart"], b'cart_pay')
#
#         ],
#
#         [
#
#             Button.inline(bot_text["pay_link_zibal"], b'pay_zibal')
#
#         ],
#
#     ]
#
#     await event.reply(bot_text["pay_war"].format(inventory=), buttons=keys)



@bot.on(events.CallbackQuery(data=b'pay_zibal'))

async def zibal_pay(event):

    user_id = event.sender_id

    is_ban = config.is_ban(user_id)

    if is_ban:

        await event.reply(bot_text["you_banned"])

        return

    user = cur.execute(f"SELECT * FROM users WHERE user_id = {user_id}").fetchone()

    if user[2] is None:

        keys = [

            [

                Button.request_phone(bot_text["phone_share"], resize=1)

            ],

            [

                Button.text(bot_text["back"])

            ]

        ]

        await event.reply(bot_text["select"], buttons=keys)

        return

    async with bot.conversation(user_id, timeout=1000) as conv:

        # pay_type_keys = [

        #     [Button.inline(bot_text["wallet"], b'wallet')],

        #     [Button.inline(bot_text["direct"], b'direct')],

        #     [Button.inline(bot_text["cancel"], b'cancel')]

        # ]

        # ask_pay = await conv.send_message(bot_text["ask_pay_type"], buttons=pay_type_keys)

        # pay_type = await conv.wait_event(events.CallbackQuery())

        # if pay_type.data == b'wallet':

        #     pay_type = "wallet"

        # elif pay_type.data == b'direct':

        #     pay_type = "direct"

        # elif pay_type.data == b'cancel':

        #     await bot.delete_messages(user_id, ask_pay.id)

        #     await event.reply(bot_text["canceled"])

        #     return

        # else:

        #     await event.reply(bot_text["action_not_found"])

        #     return

        pay_type = "wallet"

        await conv.send_message(bot_text["enter_amount"])

        while True:

            try:

                amount = await conv.get_response()

                amount = amount.raw_text

                if amount == bot_text["back"]:

                    await conv.cancel_all()

                if int(amount) < 10000:

                    await conv.send_message(bot_text["small_amount"])

                elif int(amount) > 5000000:

                    await conv.send_message(bot_text["big_amount"])

                else:

                    break

            except ValueError:

                await conv.send_message(bot_text["just_num"])

        await conv.send_message(bot_text["name"])

        name = await conv.get_response()

        if name.media is not None:

            await conv.send_message(bot_text["dont_image"])

            return

        if name.raw_text == bot_text["back"]:

            return

        phone = cur.execute(f"SELECT phone FROM users WHERE user_id = {user_id}").fetchone()[0]

        url = 'https://gateway.zibal.ir/v1/request'

        data = {

            'merchant': config.merchant,

            'amount': int(amount) * 10,

            'callbackUrl': "https://kooll.online/",

            'description': name.raw_text,

            'mobile': phone

        }

        head = {

            "Content-Type": "application/json",

        }

        response = requests.post(url, json=data, headers=head)

        response = response.json()

        if response["result"] != 100:

            await event.reply(bot_text["zibal_problem"])

        else:

            track_id = response["trackId"]

            cur.execute(f"INSERT INTO pay VALUES ({user_id}, {amount}, '{name.raw_text}', '{phone}', '{None}', '{None}', 'zibal', {track_id}, '{pay_type}', {False}, '{None}')")

            db.commit()

            key = [

                [

                    Button.url(bot_text["pay_url"].format(amount=amount), f"https://gateway.zibal.ir/start/{track_id}")

                ],

                [

                    Button.inline(bot_text["zibal_confirmation"], str.encode("zibal_conf:" + str(track_id)))

                ]

            ]

            find_user_phone = cur.execute(f"SELECT phone From users WHERE user_id = {user_id}").fetchone()[0]

            await event.reply(bot_text["zibal_ok"].format(amount=int(amount), phone=find_user_phone), buttons=key)

@bot.on(events.CallbackQuery(data=b'cart_pay'))

async def cart_pay(event):

    user_id = event.sender_id

    is_ban = config.is_ban(user_id)

    if is_ban:

        await event.reply(bot_text["you_banned"])

        return

    user = cur.execute(f"SELECT * FROM users WHERE user_id = {user_id}").fetchone()

    if user[2] is None:

        keys = [

            [

                Button.request_phone(bot_text["phone_share"], resize=1)

            ],

            [

                Button.text(bot_text["back"])

            ]

        ]

        await event.reply(bot_text["select"], buttons=keys)

        return

    async with bot.conversation(user_id, timeout=1000) as conv:

        # pay_type_keys = [

        #     [Button.inline(bot_text["wallet"], b'wallet')],

        #     [Button.inline(bot_text["direct"], b'direct')],

        #     [Button.inline(bot_text["cancel"], b'cancel')]

        # ]

        # ask_pay = await conv.send_message(bot_text["ask_pay_type"], buttons=pay_type_keys)

        # pay_type = await conv.wait_event(events.CallbackQuery())

        # if pay_type.data == b'wallet':

        #     pay_type = "wallet"

        # elif pay_type.data == b'direct':

        #     pay_type = "direct"

        # elif pay_type.data == b'cancel':

        #     await bot.delete_messages(user_id, ask_pay.id)

        #     await event.reply(bot_text["canceled"])

        #     return

        # else:

        #     await event.reply(bot_text["action_not_found"])

        #     return

        pay_type = "wallet"

        await conv.send_message(bot_text["enter_amount"])

        while True:

            try:

                amount = await conv.get_response()

                amount = amount.raw_text

                if amount == bot_text["back"]:

                    await conv.cancel_all()

                if int(amount) < 10000:

                    await conv.send_message(bot_text["small_amount"])

                elif int(amount) > 5000000:

                    await conv.send_message(bot_text["big_amount"])

                else:

                    break

            except ValueError:

                await conv.send_message(bot_text["just_num"])

        await conv.send_message(bot_text["name"])

        name = await conv.get_response()

        if name.media is not None:

            await conv.send_message(bot_text["dont_image"])

            return

        if name.raw_text == bot_text["back"]:

            return

        phone = cur.execute(f"SELECT phone FROM users WHERE user_id = {user_id}").fetchone()[0]

        await conv.send_message(bot_text["cart_pay_created"].format(amount=int(amount), cart=config.CART))

        while True:

            image = await conv.get_response()

            if image.media is not None:

                path = await image.download_media()

                break

            else:

                if image.raw_text == bot_text["back"]:

                    return

                await conv.send_message(bot_text["just_media"])

        code = randint(1000, 9999)

        cur.execute(f"INSERT INTO pay VALUES ({user_id}, {amount}, '{name.raw_text}', {phone}, '{None}', {code}, 'cart', '{None}', 'wallet', {False}, '{path}')")

        db.commit()

        for admin in config.ADMINS_LIST:

            find_pay = cur.execute(f"SELECT * FROM pay WHERE code = {code}").fetchone()

            phone = find_pay[3]

            desc = find_pay[2]

            pay_type = find_pay[8]

            now = datetime.now()

            iran_timezone = pytz.timezone('Asia/Tehran')

            iran_time = now.astimezone(iran_timezone)

            now_hms = iran_time.strftime("%H-%M-%S")

            now_hms = str(now_hms).split("-")

            now_hms = now_hms[0] + ":" + now_hms[1] + ":" + now_hms[2]

            now_string_ = jdatetime.date.fromgregorian(day=iran_time.day, month=iran_time.month, year=iran_time.year)

            now_string = str(now_string_).split("-")

            year, month, day = now_string[0], now_string[1], now_string[2]

            month_s = {

                "01": "فروردین",

                "02": "اردیبهشت",

                "03": "خرداد",

                "04": "تیر",

                "05": "مرداد",

                "06": "شهریور",

                "07": "مهر",

                "08": "آبان",

                "09": "آذر",

                "10": "دی",

                "11": "بهمن",

                "12": "اسفند"

            }

            time_s = f"{day} {month_s[month]} {year}"

            fa_pay_type = {

                "direct": bot_text["direct"],

                "wallet": bot_text["wallet"]

            }

            conf_keys = [

                Button.inline(bot_text["cart_conf"], str.encode("cart_conf:" + str(code))),

                Button.inline(bot_text["cart_not_conf"], str.encode("cart_not_conf:" + str(code))),

            ]

            await bot.send_message(admin, bot_text["new_pay_cart"].format(user_id=user_id, name=desc, phone=phone, time=now_hms, date=time_s, code=code, amount=int(amount), pay_type=fa_pay_type[pay_type]), file=path, buttons=conf_keys)

        await conv.send_message(bot_text["cart_send_admin"])

@bot.on(events.CallbackQuery(data=b'back'))

async def back_call(event):

    user_id = event.sender_id

    is_ban = config.is_ban(user_id)

    if is_ban:

        await event.reply(bot_text["you_banned"])

        return

    user = cur.execute(f"SELECT * FROM users WHERE user_id = {user_id}").fetchone()

    if user[2] is None:

        keys = [

            [

                Button.request_phone(bot_text["phone_share"], resize=1)

            ],

            [

                Button.text(bot_text["back"])

            ]

        ]

        await event.reply(bot_text["select"], buttons=keys)

        return

    if user_id in config.ADMINS_LIST:

        await event.reply(bot_text["start"], buttons=admin_keys)

    else:

        await event.reply(bot_text["start"], buttons=home_keys)

@bot.on(events.CallbackQuery(pattern="get_info:*"))

async def get_info(event):

    user_id = event.sender_id

    is_ban = config.is_ban(user_id)

    if is_ban:

        await event.reply(bot_text["you_banned"])

        return

    code = event.data.decode().split(":")[1]

    pay = cur.execute(f"SELECT * FROM pay WHERE code = {code}").fetchone()

    if pay is None:

        await bot.send_message(user_id, bot_text["pay_not_found"])

        return

    pay_type = pay[8]

    pay_amount = pay[1]

    pay_name = pay[2]

    pay_phone = pay[3]

    pay_date_time = pay[4]

    pay_date = str(pay_date_time).split(" ")[0]

    pay_time = str(pay_date_time).split(" ")[1]

    fa_pay_type = {

        "wallet": "کیف پول",

        "direct": "مستقیم"

    }

    full_text = bot_text["null_text"].format(pay_type=fa_pay_type[pay_type], amount=int(pay_amount), amount_two=int(pay_amount), name=pay_name, phone=pay_phone, date=pay_date, time=pay_time, code=code)

    await event.reply(full_text)

@bot.on(events.CallbackQuery(pattern="cart_not_conf:*"))

async def cart_not_conf(event):

    user_id = event.sender_id

    is_ban = config.is_ban(user_id)

    if is_ban:

        await event.reply(bot_text["you_banned"])

        return

    code = event.data.decode().split(":")[1]

    pay = cur.execute(f"SELECT * FROM pay WHERE code = {code}").fetchone()

    if pay is None:

        await bot.send_message(user_id, bot_text["pay_not_found"])

    if pay[9] is False:

        await bot.send_message(user_id, bot_text["before_not_conf"])

        return

    cur.execute(f"UPDATE pay SET confirmation = {False} WHERE code = {code}")

    db.commit()

    for admin in config.ADMINS_LIST:

        await bot.send_message(admin, bot_text["admin_not_conf"].format(code=code))

    await bot.send_message(pay[0], bot_text["user_not_conf"].format(code=code))

@bot.on(events.CallbackQuery(data=b'one_member'))

async def one_mem(event):

    user_id = event.sender_id

    is_ban = config.is_ban(user_id)

    if is_ban:

        await event.reply(bot_text["you_banned"])

        return

    buttons = []

    for key, value in config.one_member_names.items():

        buttons.append([Button.inline(value, data=str.encode("buy_service:" + str(key)))])

    await event.reply(bot_text["select"], buttons=buttons)

@bot.on(events.CallbackQuery(data=b'two_member'))

async def two_mem(event):

    user_id = event.sender_id

    is_ban = config.is_ban(user_id)

    if is_ban:

        await event.reply(bot_text["you_banned"])

        return

    buttons = []

    for key, value in config.two_member_names.items():

        buttons.append([Button.inline(value, data=str.encode("buy_service:" + str(key)))])

    await event.reply(bot_text["select"], buttons=buttons)

@bot.on(events.CallbackQuery(data=b'three_member'))

async def three_mem(event):

    user_id = event.sender_id

    is_ban = config.is_ban(user_id)

    if is_ban:

        await event.reply(bot_text["you_banned"])

        return

    buttons = []

    for key, value in config.three_member_names.items():

        buttons.append([Button.inline(value, data=str.encode("buy_service:" + str(key)))])

    await event.reply(bot_text["select"], buttons=buttons)

@bot.on(events.CallbackQuery(pattern="buy_service:*"))

async def buy_serv(event):

    user_id = event.sender_id

    is_ban = config.is_ban(user_id)

    if is_ban:

        await event.reply(bot_text["you_banned"])

        return

    service_num = int(event.data.decode().split(":")[1])

    amount = config.amounts[service_num]

    service_name = None

    try:

        service_name = config.one_member_names[service_num]

    except KeyError:

        try:

            service_name = config.two_member_names[service_num]

        except KeyError:

            service_name = config.three_member_names[service_num]

    keys = [

        [

            Button.inline(bot_text["pay_and_active"], str.encode("buy_with_wallet:" + str(service_num)))

        ],

        # [

        #     Button.inline(bot_text["pay"], str.encode("pay_service:" + str(service_num)))

        # ]

    ]

    await event.reply(bot_text["pay_replay"].format(amount=amount, service=service_name), buttons=keys)


@bot.on(events.CallbackQuery(pattern="iphone_buy_serv:*"))

async def buy_ipn(event):

    user_id = event.sender_id

    is_ban = config.is_ban(user_id)

    if is_ban:

        await event.reply(bot_text["you_banned"])

        return
    print(event.data.decode().split(":"))
    service_num = int(event.data.decode().split(":")[1])

    amount = config.iphone_amounts[service_num]
    print(amount)
    service_name = config.iphone_plan_names[service_num]

    keys = [

        [

            Button.inline(bot_text["pay_and_active"], str.encode("iphone_buy_wallet:" + str(service_num)))

        ],

        # [

        #     Button.inline(bot_text["pay"], str.encode("pay_service:" + str(service_num)))

        # ]

    ]

    await event.reply(bot_text["pay_replay"].format(amount=amount, service=service_name), buttons=keys)


@bot.on(events.CallbackQuery(pattern="pay_service:*"))

async def pay_serv(event):

    user_id = event.sender_id

    is_ban = config.is_ban(user_id)

    if is_ban:

        await event.reply(bot_text["you_banned"])

        return

    service_num = int(event.data.decode().split(":")[1])

    amount = config.amounts[service_num]

    service_name = None

    try:

        service_name = config.one_member_names[service_num]

    except KeyError:

        try:

            service_name = config.two_member_names[service_num]

        except KeyError:

            service_name = config.three_member_names[service_num]



    await event.reply(bot_text["pay_link_replay"].format(amount=amount, service=service_name))    

@bot.on(events.CallbackQuery(pattern="buy_with_wallet:*"))

async def buy_with_wallet(event):

    user_id = event.sender_id

    is_ban = config.is_ban(user_id)

    if is_ban:

        await event.reply(bot_text["you_banned"])

        return

    await bot.delete_messages(user_id, event.original_update.msg_id)

    service_num = int(event.data.decode().split(":")[1])

    find_amount = config.amounts[service_num]

    user_inventory = cur.execute(f"SELECT inventory FROM users WHERE user_id = {user_id}").fetchone()[0]

    if user_inventory - int(find_amount) < 0:

        await event.reply(bot_text["none_inventory"])

    else:

        keys = [

            Button.inline(bot_text["yes"], str.encode("wallet_yes:" + str(service_num))),

            Button.inline(bot_text["no"], b'wallet_no'),

        ]

        service_name = None

        try:

            service_name = config.one_member_names[service_num]

        except KeyError:

            try:

                service_name = config.two_member_names[service_num]

            except KeyError:

                service_name = config.three_member_names[service_num]

        await event.reply(bot_text["pay_wallet_sure"].format(service=service_name), buttons=keys)


@bot.on(events.CallbackQuery(pattern="iphone_buy_wallet:*"))

async def iphone_buy_wallet(event):

    user_id = event.sender_id

    is_ban = config.is_ban(user_id)

    if is_ban:

        await event.reply(bot_text["you_banned"])

        return

    await bot.delete_messages(user_id, event.original_update.msg_id)

    service_num = int(event.data.decode().split(":")[1])

    find_amount = config.iphone_amounts[service_num]

    user_inventory = cur.execute(f"SELECT inventory FROM users WHERE user_id = {user_id}").fetchone()[0]

    if user_inventory - int(find_amount) < 0:

        await event.reply(bot_text["none_inventory"])

    else:

        keys = [

            Button.inline(bot_text["yes"], str.encode("iphone_yes:" + str(service_num))),

            Button.inline(bot_text["no"], b'iphone_no'),

        ]

        service_name = iphone_plan_names[service_num]

        await event.reply(bot_text["pay_wallet_sure"].format(service=service_name), buttons=keys)


@bot.on(events.CallbackQuery(pattern="iphone_yes:*"))
async def iphone_yes(event):
    msg_id = event.original_update.msg_id

    user_id = event.sender_id

    is_ban = config.is_ban(user_id)

    if is_ban:
        await event.reply(bot_text["you_banned"])

        return

    service_num = int(event.data.decode().split(":")[1])

    amount = config.iphone_amounts[service_num]
    expire = config.iphone_expire_dates[service_num]
    data_limit = config.iphone_data_limits[service_num]
    await bot.delete_messages(user_id, msg_id)

    user_inventory = cur.execute(f"SELECT inventory FROM users WHERE user_id={user_id}").fetchone()[0]

    user_inventory = int(user_inventory) - int(amount)

    cur.execute(f"UPDATE users SET inventory = {user_inventory} WHERE user_id = {user_id}")

    to = cur.execute(f"SELECT phone FROM users WHERE user_id = {user_id}").fetchone()[0]

    db.commit()

    loading = await event.reply(bot_text["loading_account"])

    url = f"{config.API_ADDRESS}get-service-iphone/?expire={expire}&data_limit={data_limit}"
    try:
        response = requests.get(url=url)
    except:
        response = None

    response = response.json()
    print(response)
    if response["status"] == 200:

        username = response["username"]
        sub_link = response["sub_link"]
        random_num = randint(100000, 999999)
        service_name = config.iphone_plan_names[service_num]
        # متغیر شروع با زمان فعلی

        start_time = time.time()

        # تبدیل زمان به فرمت datetime

        start_datetime = datetime.fromtimestamp(start_time)

        # شرط برای اضافه کردن روز

        if "1 ماهه" in service_name:

            condition = 'add_32_days'  # می‌توانید این مقدار را به 'add_64_days' یا 'add_99_days' تغییر دهید

        elif "2 ماهه" in service_name:

            condition = 'add_64_days'

        elif "3 ماهه" in service_name:

            condition = 'add_99_days'

        else:

            print("نیست")

        if condition == 'add_32_days':

            new_datetime = start_datetime + timedelta(days=32)

        elif condition == 'add_64_days':

            new_datetime = start_datetime + timedelta(days=64)

        elif condition == 'add_99_days':

            new_datetime = start_datetime + timedelta(days=99)

        else:

            new_datetime = start_datetime  # در صورت عدم تطابق، زمان اولیه را برمی‌گرداند

        # تبدیل زمان جدید به timestamp

        new_timestamp = new_datetime.timestamp()

        # نمایش زمان جدید به صورت timestamp

        # print("زمان جدید (timestamp):", new_timestamp)

        cur.execute(
            f"INSERT INTO iphone_services VALUES ({user_id}, '{username}', '{sub_link}', '{service_num}', {random_num}, {start_time}, {new_timestamp})")

        db.commit()

        await bot.delete_messages(user_id, loading.id)

        for admin in config.ADMINS_LIST:
            user_get = await bot.get_entity(user_id)

            user_full_name = user_get.first_name if user_get.last_name is None else user_get.first_name + user_get.last_name

            username_ = "❌" if user_get.username is None else user_get.username

            await bot.send_message(admin, bot_text["admin_service_notif_iphone"].format(service_name=service_name,
                                                                                 user_inventory=user_inventory,
                                                                                 user_phone=to,
                                                                                 username=username_,
                                                                                 user_name=user_full_name,
                                                                                 user_id=user_id,
                                                                                 sub_link=sub_link))

        full_text = f"""🔑 اشتراک شما با موفقیت ساخته شد.

⚡️ اطلاعات حساب کاربری شما عبارت است از :

نام کاربری : {username} 
لینک اشتراک : {sub_link}
📌 مشخصات حساب کاربری شما نیز به قرار زیر است:"""
        service_time = service_name.split("-")[1]
        service_value = service_name.split("-")[0]
        key = [
            [Button.inline(service_time), Button.inline("زمان سرویس")],
            [Button.inline(service_value), Button.inline("حجم سرویس")]
        ]
        await event.reply(full_text, buttons=key)

        username_sms = config.sms_username

        password_sms = config.sms_password

        api = Api(username_sms, password_sms)

        sms_soap = api.sms('soap')

        text = """

        پرداخت  فاکتور شما تایید و حساب کاربری  شما ساخته شد.



        اطلاعات حساب کاربری شما عبارت است از:



        نام کاربری : {1}

        رمز عبور  : {2}



        فروشگاه آنلاین

        """

        test = sms_soap.send_by_base_number(f"{username};بدون رمز عبور", to, 239802)

        print(test)

    else:

        user_inventory = cur.execute(f"SELECT inventory FROM users WHERE user_id={user_id}").fetchone()[0]

        user_inventory = int(user_inventory) + int(amount)

        cur.execute(f"UPDATE users SET inventory = {user_inventory} WHERE user_id = {user_id}")

        db.commit()

        await event.reply(bot_text["cant_make_service"])

@bot.on(events.CallbackQuery(pattern="wallet_yes:*"))

async def yes_wallet(event):

    msg_id = event.original_update.msg_id

    user_id = event.sender_id

    is_ban = config.is_ban(user_id)

    if is_ban:

        await event.reply(bot_text["you_banned"])

        return

    service_num = int(event.data.decode().split(":")[1])

    amount = config.amounts[service_num]

    await bot.delete_messages(user_id, msg_id)

    user_inventory = cur.execute(f"SELECT inventory FROM users WHERE user_id={user_id}").fetchone()[0]

    user_inventory = int(user_inventory) - int(amount)

    cur.execute(f"UPDATE users SET inventory = {user_inventory} WHERE user_id = {user_id}")

    to = cur.execute(f"SELECT phone FROM users WHERE user_id = {user_id}").fetchone()[0]

    db.commit()

    loading = await event.reply(bot_text["loading_account"])

    url = f"{config.API_ADDRESS}get-service/?number={service_num}&user_id={user_id}"

    response = requests.get(url=url)

    response = response.json()

    if response["status"] == 200:

        username, password = response["username"], response["password"]

        random_num = randint(1000, 9999)

        service_name = None

        try:

            service_name = config.one_member_names[service_num]

        except KeyError:

            try:

                service_name = config.two_member_names[service_num]

            except KeyError:

                service_name = config.three_member_names[service_num]

        # متغیر شروع با زمان فعلی

        start_time = time.time()



        # تبدیل زمان به فرمت datetime

        start_datetime = datetime.fromtimestamp(start_time)



        # شرط برای اضافه کردن روز

        if "1 ماهه" in service_name:

            condition = 'add_32_days'  # می‌توانید این مقدار را به 'add_64_days' یا 'add_99_days' تغییر دهید

        elif "2 ماهه" in service_name:

            condition = 'add_64_days'

        elif "3 ماهه" in service_name:

            condition = 'add_99_days'

        else:

            print("نیست")

        if condition == 'add_32_days':

            new_datetime = start_datetime + timedelta(days=32)

        elif condition == 'add_64_days':

            new_datetime = start_datetime + timedelta(days=64)

        elif condition == 'add_99_days':

            new_datetime = start_datetime + timedelta(days=99)

        else:

            new_datetime = start_datetime  # در صورت عدم تطابق، زمان اولیه را برمی‌گرداند



        # تبدیل زمان جدید به timestamp

        new_timestamp = new_datetime.timestamp()



        # نمایش زمان جدید به صورت timestamp

        # print("زمان جدید (timestamp):", new_timestamp)

        cur.execute(f"INSERT INTO services VALUES ({user_id}, '{username}', '{password}', {service_num}, {random_num}, {start_time}, {new_timestamp}, {False})")

        db.commit()

        await bot.delete_messages(user_id, loading.id)

        for admin in config.ADMINS_LIST:

            user_get = await bot.get_entity(user_id)

            user_full_name = user_get.first_name if user_get.last_name is None else user_get.first_name + user_get.last_name

            username_ = "❌" if user_get.username is None else user_get.username

            await bot.send_message(admin, bot_text["admin_service_notif"].format(service_name=service_name, user_inventory=user_inventory, user_phone=to, service_password=password, username=username_, user_name=user_full_name, user_id=user_id))

        full_text = f"""🔑 اشتراک شما با موفقیت ساخته شد.
          
⚡️ اطلاعات حساب کاربری شما عبارت است از :
    
نام کاربری : {username} 

رمز عبور : {password} 

📌 مشخصات حساب کاربری شما نیز به قرار زیر است:"""
        service_time = service_name.split("-")[1]
        service_value = service_name.split("-")[0]
        key = [
            [Button.inline(service_time), Button.inline("زمان سرویس")],
            [Button.inline(service_value), Button.inline("حجم سرویس")]
        ]
        await event.reply(full_text, buttons=key)

        username_sms = config.sms_username

        password_sms = config.sms_password

        api = Api(username_sms,password_sms)

        sms_soap = api.sms('soap')

        text = """

        پرداخت  فاکتور شما تایید و حساب کاربری  شما ساخته شد.



        اطلاعات حساب کاربری شما عبارت است از:



        نام کاربری : {1}

        رمز عبور  : {2}



        فروشگاه آنلاین

        """

        test = sms_soap.send_by_base_number(f"{username};{password}", to, 239802)

        print(test)

    else:

        user_inventory = cur.execute(f"SELECT inventory FROM users WHERE user_id={user_id}").fetchone()[0]

        user_inventory = int(user_inventory) + int(amount)

        cur.execute(f"UPDATE users SET inventory = {user_inventory} WHERE user_id = {user_id}")

        db.commit()

        await event.reply(bot_text["cant_make_service"])

@bot.on(events.CallbackQuery(pattern="gt_service:*"))

async def serv_info_get(event):

    user_id = event.sender_id

    is_ban = config.is_ban(user_id)

    if is_ban:

        await event.reply(bot_text["you_banned"])

        return

    service_num = int(event.data.decode().split(":")[1])

    random_num = int(event.data.decode().split(":")[2])

    service = cur.execute(f"SELECT * FROM services WHERE service_num = {service_num} AND random_num = {random_num}").fetchone()

    username, password = service[1], service[2]

    service_name = None

    try:

        service_name = config.one_member_names[service_num]

    except KeyError:

        try:

            service_name = config.two_member_names[service_num]

        except KeyError:

            service_name = config.three_member_names[service_num]
    url = f"{config.API_ADDRESS}client-info?username={username}"
    r = await event.reply("درحال دریافت اطلاعات...")
    response = requests.get(url)
    await bot.delete_messages(user_id, r.id)
    response = response.json()
    is_active = None
    print(response["info"]['active'])
    if response["info"]['active'] == 'deactive':
        is_active = "غیر فعال"
    else:
        is_active = "فعال"
    full_text = f"""
🌿 نام سرویس: {service_name}

وضعیت: {is_active}


📌 شما میتوانید با استفاده از دکمه های زیر سرویس خود را مدیریت کنید

🆔 @SpeedConnectbot"""
    keys = [
        [
            Button.inline(bot_text["service_info"], str.encode("sr_inf:" + str(username))),
            Button.inline(bot_text["connected_pep"], str.encode("sr_pep:" + str(username)))
        ],
        [
            Button.inline(bot_text["change_service_to_iphone"], str.encode("change_service_to_iphone:" + str(username) + ":" + str(service_num)))
        ]
        # [
        #     Button.inline(bot_text["sub_link"], str.encode("sr_vl:" + str(username))),
        #     Button.inline(bot_text["outline"], str.encode("sr_ot:" + str(username)))
        # ],
    ]
    await event.reply(full_text, buttons=keys)
@bot.on(events.CallbackQuery(pattern="change_service_to_iphone:*"))
async def change_service_to_iphone(event):
    user_id = event.sender_id
    username_panel = event.data.decode().split(":")[1]
    service_num = event.data.decode().split(":")[2]
    url = f"{config.panel_api_address}?method=data_user&name={username_panel}&ADMIN=SpeedConnect"
    response = requests.get(url)
    response = response.json()
    total = int(response["total"]) * 1000
    size = response["size"]
    update_value_size = int(total) - int(size)
    expire = functions.calculate_date_difference(response["date_buy"], response["day"]) * 86400
    username, sub = await functions.get_iphone_service(expire, functions.mega_to_bytes(update_value_size))
    random_num = randint(1000000, 9999999)
    # متغیر شروع با زمان فعلی
    service_name = config.iphone_plan_names[int(service_num)]
    start_time = time.time()

    # تبدیل زمان به فرمت datetime

    start_datetime = datetime.fromtimestamp(start_time)

    # شرط برای اضافه کردن روز

    if "1 ماهه" in service_name:

        condition = 'add_32_days'  # می‌توانید این مقدار را به 'add_64_days' یا 'add_99_days' تغییر دهید

    elif "2 ماهه" in service_name:

        condition = 'add_64_days'

    elif "3 ماهه" in service_name:

        condition = 'add_99_days'

    else:

        print("نیست")

    if condition == 'add_32_days':

        new_datetime = start_datetime + timedelta(days=32)

    elif condition == 'add_64_days':

        new_datetime = start_datetime + timedelta(days=64)

    elif condition == 'add_99_days':

        new_datetime = start_datetime + timedelta(days=99)

    else:

        new_datetime = start_datetime  # در صورت عدم تطابق، زمان اولیه را برمی‌گرداند

    # تبدیل زمان جدید به timestamp

    new_timestamp = new_datetime.timestamp()
    cur.execute(
        f"INSERT INTO iphone_services VALUES ({user_id}, '{username}', '{sub}', '{service_num}', {random_num}, {start_time}, {new_timestamp})")
    db.commit()
    print(username, sub)
    delete_user = f"{config.panel_api_address}?method=delete_user&name={username_panel}&ADMIN=SpeedConnect"
    response = requests.get(delete_user)
    print(response.json())
    text = f"""اشتراک اختصاصی شما حذف شد و اشتراک آیفون برای شما ساخته شد
لینک اشتراک آیفون شما:
{sub}
نام کاربری اشتراک آیفون شما:
{username}
"""
    await event.reply(text)
@bot.on(events.CallbackQuery(pattern="iphone_gt_service:*"))

async def iphone_gt_service(event):

    user_id = event.sender_id

    is_ban = config.is_ban(user_id)

    if is_ban:

        await event.reply(bot_text["you_banned"])

        return

    service_num = int(event.data.decode().split(":")[1])

    random_num = int(event.data.decode().split(":")[2])

    service = cur.execute(f"SELECT * FROM iphone_services WHERE random_num = {random_num}").fetchone()

    username = service[1]

    service_name = config.iphone_plan_names[service_num]
    r = await event.reply("درحال دریافت اطلاعات...")
    user_info = await functions.get_info(username)
    await bot.delete_messages(user_id, r.id)
    if user_info['status'] == 'deactive':
        is_active = "غیر فعال"
    else:
        is_active = "فعال"
    full_text = f"""
🌿 نام سرویس: {service_name}

وضعیت: {is_active}


📌 شما میتوانید با استفاده از دکمه های زیر سرویس خود را مدیریت کنید

🆔 @SpeedConnectbot"""
    keys = [
        [
            Button.inline(bot_text["service_info"], str.encode("iphone_sr_inf:" + str(username))),
        ],
        # [
        #     Button.inline(bot_text["sub_link"], str.encode("sr_vl:" + str(username))),
        #     Button.inline(bot_text["outline"], str.encode("sr_ot:" + str(username)))
        # ],
    ]
    await event.reply(full_text, buttons=keys)

@bot.on(events.CallbackQuery(data=b'android_help'))

async def android_help(event):

    user_id = event.sender_id

    is_ban = config.is_ban(user_id)

    if is_ban:

        await event.reply(bot_text["you_banned"])

        return

    await bot.send_message(user_id, bot_text["android_help"])

    android_video_path = f"media{os.sep}android.mp4"

    await bot.send_file(user_id, file=android_video_path)

@bot.on(events.CallbackQuery(data=b'windows_help'))

async def win_help(event):

    user_id = event.sender_id

    is_ban = config.is_ban(user_id)

    if is_ban:

        await event.reply(bot_text["you_banned"])

        return

    await bot.send_message(user_id, bot_text["windows_help"])

    windows_video_path = f"media{os.sep}windows.mp4"

    await bot.send_file(user_id, file=windows_video_path)

@bot.on(events.CallbackQuery(data=b'mac_help'))

async def win_help(event):

    user_id = event.sender_id

    is_ban = config.is_ban(user_id)

    if is_ban:

        await event.reply(bot_text["you_banned"])

        return

    await bot.send_message(user_id, bot_text["mac_help"])

    mac_video_path = f"media{os.sep}mac.mp4"

    await bot.send_file(user_id, file=mac_video_path)

@bot.on(events.CallbackQuery(data=b'ios_help'))

async def win_help(event):

    user_id = event.sender_id

    is_ban = config.is_ban(user_id)

    if is_ban:

        await event.reply(bot_text["you_banned"])

        return

    await bot.send_message(user_id, bot_text["ios_help"])

    ios_video_path = f"media{os.sep}ios.mp4"

    await bot.send_file(user_id, file=ios_video_path)

@bot.on(events.CallbackQuery(data=b'down_android'))

async def android_down(event):

    user_id = event.sender_id

    await bot.send_message(user_id, bot_text["down_android"])

@bot.on(events.CallbackQuery(data=b'down_windows'))

async def win_down(event):

    user_id = event.sender_id

    await bot.send_message(user_id, bot_text["down_windows"])

@bot.on(events.CallbackQuery(data=b'down_mac'))

async def mac_down(event):

    user_id = event.sender_id

    await bot.send_message(user_id, bot_text["down_mac"])

@bot.on(events.CallbackQuery(data=b'down_ios'))

async def ios_down(event):

    user_id = event.sender_id

    await bot.send_message(user_id, bot_text["down_ios"])

@bot.on(events.CallbackQuery(data=b'soon'))

async def soon(event):

    user_id = event.sender_id

    is_ban = config.is_ban(user_id)

    if is_ban:

        await event.reply(bot_text["you_banned"])

        return

    await bot.send_message(user_id, bot_text["soon"])

@bot.on(events.CallbackQuery(pattern="user_services:*"))

async def user_services(event):

    admin_user_id = event.sender_id

    if admin_user_id in config.ADMINS_LIST:

        user_id = event.data.decode().split(":")[1]

        history = cur.execute(f"SELECT * FROM services WHERE user_id = {user_id}").fetchall()

        if len(history) == 0:

            await event.reply(bot_text["user_dont_service"])

            return

        keys = []

        for service in history:

            serv_code = service[3]

            random_num = service[4]

            service_name = service[1]        

            key = [

                Button.inline(str(service_name), str.encode("sh_admin_serv:" + str(serv_code) + ":" + str(random_num)))

            ]

            keys.append(key)

        await event.reply(bot_text["select"], buttons=keys)

@bot.on(events.CallbackQuery(pattern="sh_admin_serv:*"))

async def sh_admin_serv_func(event):

    user_id = event.sender_id

    if user_id in config.ADMINS_LIST:

        is_ban = config.is_ban(user_id)

        if is_ban:

            await event.reply(bot_text["you_banned"])

            return

        service_num = int(event.data.decode().split(":")[1])

        random_num = int(event.data.decode().split(":")[2])

        service = cur.execute(f"SELECT * FROM services WHERE service_num = {service_num} AND random_num = {random_num}").fetchone()

        username, password = service[1], service[2]

        service_name = None

        try:

            service_name = config.one_member_names[service_num]

        except KeyError:

            try:

                service_name = config.two_member_names[service_num]

            except KeyError:

                service_name = config.three_member_names[service_num]

        full_text = f"""

        ⚡️ اطلاعات حساب کاربر عبارت است از:

        username: {username}

        password: {password}



        📌 مشخصات حساب کاربر نیز به قرار زیر است:



        نوع سرویس: {service_name}"""

        await event.reply(full_text)
@bot.on(events.CallbackQuery(data=b'serv_new'))
async def ssn(event):
    user_id = event.sender_id
    members_key = [

        [

            Button.inline(bot_text["one_member"], b'one_member'),

        ],

        [

            Button.inline(bot_text["two_member"], b'two_member'),

        ],

        [

            Button.inline(bot_text["three_member"], b'three_member'),

        ]

    ]

    await bot.send_message(user_id, bot_text["select"], buttons=members_key)
@bot.on(events.CallbackQuery(data=b'buy_iphone_account'))
async def bia(event):
    user_id = event.sender_id

    is_ban = config.is_ban(user_id)

    if is_ban:

        await event.reply(bot_text["you_banned"])

        return

    buttons = []

    for key, value in config.iphone_plan_names.items():

        buttons.append([Button.inline(value, data=str.encode("iphone_buy_serv:" + str(key)))])

    await event.reply(bot_text["select"], buttons=buttons)

@bot.on(events.NewMessage(pattern=f"(?i){bot_text['service_extension']}"))
async def sr_extension(event):
    user_id = event.sender_id
    history = cur.execute(f"SELECT * FROM services WHERE user_id = {user_id}").fetchall()

    if len(history) == 0:

        key = Button.inline(bot_text["go_buy"], b'new_service_go')

        await event.reply(bot_text["not_service"], buttons=key)

        return
    async with bot.conversation(user_id, timeout=1000) as conv:
        await conv.send_message(bot_text["enter_service_username"], buttons=back)
        username = await conv.get_response()
        if username.raw_text is None or username.raw_text == bot_text["back"]:
            return
        else:
            username = username.raw_text
            url = f"{config.API_ADDRESS}client-info?username={username}"
            response = requests.get(url)
            print(response)
            if response.status_code != 200:
                await conv.send_message(bot_text["service_not_found"])
                return
            else:
                response = response.json()
                service_username = response["info"]["username"]
                if service_username != username:
                    await conv.send_message(bot_text["service_not_found"])
                    return
                else:
                    service_password = response["info"]["password"]
                    await conv.send_message(bot_text["enter_service_password"], buttons=back)
                    password = await conv.get_response()
                    if service_password != password.raw_text:
                        await conv.send_message(bot_text["password_invalid"])
                        return
                    else:
                        find_service = cur.execute(f"SELECT * FROM services WHERE username = '{service_username}' AND user_id = {user_id}").fetchone()
                        if find_service is None:
                            await conv.send_message(bot_text["service_not_found"])
                            return
                        else:
                            serv_code = find_service[3]

                            random_num = find_service[4]

                            service_name = find_service[1]

                            key = [

                                Button.inline(str(service_name), str.encode("ex_service:" + str(serv_code) + ":" + str(random_num)))

                            ]

                            await event.reply(bot_text["select"], buttons=key)
@bot.on(events.CallbackQuery(pattern="ex_service:*"))
async def ex_service(event):
    user_id = event.sender_id
    service_num = event.data.decode().split(":")[1]
    random_num = event.data.decode().split(":")[2]
    find_service = cur.execute(f"SELECT username FROM services WHERE random_num = {random_num}").fetchone()
    if find_service is None:
        await event.reply(bot_text["service_not_found"])
    else:
        info_url = f"{config.API_ADDRESS}client-info/?username={find_service[0]}"
        response = requests.get(info_url)
        if response.status_code == 200:
            response = response.json()
            client_id = find_service[0]
            members_key = [

            [

                Button.inline(bot_text["one_member"], str.encode("one_ex_service:" + str(client_id))),

            ],

            [

                Button.inline(bot_text["two_member"], str.encode("two_ex_service:" + str(client_id))),

            ],

            [

                Button.inline(bot_text["three_member"], str.encode("three_ex_service:" + str(client_id))),

            ]

        ]

            await bot.send_message(user_id, bot_text["select_ex_plan"], buttons=members_key)
        else:
            await event.reply(bot_text["cant_request_info"])
@bot.on(events.CallbackQuery(pattern="one_ex_service:*"))
async def one_ex_service(event):
    user_id = event.sender_id

    is_ban = config.is_ban(user_id)

    if is_ban:

        await event.reply(bot_text["you_banned"])

        return
    username = event.data.decode().split(":")[1]
    buttons = []

    for key, value in config.one_member_names.items():

        buttons.append([Button.inline(value, data=str.encode("plan_ex_service:" + str(key) + ":" + str(username)))])

    await event.reply(bot_text["select"], buttons=buttons)
@bot.on(events.CallbackQuery(pattern="two_ex_service:*"))
async def two_ex_service(event):
    user_id = event.sender_id

    is_ban = config.is_ban(user_id)

    if is_ban:

        await event.reply(bot_text["you_banned"])

        return
    username = event.data.decode().split(":")[1]
    buttons = []

    for key, value in config.two_member_names.items():

        buttons.append([Button.inline(value, data=str.encode("plan_ex_service:" + str(key) + ":" + str(username)))])

    await event.reply(bot_text["select"], buttons=buttons)
@bot.on(events.CallbackQuery(pattern="three_ex_service:*"))
async def three_ex_service(event):
    user_id = event.sender_id

    is_ban = config.is_ban(user_id)

    if is_ban:

        await event.reply(bot_text["you_banned"])

        return
    username = event.data.decode().split(":")[1]
    buttons = []

    for key, value in config.three_member_names.items():

        buttons.append([Button.inline(value, data=str.encode("plan_ex_service:" + str(key) + ":" + str(username)))])

    await event.reply(bot_text["select"], buttons=buttons)
@bot.on(events.CallbackQuery(pattern="plan_ex_service:*"))
async def plan_ex_service(event):
    user_id = event.sender_id
    service_num = int(event.data.decode().split(":")[1])
    username = str(event.data.decode().split(":")[2])
    amount = config.amounts[service_num]

    service_name = None

    try:

        service_name = config.one_member_names[service_num]

    except KeyError:

        try:

            service_name = config.two_member_names[service_num]

        except KeyError:

            service_name = config.three_member_names[service_num]

    keys = [

        [

            Button.inline(bot_text["pay_and_active_ex"], str.encode("buy_ex_wallet:" + str(service_num) + ":" + str(username)))

        ],

        # [

        #     Button.inline(bot_text["pay"], str.encode("pay_service:" + str(service_num)))

        # ]

    ]

    await event.reply(bot_text["pay_replay_ex"].format(amount=amount, service=service_name), buttons=keys)
@bot.on(events.CallbackQuery(pattern="buy_ex_wallet:*"))
async def buy_ex_wallet(event):
    user_id = event.sender_id

    is_ban = config.is_ban(user_id)

    if is_ban:

        await event.reply(bot_text["you_banned"])

        return

    await bot.delete_messages(user_id, event.original_update.msg_id)

    service_num = int(event.data.decode().split(":")[1])
    username = event.data.decode().split(":")[2]

    find_amount = config.amounts[service_num]

    user_inventory = cur.execute(f"SELECT inventory FROM users WHERE user_id = {user_id}").fetchone()[0]

    if user_inventory - int(find_amount) < 0:

        await event.reply(bot_text["none_inventory"])

    else:

        keys = [

            Button.inline(bot_text["yes"], str.encode("wallet_ex_yes:" + str(service_num) + ":" + str(username))),

            Button.inline(bot_text["no"], b'wallet_no'),

        ]

        service_name = None

        try:

            service_name = config.one_member_names[service_num]

        except KeyError:

            try:

                service_name = config.two_member_names[service_num]

            except KeyError:

                service_name = config.three_member_names[service_num]

        await event.reply(bot_text["pay_wallet_sure"].format(service=service_name), buttons=keys)
@bot.on(events.CallbackQuery(pattern="wallet_ex_yes:"))
async def wallet_ex_yes(event):
    msg_id = event.original_update.msg_id

    user_id = event.sender_id

    is_ban = config.is_ban(user_id)

    if is_ban:

        await event.reply(bot_text["you_banned"])

        return

    service_num = int(event.data.decode().split(":")[1])
    username = event.data.decode().split(":")[2]
    amount = config.amounts[service_num]

    await bot.delete_messages(user_id, msg_id)

    user_inventory = cur.execute(f"SELECT inventory FROM users WHERE user_id={user_id}").fetchone()[0]

    user_inventory = int(user_inventory) - int(amount)

    cur.execute(f"UPDATE users SET inventory = {user_inventory} WHERE user_id = {user_id}")

    to = cur.execute(f"SELECT phone FROM users WHERE user_id = {user_id}").fetchone()[0]

    db.commit()

    loading = await event.reply(bot_text["loading_account"])
    print(username)
    url = f"{config.API_ADDRESS}service-extension/?number={service_num}&username={username}"

    response = requests.get(url=url)


    if response.status_code == 200:
        await event.reply(bot_text["ss_ex"])
    else:

        user_inventory = cur.execute(f"SELECT inventory FROM users WHERE user_id={user_id}").fetchone()[0]

        user_inventory = int(user_inventory) + int(amount)

        cur.execute(f"UPDATE users SET inventory = {user_inventory} WHERE user_id = {user_id}")

        db.commit()

        await event.reply(bot_text["cant_make_service"])
@bot.on(events.CallbackQuery(pattern="sr_vl:"))
async def sr_vl(event):
    username = event.data.decode().split(":")[1]
    url = f"{config.API_ADDRESS}client-info?username={username}"
    response = requests.get(url=url)
    response = response.json()
    sub_link = response["info"]["subscription_link"]
    text = f"""
❕لینک v2ray جهت استفاده برای آیفون، اندروید در صورت اضطراری بودن

❗️توجه کنید استفاده از این اپشن فقط در صورت اضطراری بودن میباشد.

⚜️ اپلیکیشن اختصاصی همیشه بهترین سرورها رو دارد .

لینک سابسکرایب:

{sub_link}

"""
    await event.reply(text)
@bot.on(events.CallbackQuery(pattern="sr_ot:"))
async def sr_ot(event):
    username = event.data.decode().split(":")[1]
    url = f"{config.API_ADDRESS}client-info?username={username}"
    response = requests.get(url=url)
    response = response.json()
    sub_link = response["info"]["outline_link"]
    text = f"""
❕لینک اوتلاین جهت استفاده برای آیفون، اندروید در صورت اضطراری بودن

❗️توجه کنید استفاده از این آپشن فقط در صورت اضطراری بودن میباشد.

⚜️ اپلیکیشن اختصاصی همیشه بهترین سرورها رو دارد .

لینک اوتلاین :

`{sub_link}`
"""
    await event.reply(text)
@bot.on(events.CallbackQuery(pattern="sr_inf:"))
async def sr_inf(event):
    username = event.data.decode().split(":")[1]
    url = f"{config.API_ADDRESS}client-info?username={username}"
    response = requests.get(url=url)
    response = response.json()
    split_time = response["info"]["date_to"].split("-")
    year, month, day = int(split_time[0]), int(split_time[1]), int(split_time[2])
    miladi_date = jdatetime.datetime(year, month, day).date()
    shamsi_date = jdatetime.date.fromgregorian(date=miladi_date).__str__()
    keys = [
        [Button.inline("انقضا"), Button.inline(shamsi_date)],
        [
            Button.inline("حجم کل"), Button.inline(f'{response["info"]["total"]}G')
        ],
        [
            Button.inline("حجم مصرفی"), Button.inline(f'{response["info"]["size"]}M')
        ],
        [
            Button.inline("حجم باقیمانده"), Button.inline(f'{response["info"]["full"]}G')
        ]
    ]
    text = f"""مشخصات سرویس
نام کاربری:{username}
    
    
پسورد:{response["info"]["password"]}
    """
    await event.reply(text, buttons=keys)


@bot.on(events.CallbackQuery(pattern="iphone_sr_inf:"))
async def iphone_sr_inf(event):
    username = event.data.decode().split(":")[1]
    user_info = await functions.get_info(username)
    used_traffic = user_info["used_traffic"]
    used_traffic = functions.bytes_to_gigabytes(used_traffic)
    keys = [
        # [Button.inline("انقضا"), Button.inline(user_info[])],
        # [
        #     Button.inline("حجم کل"), Button.inline(f"{response["info"]["total"]}G")
        # ],
        [
            Button.inline("حجم مصرفی"), Button.inline(f"{used_traffic}G")
        ],
        # [
        #     Button.inline("حجم باقیمانده"), Button.inline(f"{response["info"]["full"]}G")
        # ]
    ]
    text = f"""مشخصات سرویس
نام کاربری:{username}

    """
    await event.reply(text, buttons=keys)

@bot.on(events.CallbackQuery(pattern="sr_inf:"))
async def sr_inf(event):
    username = event.data.decode().split(":")[1]
    url = f"{config.API_ADDRESS}client-info?username={username}"
    response = requests.get(url=url)
    response = response.json()
    split_time = response["info"]["date_to"].split("-")
    year, month, day = int(split_time[0]), int(split_time[1]), int(split_time[2])
    miladi_date = jdatetime.datetime(year, month, day).date()
    shamsi_date = jdatetime.date.fromgregorian(date=miladi_date).__str__()
    keys = [
        [Button.inline("انقضا"), Button.inline(shamsi_date)],
        [
            Button.inline("حجم کل"), Button.inline(f'{response["info"]["total"]}G')
        ],
        [
            Button.inline("حجم مصرفی"), Button.inline(f'{response["info"]["size"]}M')
        ],
        [
            Button.inline("حجم باقیمانده"), Button.inline(f'{response["info"]["full"]}G')
        ]
    ]
    text = f"""مشخصات سرویس
نام کاربری:{username}


پسورد:{response["info"]["password"]}
    """
    await event.reply(text, buttons=keys)
@bot.on(events.CallbackQuery(pattern="iphone_sr_pep:"))
async def iphone_sr_pep(event):
    username = event.data.decode().split(":")[1]
    url = f"{config.panel_api_address}?method=devices&name={username}&ADMIN=SpeedConnect"
    response = requests.get(url=url)
    response = response.json()
    print(response)
    total_device = response["is_login"]
    print(total_device)
    if int(total_device) == 0:
        await event.reply(bot_text["no_device_found"])
    else:
        devices = response["devices"]
        text = f"""
    ⚠️ دستگاه ها :
    """
        keys = []
        for i in devices:
            print(i)
            key = [
                Button.inline(i)
            ]
            keys.append(key)
        await event.reply(text, buttons=keys)
bot.run_until_disconnected()

