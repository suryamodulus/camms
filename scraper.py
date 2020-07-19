import requests
from bs4 import BeautifulSoup
from tinydb import TinyDB,Query,where
import time
import os
import animation
from collector import Collect
from voiceover import VoiceOver
from clipmaker import ClipMaker


# Init Database
open('db.json', 'a').close()
db = TinyDB('db.json')
Articles = Query()

 
def initScrape(targetUrl):
	r= requests.get(targetUrl)
	data=r.text
	return BeautifulSoup(data,features="html.parser")

def getTitle(soup):
	return soup.title.string.split('-')[0].strip()

def getNumOfMethods(soup):
	num = 0
	for item in soup.find_all(class_="altblock"):
		try: 
			num = item.find('span').text
		except:
			pass
	return int(num)

def getAllSteps(soup):
	s_data = []
	for i,step in enumerate(soup.find_all(class_="hasimage")):
		try:
			step_num = i+1
			step_title = step.find(class_="whb").text
			step_detail = step.find(class_="step").text
			step_img = step.find("img",class_="whcdn").get('data-src')
			s_data.append({'s_num':step_num,'s_title':step_title,'s_detail':step_detail,'s_img':step_img})
			continue
		except:
			pass
		try:
			step_num = i+1
			step_title = step.find(class_="whb").text
			step_detail = step.find(class_="step").text
			step_img = step.find("video").get('data-poster')
			s_data.append({'s_num':step_num,'s_title':step_title,'s_detail':step_detail,'s_img':step_img})
			continue
		except:
			pass
	return {'m_title':None,'steps':s_data}

def getAllMethods(soup):
	methods = []
	for method in soup.find_all(attrs={'class':["section", "steps"]}):
	    if(method.find("span").text.isdigit()):
	    	methods.append(method.find(class_="mw-headline").text)
	return methods

def getAllMethodSteps(methods,soup):
	data = []
	for i,method in enumerate(methods):
		for steps in soup.find_all(attrs={'id':"steps_"+str(i+1)}):
			s_data=[]
			for i,step in enumerate(steps.find_all(class_="hasimage")):
				try:
					step_num = i+1
					step_title = step.find(class_="whb").text
					step_detail = step.find(class_="step").text
					step_img = step.find("img",class_="whcdn").get('data-src')
					s_data.append({'s_num':step_num,'s_title':step_title,'s_detail':step_detail,'s_img':step_img})
					continue
				except:
					pass
				try:
					step_num = i+1
					step_title = step.find(class_="whb").text
					step_detail = step.find(class_="step").text
					step_img = step.find("video").get('data-poster')
					s_data.append({'s_num':step_num,'s_title':step_title,'s_detail':step_detail,'s_img':step_img})
					continue
				except:
					pass
			data.append({'m_title':method,'steps':s_data})
	return data

loader = (': ','\u02D9\u02D9',' :','..')
@animation.wait(loader,'\u2744\u0020Scraping\u0020')
def Scrape(url):
	#soup = initScraper("https://www.wikihow.com/Buy-a-Home-With-No-Money-Down")
	soup = initScrape(url)
	title = getTitle(soup)
	if(db.search(where('url')==url)):
		print("\u0020Article Already Scraped.")
		return 0
	nm = getNumOfMethods(soup)
	if(nm==0):
		data=getAllSteps(soup)
	else:
		methods = getAllMethods(soup)
		data = getAllMethodSteps(methods,soup)
	db.insert({'url':url,'title':title,'content':data,'collected':False,'voiced':False,'clipsmade':False,'captioned':False,'timestamp':time.time()})
	print("\u0020Finished Scraping Article.")


if __name__ == '__main__':
	Scrape("https://www.wikihow.com/Connect-PC-to-TV")
	Collect("https://www.wikihow.com/Connect-PC-to-TV")
	VoiceOver("https://www.wikihow.com/Connect-PC-to-TV")
	ClipMaker("https://www.wikihow.com/Connect-PC-to-TV")