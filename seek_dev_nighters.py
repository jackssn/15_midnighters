import requests
import json
import pytz
from datetime import datetime


def load_attempts():
    data = []
    page_number = 0
    while 1:
        page_number += 1
        url = 'http://devman.org/api/challenges/solution_attempts/?page=%s' % page_number
        r = requests.get(url)
        if r.status_code == 200:
            page_data = json.loads(r.text)
            data += page_data['records']
        else:
            break
    return data


def get_midnighters(data):
    fmt = '%H:%M:%S'
    users = set()
    for action in data:
        username = action['username']
        timestamp = action['timestamp']
        timezone = action['timezone']
        if timestamp:
            utc_dt = datetime.utcfromtimestamp(timestamp).replace(tzinfo=pytz.utc)
            user_tz = pytz.timezone(timezone)
            user_dt = user_tz.normalize(utc_dt.astimezone(user_tz))
            upload_time = datetime.strptime(user_dt.strftime(fmt), "%H:%M:%S").time()
            midnight = datetime.strptime('0:0:0', "%H:%M:%S").time()
            morning = datetime.strptime('6:0:0', "%H:%M:%S").time()
            if midnight < upload_time < morning:
                users.add(username)
    return users


def print_midnighters(users):
    for user in sorted(users):
        print(user)


if __name__ == '__main__':
    data = load_attempts()
    midnighters = get_midnighters(data)
    print_midnighters(midnighters)
