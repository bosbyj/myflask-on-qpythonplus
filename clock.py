import time

import requests

from apscheduler.schedulers.blocking import BlockingScheduler


sched = BlockingScheduler()

@sched.scheduled_job('interval', minutes=20)
def timed_job_awake_your_app():
    print('awake app every 10 minutes.')
    url = 'https://bosbyj.herokuapp.com/'
    r = requests.get(url)
    print("--> r.content")
    print(r.content)

sched.start()
