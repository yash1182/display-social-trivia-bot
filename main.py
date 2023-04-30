import json
import requests
import gsearch
from dhooks import Webhook, Embed
from urllib.parse import quote
from flask import Flask, request
from flask_cors import CORS
import os
import datetime
import time
import random
import subprocess
import string
cd = os.path.dirname(os.path.realpath(__file__))
app = Flask(__name__)
CORS(app)
app.config['JSON_SORT_KEYS'] = False

webhook = "https://discord.com/api/webhooks/885314007202938971/TymHteUlytp428RuaCDANyB348Rz4bpTMlXqdI7b8oY0qB3A3h-RLh_F2VpfMFt-1ifA"
webhook = Webhook(webhook)
webhook2 = "https://discord.com/api/webhooks/878429628144943124/le_OdUu2EuMey9unrTvuAGGpjKzTIDJ7Y4ECMKBeN0spMCaSbjFFMwZM8EZxBL5HSpau"
webhook2 = Webhook(webhook2)
webhook3 = Webhook("https://discord.com/api/webhooks/889959436221825024/PG5SoPx81quw62DmmXTaatETd2BF67kt4lJ17ExcKcfLW_KVIduIJ0buI4oF85_Yyjdj")

questions = []
results = []

class Question:
    def __init__(self,payload) -> None:
        self.payload = payload
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
        return json.dumps(self.payload)
class Result:
    def __init__(self,payload) -> None:
        self.payload = payload
        self.type = payload.get("t")
        self.totalQ = payload.get("max_q")
        self.questionDict = payload.get("q")[0]
        self.question = self.questionDict.get("q_c")
        self.questionId = self.questionDict.get("id")
        self.questionNumber = self.questionDict.get("nth")
        self.questionType = self.questionDict.get("t")
        self.options = self.questionDict.get("a")
    def __str__(self):
        return json.dumps(self.payload)

@app.route("/displaytv",methods=["POST"])
def displayTrivia():
    global questions
    response = request.get_json()
    if response.get("t") =="trivium":
        questionObj = Question(response)
        print(questionObj.questionId in [question.questionId for question in questions])
        if questionObj.question in [question.question for question in questions]:
            return {}
        questions.append(questionObj)
        question = questionObj.question
        questionNumber = questionObj.questionNumber
        totalQuestion = questionObj.totalQ
        try:
            options = [option["a"] for option in questionObj.options]
        except Exception:
            options = [option["a_c"] for option in questionObj.options]
        print(options)
        option1 = options[0]
        option2 = options[1]
        option3 = options[2]
        googlelink = f"https://google.com/search?q="
        ducklink = f"https://duckduckgo.com/?q="
        allOptions = f'+("{option1}" OR "{option2} OR "{option3}")'
        googleWOAnswers = googlelink+quote(f'{question}')
        googleWAnswers = googleWOAnswers+quote(f'{allOptions}')
        duckWOAnswers = ducklink+quote(f'{question}')
        duckWAnswers = duckWOAnswers+quote(f'{allOptions}')
        option1Link = googleWOAnswers+quote(f'{option1}')
        option2Link = googleWOAnswers+quote(f'{option2}')
        option3Link = googleWOAnswers+quote(f'{option3}')
        embed = Embed(title=f"{question}",url=googleWOAnswers,description=f"[{option1}]({option1Link})\n\n[{option2}]({option2Link})\n\n[{option3}]({option3Link})\n\n",color=0x5761ee)
        embed.add_field(name="Google:",value=f"[Google]({googleWOAnswers})\n\n[Google W/Options]({googleWAnswers})")
        embed.add_field(name="Duck Duck Go:",value=f"[Duck]({duckWOAnswers})\n\n[Duck W/Options]({duckWAnswers})")
        embed.set_author(name=f"Question {questionNumber} out of {totalQuestion}")
        #embed.set_footer(text="The Unfortunate Guy#7835 | Display Trivia |")
        webhook.send(embed=embed)
        webhook2.send(embed=embed)
        webhook3.send(embed=embed)
        response = gsearch.googlesearch(question,options).results()
        if response.get("scores"):
            score = response['scores']
            embed = Embed(title=f"Results:",description=f"**{options[0]}: {score[options[0]]}\n{options[1]}: {score[options[1]]}\n{options[2]}: {score[options[2]]}**",color=0xff0000)
            #embed.set_footer(text="The Unfortunate Guy#7835 | Display Trivia |")
            webhook.send(embed=embed)
            webhook2.send(embed=embed)
        
        return {"status":"success"}
    if response.get("t") =="results":
        resultObj = Question(response)
        print(response)
        print(resultObj.questionId in [question.questionId for question in questions])
        if resultObj.question in [question.question for question in questions]:
            return {}
        questions.append(resultObj)
        question = resultObj.question
        questionNumber = resultObj.questionNumber
        totalQuestion = resultObj.totalQ
        options = [option["a_c"] for option in resultObj.options]
        option1 = options[0]
        option2 = options[1]
        option3 = options[2]
        for option in resultObj.options:
            if option.get("c") is True:
                correctAnswer = option.get("a_c")
                break
        embed = Embed(title=f"{question}",description=f"{option1}\n\n{option2}\n\n{option3}\n\n",color=0x5761ee)
        embed.add_field(name="Correct Answer:",value=correctAnswer)
        embed.set_author(name=f"Question {questionNumber} out of {totalQuestion}")
        #embed.set_footer(text="The Unfortunate Guy#7835 | Display Trivia |")
        webhook.send(embed=embed)
        webhook2.send(embed=embed)
        webhook3.send(embed=embed)

    return {}

if __name__ == '__main__':
    #os.system(cd+'\index.html')
    app.run(debug=True,host="localhost", port=8080)


