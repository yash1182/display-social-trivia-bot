from flask import Flask, request
import os
import json
import base64
import hashlib
import datetime
import time
import random
import string
import jwtHandling
cd = os.path.dirname(os.path.realpath(__file__))
app = Flask(__name__)
app.config['JSON_SORT_KEYS'] = False


currentVerifications = []

def generateVerification(number):
	global currentVerifications
	letters = string.ascii_lowercase
	verificationId = ''.join(random.choice(letters) for i in range(8)) + "-" + ''.join(random.choice(letters) for i in range(4)) + "-" +''.join(random.choice(letters) for i in range(3)) 
	#verificationId = "Dibg1KHeRWHabCOIpPgNY9BizX177s"
	otpCode = random.randint(1000,9999)
	print(f"New OTP: {otpCode}")
	json = {"number":number, "verificationId" : verificationId , "otp":otpCode}
	currentVerifications.append(json)
	return verificationId

def checkUserToken(token):
	with open("data.json") as f:
		data = json.load(f)
	users = data["users"]
	for user in users:
		if user["authToken"] == token:
			return {"success":True}
	return {"success":False}

def verifyAuth(request):
	headers = request.headers
	authToken = headers.get("Authorization")
	if not authToken:
		return {"error": "Auth not valid","errorCode": 105}
	authToken = authToken.replace("Bearer ","")
	if checkUserToken(authToken)["success"] is False:
		return {"error": "Auth not valid","errorCode": 105}
	return {"success":True}

@app.route('/verifications',methods=['GET','POST'])
def verifications():
    print(request)
    content = request.get_json()
    number = content.get("phone")
    json = {
    "verificationId": generateVerification(number),
    "phone": number,
    "retrySeconds": 10,"expires": "2020-09-04T02:03:58.312Z","callsEnabled": False }
    return json

def verifyCode(verificationId,code):
    for verifications in currentVerifications:
    	print(verifications["verificationId"]+" == "+verificationId)
    	print(str(code)+" == "+str(verifications["otp"]))
    	if verifications["verificationId"] == verificationId and int(verifications["otp"])==int(code):
    		return {"status":True,"number":verifications["number"]}
    		
    return {"status":False}

def getUserInfo(number):
	with open("data.json") as f:
		data = json.load(f)
	users = data["users"]
	for user in users:
		if number == user["number"]:
			pass

@app.route('/verifications/<verificationId>',methods=['POST'])
def verificationids(verificationId):
    print(request)
    
    content = request.get_json()
    code = content.get("code")
    if not code:
        json_data = {"error": "code is required","errorCode": 401}
        return json_data
    response = verifyCode(verificationId,code)
    if response["status"] is False:
        json_data = {"error": "That verification code is incorrect.","errorCode": 458}
        return json_data , 400
    else:
    	with open("data.json") as f:
    		data = json.load(f)
    	users = data["users"]
    	for user in users:
    		print()
    		if user["phoneNumber"] == response["number"]:
    			userId = user["userId"]
    			username = user["username"]
    			isAdmin = user["admin"]
    			isTester = user["tester"]
    			isGuest = user["guest"]
    			avatarUrl = user["avatarUrl"]
    			loginToken = user["loginToken"]
    			accessToken = user["accessToken"]
    			authToken = user["authToken"]
    			canEnterReferral = user["canEnterReferral"]
    			wasReferralDenied = user["wasReferralDenied"]
    			return {"auth":{"userId":userId, "username": username, "admin": isAdmin, "guest":isGuest,"avatarUrl":avatarUrl, "loginToken":loginToken, "accessToken":accessToken, "authToken":authToken, "canEnterReferral":canEnterReferral, "wasReferralDenied": wasReferralDenied} }

    	return {}

@app.route("/config/public",methods=["GET"])
def public():
    json = {
    "verification": {"provider": "p1"}, "showReferrals": True, "telemetry": { "enabled": True, "batchSize": 50, "host": "https://telemetry.prod.hype.space"}}
    return json


def checkUsernameAvailibility(username):
	with open("data.json","r") as f:
		data = json.load(f)
	users = data["users"]
	for user in users:
		if user["username"].lower() == username.lower():
			return False
	return True


