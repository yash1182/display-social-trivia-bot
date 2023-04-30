import json
from turtle import color
import requests
from bs4 import BeautifulSoup
import re
from urllib.parse import quote_plus,parse_qs
import random

from dhooks import Webhook, Embed


webhook = "https://discord.com/api/webhooks/878429628144943124/le_OdUu2EuMey9unrTvuAGGpjKzTIDJ7Y4ECMKBeN0spMCaSbjFFMwZM8EZxBL5HSpau"
webhook = Webhook(webhook)


class Result:
    def __init__(question:str,) -> None:
        pass
class Google:
    def __init__(self,question:str,options:list) -> None:
        self.question:str = question
        self.options:list = options
        self.agents:tuple = ("Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.37",
                "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2227.1 Safari/537.36",
                "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2227.0 Safari/537.37",
                )
        self.session = requests.Session()
    def search(self):
        results = {"organic_results":[]}
        headers = {"user-agent":self.agents[random.randrange(len(self.agents))],
                   "Accept-Encoding": "gzip","Accept-Language":"en-US,en;q=0.9,es;q=0.8"}
        params = {"q":self.question,"num":"50"}
        question = self.question.lower().replace("except","").replace("not","")
        options = " OR ".join(self.options)
        query = f"{question} ({options})"
        query = quote_plus(query)
        # googlelink = "https://www.google.com/search"
        # query = f"{googlelink}?q={question}"
        query = f"https://www.google.com/search?q={query}"
        # print(query)
        response = self.session.get(query,headers=headers)
        with open("result.txt","w+") as f:
            f.write(response.text)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # print(soup)
        answer_description = soup.find("div",attrs={"class":"kCrYT"})
        # if len(answer_description)!=0:
        #     answer_description= answer_description[-1]
        if answer_description:
            results["direct_answer"] = {"description":answer_description.text}
            direct_answer = answer_description.find("span")
            if direct_answer: results["direct_answer"]["title"] = direct_answer.text
        search_result = soup.find_all("div",attrs={"class":"ZINbbc luh4tb xpd O9g5cc uUPGi"})
        for result in search_result:
            title = result.find("h3",attrs={"class":"zBAuLc l97dzf"}).text
            link = parse_qs(result.find("a").get("href")).get("url")
            if link: link = link[0]
            snippet = result.find("div",attrs={"class":"BNeawe s3v9rd AP7Wnd"}).text
            results["organic_results"].append({"title":title,"link":link,"snippet":snippet})
        return results

if __name__=="__main__":
    options = ["Melpomene","polyhymnia","thalia"]
    gsearch = Google("The Greek drama masks represent all of the following figures",options)
    response = gsearch.search()
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
        #webhook.send(embed=embed)
        