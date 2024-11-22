import requests
import config
from datetime import datetime, timedelta
import random
import string
#
# url = "https://app-panelmyqp.ir/get.php?method=data_user&name=user_p_2702&ADMIN=SpeedConnect"
#
# response = requests.get(url)
# print(response)
# print(response.text)
# print(response.json())
# from jdatetime import datetime, date
#
# miladi_date = datetime(2024, 11, 22).date()
# shamsi_date = date.fromgregorian(date=miladi_date)
#
# print(shamsi_date)
def bytes_to_gigabytes(bytes, decimals=2):
    gigabytes = bytes / (1024 ** 3)
    return round(gigabytes, decimals)
def mega_to_bytes(mega):
    bytes = mega * 1048576
    return bytes
def gaga_to_byte(giga):
    gigabytes = giga * (1024 ** 3)
    return gigabytes
async def get_info(username):
    login_body = {
        "username": "mmd",
        "password": "mmd",
    }
    login_token = requests.post(f"{config.MARZBAN_API_URL}admin/token", data=login_body).json()["access_token"]
    user_info = f"{config.MARZBAN_API_URL}user/{username}"
    user_info = requests.get(user_info, headers={"Authorization": f"Bearer {login_token}"}).json()
    return user_info

async def get_iphone_service(expire, data_limit):
    login_body = {
        "username": "mmd",
        "password": "mmd",
    }
    login_token = requests.post(f"{config.MARZBAN_API_URL}admin/token", data=login_body).json()["access_token"]
    print(login_token)
    username = f"user_{random.choice(string.ascii_letters)}_{random.randint(1000, 9999)}"
    headers = {
        "accept": "application/json",
        "Authorization": f"Bearer {login_token}",
        "content-type": "application/json",
    }
    print(username)
    print(expire)
    data = {"username": username,"proxies": {"vless": {}},"inbounds": {"vless": ["deco", "info", "upgrade"]},"expire": 0,"data_limit": data_limit,"data_limit_reset_strategy": "no_reset","status": "on_hold","note": "","on_hold_timeout": "2023-11-03T20:30:00","on_hold_expire_duration": expire}
    request = f"{config.MARZBAN_API_URL}user/"
    response = requests.post(request, json=data, headers=headers)
    sub = response.json()["subscription_url"]
    if response.status_code != 200:
        return None
    else:
        return username, sub

def calculate_date_difference(original_date, days):
    # Convert the original date to a datetime object
    date_obj = datetime.strptime(original_date, '%Y-%m-%d')

    # Add the specified number of days to the original date
    new_date = date_obj + timedelta(days=int(days))

    # Calculate the number of days between the original date and the new date
    date_difference = (new_date - date_obj).days

    return date_difference

iphone_data_limits = {2: 16106127360, 3: 53687091200, 4: 53687091200, 5: 75161927680, 6: 107374182400, 7: 161061273600, 8: 268435456000, 9: 214748364800, 10: 536870912000, 11: 75161927680, 12: 107374182400, 13: 161061273600, 14: 268435456000, 15: 322122547200, 16: 53687091200, 17: 75161927680, 18: 107374182400, 19: 161061273600, 20: 268435456000, 21: 322122547200}
# for i, g in iphone_data_limits.items():
#     iphone_data_limits[i] = gaga_to_byte(g)
# print(iphone_data_limits)