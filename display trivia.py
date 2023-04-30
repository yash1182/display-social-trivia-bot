import requests
import websocket
import json
from googlesearch import Google
from gsearch import googlesearch
import threading

from urllib.parse import quote

from dhooks import Webhook, Embed


webhook = "https://discord.com/api/webhooks/878429628144943124/le_OdUu2EuMey9unrTvuAGGpjKzTIDJ7Y4ECMKBeN0spMCaSbjFFMwZM8EZxBL5HSpau"
webhook = Webhook(webhook)

webhook2 = "https://discord.com/api/webhooks/695323528102150256/adOHWzqXwxDxvLISn9gVuFrteTe2sAa_iCG7a6G0hQhfLvPdjH4ivjohHIAZFQ-MWYES"
webhook2 = Webhook(webhook2)


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

class User(dict):
    def __getattr__(self, key):
        try:
            return self[key]
        except KeyError as k:
            raise AttributeError(k)
    def __setattr__(self, key, value):
        self[key] = value

    def __delattr__(self, key):
        try:
            del self[key]
        except KeyError as k:
            raise AttributeError(k)

    def __repr__(self):
        return '<User ' + dict.__repr__(self) + '>'

class Client:
    VERSION_CODE = "154"
    APP_VERSION = "2.4.0.3"
    VERSION = f"{APP_VERSION}({VERSION_CODE})"
    EMAIL = "ygygupta01@gmail.com"
    PASSWORD = "9826141207Y@sh"
    BASE_URL = "https://api.tsuprod.com/api/v1"
    LOGIN_URL = BASE_URL+"/user/login"
    WEBSOCKET_URL = "wss://trivia-websockets.tsuprod.com/"
    def __init__(self,email=None,password=None,version=None) -> None:
        self.email = self.password = self.version = None
        
        if email: self.email = email
        else: self.email = self.EMAIL
        
        if password: self.password = password
        else: self.password = self.PASSWORD

        if version: self.version = version
        else: self.version = self.VERSION
        
        self.authToken = None
        self.user:User = None
        self.ws = None
        
        self.subscribedId = None
        self.prev_question_number = 0
        self.prev_result_number = 0
        self.questions:list[Question] = []
        self.results:list[Result] = []
        self.polls:list = []
        
    def login(self):
        data = {"login":self.email,"password":self.password,"client_version":self.version,"device_id":"android","device_type":"android"}
        
        headers = {
            "x-api-key":"Lb1GVRNi6Qh1Mk7QXOTq9hVMES5pBzi7IiN0Yhw2",
            "content-type":"application/json; charset=UTF-8",
            "user-agent":"okhttp/4.9.1",
            "accept-encoding":"gzip",
            "version_code":self.VERSION_CODE,
            "device_os":"Android",
            "device_model":"motorola motorola one fusion+",
            "app_version":self.APP_VERSION
            }
        response = requests.post(self.LOGIN_URL,headers=headers,json=data)
        if response.status_code!=200:
            print(response.json().get("message"))
            exit()
        response = response.json()
        print(response)
        self.user = User(response["data"])
        return
    
    def getConfig(self):
        pass
    
    def connect(self):
        if self.ws!=None:
            return
        def on_open(ws):
            print("connected to ws")
        def on_message(ws,message):
            message = json.loads(message)
            #print(message)
            if message.get("type") == "games_list":
                if self.subscribedId!= None:
                    self.ws.send(json.dumps({"action":"unsubscribe","data":{"game_id":self.subscribedId}}))
                    self.subscribedId=None
                if message.get("data") and len(message["data"])!=0:
                    for data in message["data"]:
                        game_id = data["id"]
                        payload = {"action":"subscribe","data":{"game_id":game_id}}
                        self.ws.send(json.dumps(payload))
                        self.subscribedId = game_id
                        return
            if message.get("game_type")=="poll" and self.subscribedId!=None:
                    self.ws.send(json.dumps({"action":"unsubscribe","data":{"game_id":self.subscribedId}}))
            try:
                if message.get("t") =="trivium":
                    questionObj = Question(message)
                    # print(questionObj.questionId in [question.questionId for question in self.questions])
                    if questionObj.question in [question.question for question in self.questions]:
                        return
                    self.questions.append(questionObj)
                    question = questionObj.question
                    refinedQuestion = question.replace("except","").replace("not","")
                    questionNumber = questionObj.questionNumber
                    totalQuestion = questionObj.totalQ
                    try:
                        options = [option["a"] for option in questionObj.options]
                    except Exception:
                        options = [option["a_c"] for option in questionObj.options]
                    print(options)
                    # options.reverse()
                    option1 = options[0]
                    option2 = options[1]
                    option3 = options[2]
                    googlelink = f"https://google.com/search?q="
                    ducklink = f"https://duckduckgo.com/?q="
                    allOptions = f'+("{option1}" OR "{option2} OR "{option3}")'
                    googleWOAnswers = googlelink+quote(f'{refinedQuestion}')
                    googleWAnswers = googleWOAnswers+quote(f'{allOptions}')
                    duckWOAnswers = ducklink+quote(f'{refinedQuestion}')
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
                    gsearch = googlesearch(question,options)
                    #response = gsearch.results()
                    response = gsearch.custom()
                    if response.get("scores"):
                        score = response['scores']
                        embed = Embed(title=f"Results:",description=f"**{options[0]}: {score[options[0]]}\n{options[1]}: {score[options[1]]}\n{options[2]}: {score[options[2]]}**",color=0xff0000)
                        #embed.set_footer(text="The Unfortunate Guy#7835 | Display Trivia |")
                        webhook.send(embed=embed)
                        webhook2.send(embed=embed)
                    google = Google(question,options)
                    response = google.search()
                    print(response)
                    if response.get("direct_answer"):
                        embed = Embed(color=0x39FF14)
                        if response["direct_answer"].get("title"): 
                            embed.set_title(title=response["direct_answer"].get("title"))
                        if response["direct_answer"].get("description"): 
                            description = response["direct_answer"].get("description").lower()
                            for option in options:
                                if option.lower() in description:
                                    description = description.replace(option,f"**{option}**")
                            embed.description = description
                        webhook.send(embed=embed)    
                
                if message.get("game_type") == "trivium" and self.subscribedId!=None:
                    self.ws.send(json.dumps({"action":"unsubscribe","data":{"game_id":self.subscribedId}}))
                if message.get("t")=="poll":
                    
                    print(message)
                # if message.get("t") == "results":
                #     question_details = message.get("q")[0]
                #     question = question_details.get("q_c")
                #     question_number = question_details.get("nth")
                #     if self.prev_result_number == question_number:
                #         return
                #     correct_answer = ""
                #     for option_details in question_details["a"]:
                #          if option_details["c"] is True:
                #              correct_answer = option_details["a_c"]
                #              break
                #     if not correct_answer:
                #         return
                #     self.prev_result_number = question_number
                if message.get("t") =="results":
                    resultObj = Question(message)
                    # print(message)
                    if resultObj.question in [question.question for question in self.questions]:
                        return
                    self.questions.append(resultObj)
                    question = resultObj.question
                    questionNumber = resultObj.questionNumber
                    totalQuestion = resultObj.totalQ
                    options = [option["a_c"] for option in resultObj.options]
                    option1 = options[0]
                    option2 = options[1]
                    option3 = options[2]
                    correctAnswer = None
                    for option in resultObj.options:
                        if option.get("c") is True:
                            correctAnswer = option.get("a_c")
                            break
                    if not correctAnswer: return
                    embed = Embed(title=f"{question}",description=f"{option1}\n\n{option2}\n\n{option3}\n\n",color=0x5761ee)
                    embed.add_field(name="Correct Answer:",value=correctAnswer)
                    embed.set_author(name=f"Question {questionNumber} out of {totalQuestion}")
                    #embed.set_footer(text="The Unfortunate Guy#7835 | Display Trivia |")
                    webhook.send(embed=embed)
            except Exception as e:
                print(e)
                    
                        
        def on_error(ws,error):
            print(error)
        def on_close(ws,status,message):
            print(f"closed : {message}")
        websocket.enableTrace(False)
        headers = {"User-Agent":"okhttp/4.9.1","Accept-Encoding":"gzip","Sec-WebSocket-Extensions":"permessage-deflate","Sec-WebSocket-Protocol":"ebe15f21ac2249daa7297f83b4edc2b2"}
        self.ws = websocket.WebSocketApp("wss://trivia-websockets.tsuprod.com/",header=headers,on_open=on_open,on_message=on_message,on_error=on_error,on_close=on_close)
        self.ws.run_forever() 
        


if __name__ == "__main__":
    client =Client()
    #client.login()
    client.connect()
        