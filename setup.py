import configparser
from sqlite3 import connect

db = connect("bot.db")
cur = db.cursor()
# cur.execute("DROP TABLE pay")
# cur.execute("DROP TABLE users")
# cur.execute("DROP TABLE test_account")
# cur.execute("DROP TABLE services")
# cur.execute("DROP TABLE iphone_services")
cur.execute(
    "CREATE TABLE IF NOT EXISTS users(user_id, inventory, phone, can_test, is_ban, access_code, has_access, user_type)")
cur.execute(
    "CREATE TABLE IF NOT EXISTS pay(user_id, amount, desc, phone, date_time, code, pay_through, track_id, pay_type, confirmation, media)")
cur.execute("CREATE TABLE IF NOT EXISTS test_account(user_id, username, password, end)")
cur.execute("CREATE TABLE IF NOT EXISTS services(user_id, username, password, service_num, random_num, created, end)")
cur.execute(
    "CREATE TABLE IF NOT EXISTS iphone_services(user_id, username, sub_link, plan_id, random_num, created, end)")
# cur.execute(f"ALTER TABLE test_account ADD send_notification {False}")
# cur.execute(f"ALTER TABLE users ADD user_type 'normal'")
users = cur.execute("SELECT user_id FROM test_account").fetchall()
for user in users:
    user_id = user[0]
    cur.execute(f"UPDATE users SET user_type = 'normal' WHERE user_id = {user_id}")
    db.commit()
# services = cur.execute("SELECT random_num FROM services").fetchall()
# for service in services:
#     user_id = service[0]
#     cur.execute(f"UPDATE services SET send_notification = {False} WHERE random_num = {user_id}")
# db.commit()