@app.route("/users",methods=["POST"])
def users():
    print(request)
    content = request.get_json()
    country = content.get("country")
    language = content.get("language")
    username = content.get("username")
    verificationId = content.get("verificationId")
    if not username:
    	return {"error": "username is required","errorCode": 401}
    if checkUsernameAvailibility(username) is False:
    	return { "error": "That username is not available","errorCode": 101}
    if not verificationId:
    	return {"error": "verificationId is required","errorCode": 401}
    for verifications in currentVerifications:
    	if verifications["verificationId"] == verificationId:
    		number = verifications["number"]
    return jwtHandling.createNewUser(username,number)
    


@app.route("/usernames/available",methods=["POST"])
def checkUsernameAvailability():

	content = request.get_json()
	username = content.get("username")
	if not username:
		json_data = {"error": "username is required","errorCode": 401}
		return json
	if checkUsernameAvailibility(username) is False:
		json_data = { "error": "That username is not available","errorCode": 101}
		return json_data
	return {}

@app.route("/config",methods=["GET"])
def config():
	headers = request.headers
	with open("config.json") as f:
		json_data = json.load(f)
	return json_data


@app.route("/show-referrals",methods=["GET"])
def show_referrals():
	response = verifyAuth(request)
	if not response.get("success"):
		return response
	return {
	"title": "Enter a Referral Code",
	"subtitle": "Enter your code to get a free reward that will help you win HQ Fan Edition!",
	"shows": [{
		"vertical": "general",
		"display": {
			"title": "HQ Fan Edition",
			"accentColor": "#FFFFFF",
			"description": "Entering their code will also help your friend!",
			"logo": "https://cdn.prod.hype.space/static/channel/TRIVIA/Trivia@3x.png?v=3",
			"bgImage": "https://cdn.prod.hype.space/static/channel/TRIVIA/Trivia-frame.png"
		},
		"referredByUserId": None,
		"referredByUsername": None
	}],
	"canEnterReferral": True}

@app.route("/referral-code/valid",methods=["POST"])
def referralcode_valid():
	content = request.get_json()
	referralCode = content.get("referralCode")
	if not referralCode:
		return None , 500
	with open("data.json","r") as f:
		data = json.load(f)
	users = data["users"]

	for user in users:
		username = user["username"]
		if username.lower() == referralCode.lower():
			return {}
	return {"error": "The referral code is not valid.","errorCode": 465}



@app.route("/users/me/devices",methods=["POST"])
def users_me_devices():
	response = verifyAuth(request)
	if not response.get("success"):
		return response
	return {}


@app.route("/users/me/payouts",methods=["GET"])
def users_me_payouts():
	response = verifyAuth(request)
	if not response.get("success"):
		return response
	headers = request.headers
	authToken = headers.get("Authorization")
	authToken = authToken.replace("Bearer ","")
	with open("data.json") as f:
		data = json.load(f)
	f.close()
	users = data["users"]
	for user in users:
		if user["authToken"] == authToken:
			payouts = user["payouts"]
			balance = user["balance"]
			recentWins = user["recentWins"]
			charities = user["charities"]
			json_data = {"payouts":payouts,"balance":balance,"recentWins":recentWins,"charities":charities}
			return json_data
	

