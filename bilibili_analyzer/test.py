import redis

REDIS_SETTINGS = {
    'host': '47.94.104.237',
    'db': 7,
    'password': 'hacker_died',
    'decode_responses': True
}

connect = redis.Redis(**REDIS_SETTINGS)
count = 0
total_length = len(connect.keys())

for index, user in enumerate(connect.keys()):
    if index % 1000 == 0:
        print(f"{index + 1} / {total_length}")

    if len(connect.smembers(user)) < 2:
        print(f"{index + 1} {user}")
