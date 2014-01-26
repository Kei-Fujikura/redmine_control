# -*- coding: utf-8-*-
import json
import requests


class PushTicket():
    def __init__(self):
        self.POSTData = {}
        self.REDMINE_API_KEY = '750bea02df04d19444c0a246f03696b7c126d256'
        self.REDMINE_HOST = 'http://fj-prg.cloudapp.net/redmine/issues.json'
        self.POST_HEADER = {
            'Content-Type': 'application/json',
            'X-Redmine-API-Key': self.REDMINE_API_KEY
        }

    def setMessage(self, payload):
        self.POSTData = json.dumps(payload)
        print(self.POSTData)

    def post(self):
        url = self.REDMINE_HOST+'?format=json'
        r = requests.request('POST', url, data=self.POSTData, headers=self.POST_HEADER)
        print(r)

if __name__ == "__main__":
    f_in = open("sample.json", "r", encoding='utf-8')
    dat = json.load(f_in)
    f_in.close()

    rsender = PushTicket()
    rsender.setMessage(dat)
    rsender.post()
