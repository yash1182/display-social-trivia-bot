from urllib.parse import quote_plus,parse_qs
import json
import requests
from bs4 import BeautifulSoup
import re
import collections
from googleapiclient.discovery import build

class googlesearch:
    API_KEY = "AIzaSyBmnGrKfDNJ-NMvFRd_tpnUN8LTuPqjqNU"
    BASE_URL = "https://www.googleapis.com/customsearch/v1"
    def __init__(self,question,options):
        self.question = question
        self.options = options
        self.session = requests.Session()
    def results(self):
        query=self.question.replace(" ","+")
        googlelink = "https://www.google.com/search?q="
        url = f"{googlelink}{query}&num=50"
        headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.127 Safari/537.36',}
        page = self.session.get(url,headers=headers).text
        soup = BeautifulSoup(page, 'html.parser')
        print(soup)
        found_results=[]
        titles = soup.find_all('h3')
        print(titles)
        descriptions = soup.find_all('span')#, attrs={'class': 'aCOpRe'})
        response = {'scores': {}}
        ignorelist = ['a','the','The','A','As',"not","NOT","Not"]
        #finding same words
        checkList = []
        for option in self.options:
            optionList = option.split(" ")
            checkList = checkList + optionList
        ignorelist = ignorelist + [item for item, count in collections.Counter(checkList).items() if count > 1]
        ignorelist = [x.lower() for x in ignorelist]
        for option in self.options:
            response['scores'][option] = 0
            optionlist = option.split(" ")
            optionList = [x.lower() for x in optionlist]
            for ignore in ignorelist:
                if ignore in optionlist:
                    optionlist.remove(ignore)
            for desc in descriptions:
                for abc in optionlist:
                    if abc.lower() in desc.text.lower().replace("\n"," "):
                        response['scores'][option]+=1
            for desc in titles:
                for abc in optionlist:
                    if abc.lower() in desc.text.lower().replace("\n"," "):
                        response['scores'][option]+=1
        return response

    def wiki(self):
        query=self.question.replace(" ","+")
        googlelink = "https://www.google.com/search?q="
        url = f"{googlelink}SITE:wikipedia%20{query}&num=50"
        headers = {'User-Agent':'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:72.0) Gecko/20100101 Firefox/72.0'}
        page = requests.get(url,headers=headers).text
        soup = BeautifulSoup(page, 'html.parser')
        found_results=[]
        titles = soup.find_all('h3')
        descriptions = soup.find_all('span', attrs={'class': 'st'})
        response = {'scores': {}}
        ignorelist = ['a','the','The','A','As',"not","NOT","Not"]
        #finding same words
        checkList = []
        for option in self.options:
            optionList = option.split(" ")
            checkList = checkList + optionList
        ignorelist = ignorelist + [item for item, count in collections.Counter(checkList).items() if count > 1]
        ignorelist = [x.lower() for x in ignorelist]
        for option in self.options:
            response['scores'][option] = 0
            optionlist = option.split(" ")
            optionList = [x.lower() for x in optionlist]
            for ignore in ignorelist:
                if ignore in optionlist:
                    optionlist.remove(ignore)
            for desc in descriptions:
                for abc in optionlist:
                    if abc.lower() in desc.text.lower().replace("\n"," "):
                        response['scores'][option]+=1
                for desc in titles:
                    if abc.lower() in desc.text.lower().replace("\n"," "):
                        response['scores'][option]+=1

        return response
    
    def getDirect(self):
        query=self.question.replace(" ","%20")
        googlelink = "https://www.google.com/search?q="
        url = f"{googlelink}{query}&num=50"
        headers = {'User-Agent':'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:72.0) Gecko/20100101 Firefox/72.0'}
        page = requests.get(url,headers=headers).text
        soup = BeautifulSoup(page, 'html.parser')
        directText=soup.find('div', {"data-attrid":"wa:/description"})
        if directText: return directText
        
    def custom(self):
        service = build("customsearch", "v1", developerKey=self.API_KEY)
        question = self.question.lower().replace("except","").replace("not","")
        options = " OR ".join(self.options)
        options = " OR ".join(self.options)
        query = f"{question} ({options})"
        response = service.cse().list(q=query, cx="fbfa655e16b2fd1d8").execute()
        titles = []
        descriptions = []
        scores = {'scores': {}}
        if response.get("items"):
            for item in response.get("items"):
                titles.append(item["title"])
                descriptions.append(item["snippet"])
            
        ignorelist = ['a','the','The','A','As',"not","NOT","Not"]
        #finding same words
        checkList = []
        for option in self.options:
            optionList = option.split(" ")
            checkList = checkList + optionList
        ignorelist = ignorelist + [item for item, count in collections.Counter(checkList).items() if count > 1]
        ignorelist = [x.lower() for x in ignorelist]
        for option in self.options:
            scores['scores'][option] = 0
            optionlist = option.split(" ")
            optionList = [x.lower() for x in optionlist]
            for ignore in ignorelist:
                if ignore in optionlist:
                    optionlist.remove(ignore)
            for desc in descriptions:
                for abc in optionlist:
                    if abc.lower() in desc.lower():
                        scores['scores'][option]+=1
                for desc in titles:
                    if abc.lower() in desc.lower():
                        scores['scores'][option]+=1

        return scores
            

# if __name__=="__main__":
#     options = ["Melpomene","polyhymnia","thalia"]
#     gsearch = googlesearch("The Greek drama masks represent all of the following figures",options)
#     scores = gsearch.custom()
#     print(scores)