@app.route("/users/me",methods=["GET"])
def users_me():
	headers = request.headers
	authToken = headers.get("Authorization")
	authToken = authToken.replace("Bearer ","")
	response = verifyAuth(request)
	if not response.get("success"):
		return response
	with open("data.json") as f:
		data = json.load(f)
	f.close()
	users = data["users"]
	for user in users:
		if user["authToken"] == authToken:
			userId = user["userId"]
			avatarUrl = user["avatarUrl"]
			username = user["username"]
			created = user["created"]
			broadcasts = user["broadcasts"]
			featured = user["featured"]
			voip = user["voip"]
			deviceTokens = user["deviceTokens"]
			hasPhone = user["hasPhone"]
			phoneNumber = user["phoneNumber"]
			referralUrl = user["referralUrl"]
			lives = user["lives"]
			referred = user["referred"]
			referringUserId = user["referringUserId"]
			highScore = user["highScore"]
			gamesPlayed = user["gamesPlayed"]
			winCount = user["winCount"]
			blocked = False
			blocksMe = False
			preferences = user["preferences"]
			friendIds = user["friendIds"]
			achievementCount = user["achievementCount"]
			leaderboard = user["leaderboard"]
			items = user["items"]
			coins = user["coins"]
			stk = user["stk"]
			erase1s = user["erase1s"]
			pointsMultiplierCounts = user["pointsMultiplierCounts"]
			streakInfo = user["streakInfo"]
			json_data = {"userId":userId,"username":username, "avatarUrl":avatarUrl,"created":created,"broadcasts":broadcasts,"featured":featured,"voip":voip,"deviceTokens":deviceTokens,"hasPhone":hasPhone,"phoneNumber":phoneNumber,"referralUrl":referralUrl,"lives":lives,"referred":referred,"referringUserId":referringUserId,"highScore":highScore,"gamesPlayed":gamesPlayed,"winCount":winCount,"blocked":blocked,"blocksMe":blocksMe,"preferences":preferences,"friendIds":friendIds,"achievementCount":achievementCount,"leaderboard":leaderboard,"items":items,"coins":coins,"stk":stk,"erase1s":erase1s,"pointsMultiplierCounts":pointsMultiplierCounts,"streakInfo":streakInfo}
			return json_data


@app.route("/users/<userId>",methods=["GET"])
def user_userid(userId):
	userId = int(userId)
	response = verifyAuth(request)
	if not response.get("success"):
		return response
	with open("data.json","r") as f:
		data = json.load(f)
	users = data["users"]
	for user in users:
		if user["userId"]== userId:
			json_data = {"userId": user["userId"], "username": user["username"], "avatarUrl": user["avatarUrl"], "created": user["created"], "broadcasts": user["broadcasts"],"featured": user["featured"],"referralUrl": user["referralUrl"],"leaderboard":user["leaderboard"],"highScore": user["highScore"],"gamesPlayed": user["gamesPlayed"],"winCount": user["winCount"],"achievementCount": user["achievementCount"],"blocked": False,"blocksMe": False}
			return json_data
	return {"error": f"User profile not found! userId={userId}","errorCode": 404}

@app.route("/users/leaderboard",methods=["GET"])
def leaderboard(userId):
	#mode = request.args.get("mode"):
	mode = None
	if not mode:
		mode = 1
	mode = int(mode)
	return {"data":[]}


@app.route("/opt-in",methods=["GET","POST"])
def optin():
	headers = request.headers
	authToken = headers.get("Authorization")
	authToken = authToken.replace("Bearer ","")
	response = verifyAuth(request)
	if not response.get("success"):
		return response
	if request.method == "GET":
		with open("data.json","r") as f:
			data = json.load(f)
		users = data["users"]
		for user in users:
			if user["authToken"] == authToken:
				return {"opts": user["opts"]}
	if request.method == "POST":
		content = request.get_json()
		if content.get("opt") != "hq-general":
			return 
		if not content.get("value"):
			return {"title": "HQ Fan Edition","opt": "hq-general","in": "Subscribe","out": "Subscribed","onboardingDescription": "Play trivia to win cash"}
		if type(content.get("value")) !=type(True):
			return

		with open("data.json","r") as f:
			data = json.load(f)
		f.close()
		users = data["users"]
		for user in users:
			if user["authToken"] == authToken:
				data["users"][users.index(user)]["opts"][0]["opted"] = content.get("value")
				with open("data.json","w") as f:
					json.dump(data,f)
				return {"opts": user["opts"]}


@app.route("/shows/schedule",methods=["GET"])
def shows_schedule():
	response = verifyAuth(request)
	if not response.get("success"):
		return response
	with open("shows.json") as f:
		json_data = json.load(f)
	f.close()
	return json_data

@app.route("/store/products",methods=["GET"])
def store_products():
	response = verifyAuth(request)
	if not response.get("success"):
		return response
	with open("products.json") as f:
		json_data = json.load(f)
	f.close()
	return json_data

if __name__ == '__main__':
    app.run(debug=True,host="172.31.45.34", port=80)
