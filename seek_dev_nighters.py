import requests
import json
import pytz
from datetime import datetime


def load_attempts():
    page_number = 0
    while 1:
        page_number += 1
        payload = {'page': page_number}
        r = requests.get('http://devman.org/api/challenges/solution_attempts/', params=payload)
        if r.status_code == 200:
            data_page = json.loads(r.text)
            yield data_page['records']
        else:
            break


def get_midnighters(solved_tasks):
    fmt = '%H:%M:%S'
    users = set()
    for task in solved_tasks:
        username = task['username']
        timestamp = task['timestamp']
        timezone = task['timezone']
        if timestamp:
            utc_dt = datetime.utcfromtimestamp(timestamp).replace(tzinfo=pytz.utc)
            user_tz = pytz.timezone(timezone)
            user_dt = user_tz.normalize(utc_dt.astimezone(user_tz))
            upload_time = user_dt.time()
            midnight = datetime.strptime('0:0:0', fmt).time()
            morning = datetime.strptime('6:0:0', fmt).time()
            if midnight <= upload_time < morning:
                users.add(username)
    return users


def print_midnighters(owls):
    print("Night owls on DevMan.org:")
    for i, owl in enumerate(sorted(owls)):
        print("%s) %s" % (i+1, owl))


if __name__ == '__main__':
    api_data = []
    for x in load_attempts():
        api_data += x
    print_midnighters(get_midnighters(solved_tasks=api_data))
