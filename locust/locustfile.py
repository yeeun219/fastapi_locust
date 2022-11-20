from locust import HttpUser, task
import pandas as pd
import random
import time

def str_time_prop(start, end, format, prop):
    stime = time.mktime(time.strptime(start, format))
    etime = time.mktime(time.strptime(end, format))

    ptime = stime + prop * (etime - stime)

    return time.strftime(format, time.localtime(ptime))

def random_date(start, end, prop):
    return str_time_prop(start, end, '%Y-%m-%d', prop)

print(random_date("2022-01-01", "2022-12-31", random.random()))
class WinePredictionUser(HttpUser):
    @task(1)
    def healthcheck(self):
        self.client.get("/healthcheck")

    @task(10)
    def prediction(self):
        test_date =  random_date("2022-01-01", "2022-12-31", random.random())
        query = {
            "days": test_date,
        }
        self.client.post("/predict", json=query)

