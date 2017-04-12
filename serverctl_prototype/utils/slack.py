import requests
import json
import os


def send(data):
    data = str(data)
    if len(data) > 1000:
        data = data[:1000]
    requests.post(os.getenv('SLACK_ENDPOINT'), data=json.dumps({'text': data}))
