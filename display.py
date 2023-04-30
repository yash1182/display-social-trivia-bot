import json
import requests


authToken = "32a26e90e9372c23bf10ae8606df3161"

class displaySocial:
    def __init__(self,email,password) -> None:
        self.email = email
        self.password = password
        self.authToken = None
        self.appVersion = "2.2.6"
        self.versionCode = "109"
        self.deviceModel = "samsung SM-G977N"
        self.userId = None
        self.login()

    def login(self):
        url = "https://api.tsuprod.com/api/v1/user/login"
        headers = {"x-api-key": "Lb1GVRNi6Qh1Mk7QXOTq9hVMES5pBzi7IiN0Yhw2",
        "app_version": self.appVersion,
        "version_code": self.versionCode,
        "device_model": self.deviceModel,
        "device_os": "Android",
        "device_os_version": "25",
        "content-type": "application/json; charset=UTF-8",
        "accept-encoding": "gzip",
        "user-agent": "okhttp/4.9.1"}
        payload = {"login":self.email,"password":self.password,"client_version":"2.2.6(109)","device_id":"android","device_type":"android"}
        response = requests.post(url,headers=headers,json=payload).json()
        if not response.get("error"):
            self.authToken = response['data']['auth_token']
            self.userId = response['data']['id']
        return(response)
    
    def messages(self):
        url = f"https://api.tsuprod.com/api/v1/messages/contacted-users?limit=20&access_token={self.authToken}"
        headers = {"x-api-key": "Lb1GVRNi6Qh1Mk7QXOTq9hVMES5pBzi7IiN0Yhw2",
        "app_version": self.appVersion,
        "version_code": self.versionCode,
        "device_model": self.deviceModel,
        "device_os": "Android",
        "device_os_version": "25",
        "content-type": "application/json; charset=UTF-8",
        "accept-encoding": "gzip",
        "user-agent": "okhttp/4.9.1"}
        response = requests.get(url,headers=headers).json()
        return response

    def user_info(self):
        url = f"https://api.tsuprod.com/api/v1/user/info?user_id={self.userId}&access_token={self.authToken}"
        headers = {"x-api-key": "Lb1GVRNi6Qh1Mk7QXOTq9hVMES5pBzi7IiN0Yhw2",
        "app_version": self.appVersion,
        "version_code": self.versionCode,
        "device_model": self.deviceModel,
        "device_os": "Android",
        "device_os_version": "25",
        "content-type": "application/json; charset=UTF-8",
        "accept-encoding": "gzip",
        "user-agent": "okhttp/4.9.1"}
        response = requests.get(url,headers=headers).json()
        return response

    def getAppConfig(self):
        url = f"https://api.tsuprod.com/api/v1/settings/app-configuration?access_token={self.authToken}"
        headers = {"x-api-key": "Lb1GVRNi6Qh1Mk7QXOTq9hVMES5pBzi7IiN0Yhw2",
        "app_version": self.appVersion,
        "version_code": self.versionCode,
        "device_model": self.deviceModel,
        "device_os": "Android",
        "device_os_version": "25",
        "content-type": "application/json; charset=UTF-8",
        "accept-encoding": "gzip",
        "user-agent": "okhttp/4.9.1"}
        response = requests.get(url,headers=headers).json()
        return response

    def getLiveStreamIVS(self):
        return self.getAppConfig().get("data").get("ivs_url")



if __name__ == "__main__":
    email = "ygygupta01@gmail.com"
    password = "9826141207Y@sh"
    obj = displaySocial(email,password)
    #obj.login()
    print(obj.getLiveStreamIVS())