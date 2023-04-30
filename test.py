import json
import requests
from werkzeug.wrappers import response
import gsearch
from googlesearch import Google
from dhooks import Webhook, Embed
from urllib.parse import quote
from flask import Flask, request
import os
import datetime
import time
import random
import string
cd = os.path.dirname(os.path.realpath(__file__))
app = Flask(__name__)
app.config['JSON_SORT_KEYS'] = False

webhook = "https://discord.com/api/webhooks/872562744241553408/vCulIHonAQk2AXbwF4LMF2RxDJRd0T70MR6WAPHbruOaC0KrAJBLuJEpHWiVJyka0SOh"
webhook = Webhook(webhook)




response = {"id":195,"g_id":183,"j":5000.0,"p_c":100,"s":2,"t":"trivium","max_q":10,"q":[{"id":1089,"nth":6,"time":0,"is_a":False,"t":"Gmultiple_choice","q":"Which of these words does not mean something that can be detected by a nose?","a":[{"id":3301,"a":"Aura"},{"id":3302,"a":"Aroma"},{"id":3303,"a":"Odor"}]}]}


class Question:
    def __init__(self,payload) -> None:
        self.id = payload.get("id")
        self.type = payload.get("t")
        self.totalQ = payload.get("max_q")
        self.questionDict = payload.get("q")[0]
        self.question = self.questionDict.get("q")
        if not self.question:
            self.question = self.questionDict.get("q_c")
        self.questionId = self.questionDict.get("id")
        self.questionNumber = self.questionDict.get("nth")
        self.questionType = self.questionDict.get("t")
        self.options = self.questionDict.get("a")
    
    def __str__(self):
        return json.dumps(response)

question = Question(response)

print(question.question)
