from time import sleep
from celery.schedules import crontab
import pandas as pd
import os

from worker import celery

from client_bulksearch.es_operations import index_data

@celery.task(name="index_data")
def run_index_data(path = "/app/src/clients.csv"):
    # r = os.getcwd()
    data = pd.read_csv(path)
    data = data[['ClientName', 'ClientNumber']]
    r = index_data(data=data, index_name="client")
    return r


# example celery tasks and schedule conf

# @celery.task(name="generate_audio")
# def generate_audio():
#     spooled = generate()
#     return spooled


# @celery.task(name="process_data_task")
# def process_data_task(data):
#     df = pd.DataFrame(data)
#     sleep(5)
#     return df.to_json()


# @celery.task(name="test_task")
# def create_task(seconds):
#     sleep(int(seconds) * 10)
#     return True


# celery.conf.beat_schedule = {
#     "test": {
#         "task": "test_task",
#         "schedule": crontab(),
#         "args": (1,),
#     },
# }
