import urllib.request
from tinydb import TinyDB,Query,where
import os
import animation

# Init Database
open('db.json', 'a').close()
db = TinyDB('db.json')
Articles = Query()


cpath = os.getcwd()+"/collections/"


def addCaption2Image(text,rawpath,dirpath,fname,ext):
    width=1280
    height=720
    pass
    
    

def getArticle(url):
    return db.search((where('url')==url) & (where('captioned')==False))

def captionImages(url,article):
    if(len(article)>0):
        title = article[0]['title']
        dirpath = cpath+title+"/images/captioned"
        rawpath = cpath+title+"/images/raw"
        if not os.path.exists(dirpath):
            try:
                os.makedirs(dirpath)
            except:
                print("\u0020Unable to create folders.\r")
                return 0
        for i,method in enumerate(article[0]['content']):
        	# if not method['m_title'] == None:
        	# 	mtext = method['m_title']
	        # 	fname = f"m{i+1}"
	       	# 	ext = 'jpg'
	        # 	addCaption2Image(mtext,rawpath,dirpath,fname,ext)
        	for j,step in enumerate(method['steps']):
        		stext = step['s_title']
        		fname = f"m{i+1}_s{j+1}"
        		ext = 'jpg'
        		addCaption2Image(stext,rawpath,dirpath,fname,ext)
        db.update({'captioned':True},where('url')==url)
        print("\u0020Finished Captioning Images.")

    else:
        print("\u0020Article Not Found [or] Already Captioned.\r")

loader = (': ','\u02D9\u02D9',' :','..')
@animation.wait(loader,'\u2744\u0020Captioning\u0020')
def Captioner(url):
    article = getArticle(url)
    captionImages(url,article)

# Collect("How to Place Houseplants Around Your Home: 13 Steps")