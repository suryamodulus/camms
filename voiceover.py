import urllib.request
from tinydb import TinyDB,Query,where
import os
import animation
from gtts import gTTS


# Init Database
open('db.json', 'a').close()
db = TinyDB('db.json')
Articles = Query()


cpath = os.getcwd()+"/collections/"


def Text2Audio(text,dirpath,fname,ext):
    tts = gTTS(text, lang='en')
    tts.save(f"{dirpath}/{fname}.{ext}")

def getArticle(url):
    return db.search((where('url')==url) & (where('voiced')==False))

def generateAudio(url,article):
    if(len(article)>0):
        title = article[0]['title']
        dirpath = cpath+title+"/audio"
        if not os.path.exists(dirpath):
            try:
                os.makedirs(dirpath)
            except:
                print("\u0020Unable to create folders.\r")
                return 0
        for i,method in enumerate(article[0]['content']):
        	#print(f"\n{i+1} ** {method['m_title']}")
        	if not method['m_title'] == None:
        		mtext = method['m_title']
	        	fname = f"m{i+1}"
	       		ext = 'mp3'
	        	Text2Audio(mtext,dirpath,fname,ext)
        	for j,step in enumerate(method['steps']):
        		#print(f"{j+1} : {step['s_title']}")
        		stext = step['s_title']
        		fname = f"m{i+1}_s{j+1}"
        		ext = 'mp3'
        		Text2Audio(stext,dirpath,fname,ext)
        db.update({'voiced':True},where('url')==url)
        print("\u0020Finished Generating Audio.")

    else:
        print("\u0020Article Not Found [or] Already Voiced.\r")

loader = (': ','\u02D9\u02D9',' :','..')
@animation.wait(loader,'\u2744\u0020Generating Audio\u0020')
def VoiceOver(url):
    article = getArticle(url)
    generateAudio(url,article)

# Collect("How to Place Houseplants Around Your Home: 13 Steps")