import urllib.request
from tinydb import TinyDB,Query,where
import os
import animation
from moviepy.editor import *

# Init Database
open('db.json', 'a').close()
db = TinyDB('db.json')
Articles = Query()


cpath = os.getcwd()+"/collections/"


def makeVideoClip(audiopath,imgpath,dirpath,fname,ext):
    a_clip = AudioFileClip(f"{audiopath}/{fname}.mp3")
    v_clip = ImageClip(f"{imgpath}/{fname}.jpg")
    v_clip = v_clip.set_duration(a_clip.duration)
    v_clip.set_audio(a_clip).write_videofile(f"{dirpath}/{fname}.{ext}",fps=24)

def getArticle(url):
    return db.search((where('url')==url) & (where('clipsmade')==False))

def generateVideoClips(url,article):
    if(len(article)>0):
        title = article[0]['title']
        dirpath = cpath+title+"/video"
        imgpath = cpath+title+"/images/raw"
        audiopath = cpath+title+"/audio"
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
	       	# 	ext = 'mp4'
	        # 	makeVideoClip(dirpath,imgpath,audiopath,fname,ext)
        	for j,step in enumerate(method['steps']):
        		fname = f"m{i+1}_s{j+1}"
        		ext = 'mp4'
        		makeVideoClip(audiopath,imgpath,dirpath,fname,ext)
        db.update({'clipsmade':True},where('url')==url)
        print("\u0020Finished Generating Video Clips.")

    else:
        print("\u0020Article Not Found [or] Already Made Clips.\r")

loader = (': ','\u02D9\u02D9',' :','..')
@animation.wait(loader,'\u2744\u0020Generating Video\u0020')
def ClipMaker(url):
    article = getArticle(url)
    generateVideoClips(url,article)

# Collect("How to Place Houseplants Around Your Home: 13 Steps")