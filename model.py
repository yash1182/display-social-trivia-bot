import requests
import websocket
import json
from gsearch import googlesearch
import threading

from urllib.parse import quote

from dhooks import Webhook, Embed


#webhook = "https://discord.com/api/webhooks/878429628144943124/le_OdUu2EuMey9unrTvuAGGpjKzTIDJ7Y4ECMKBeN0spMCaSbjFFMwZM8EZxBL5HSpau"
webhook = "https://discord.com/api/webhooks/695323528102150256/adOHWzqXwxDxvLISn9gVuFrteTe2sAa_iCG7a6G0hQhfLvPdjH4ivjohHIAZFQ-MWYES"
webhook = Webhook(webhook)


from urllib.parse import quote


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

questions = []
results = []

def on_message(message:dict):
    #message = json.loads(message)
    if message.get("t") =="trivium":
        questionObj = Question(message)
        if questionObj.question in [question.question for question in questions]:
            return
        questions.append(questionObj)
        question = questionObj.question
        questionNumber = questionObj.questionNumber
        totalQuestion = questionObj.totalQ
        try:
            options = [option["a"] for option in questionObj.options]
        except Exception:
            options = [option["a_c"] for option in questionObj.options]
        option1 = options[0]
        option2 = options[1]
        option3 = options[2]
        googlelink = f"https://www.google.com/search?&rlz=1C1ONGR_enIN958IN958&aqs=chrome..69i57j69i64l2j69i60.361j0j7&sourceid=chrome&ie=UTF-8&q="
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
        gsearch = googlesearch(question,options)
        #response = gsearch.results()
        response = gsearch.custom()
        if response.get("scores"):
            score = response['scores']
            embed = Embed(title=f"Results:",description=f"**{options[0]}: {score[options[0]]}\n{options[1]}: {score[options[1]]}\n{options[2]}: {score[options[2]]}**",color=0xff0000)
            #embed.set_footer(text="The Unfortunate Guy#7835 | Display Trivia |")
            webhook.send(embed=embed)
        directText = gsearch.getDirect()
        if directText:
            print(directText.text)
            embed = Embed(title="Direct Result Found!",description=f"**{directText.text}**",color=0x800080)
            embed.set_footer(text="The Unfortunate Guy#7835 | HQ Trivia |")
            webhook.send(embed=embed)
            return
message ={"id":1070,"g_id":1076,"j":500,"p_c":100,"s":2,"t":"trivium","max_q":10,"q":[{"id":4010,"nth":1,"time":0,"is_a":False,"t":"multiple_choice","q":"A dog’s tail does this:","a":[{"id":12223,"a":"Tells lies"},{"id":12222,"a":"Spits"},{"id":12221,"a":"Wags"}]}]}
message = {"id":1070,"g_id":1076,"j":500,"p_c":100,"s":2,"t":"trivium","max_q":10,"q":[{"id":4011,"nth":2,"time":0,"is_a":False,"t":"multiple_choice","q":"Which of the following is not a utensil?","a":[{"id":12226,"a":"Digeridoo"},{"id":12225,"a":"Chopstick"},{"id":12224,"a":"Fork"}]}]}
message = {"id":1070,"g_id":1076,"j":500,"p_c":100,"s":2,"t":"trivium","max_q":10,"q":[{"id":4013,"nth":4,"time":0,"is_a":False,"t":"multiple_choice","q":"Miu Miu recently went viral with this:","a":[{"id":12232,"a":"A wedge sandal"},{"id":12231,"a":"A micro mini skirt"},{"id":12230,"a":"A scarf"}]}]}
message  = {"id":1070,"g_id":1076,"j":500,"p_c":100,"s":2,"t":"trivium","max_q":10,"q":[{"id":4014,"nth":5,"time":0,"is_a":False,"t":"multiple_choice","q":"What is on the wallpaper in Andy’s room in Toy Story?","a":[{"id":12235,"a":"Stripes"},{"id":12234,"a":"Clouds"},{"id":12233,"a":"Pine trees"}]}]}
message = {"id":1070,"g_id":1076,"j":500,"p_c":100,"s":2,"t":"trivium","max_q":10,"q":[{"id":4015,"nth":6,"time":0,"is_a":False,"t":"multiple_choice","q":"All are original cast members of “Jersey Shore” except","a":[{"id":12238,"a":"Mike “The Situation”"},{"id":12237,"a":"Pauly D"},{"id":12236,"a":"DiMarco Baby"}]}]}

on_message(message)