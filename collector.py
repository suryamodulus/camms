import urllib.request
from tinydb import TinyDB,Query,where
import os,sys
import animation

# Init Database
open('db.json', 'a').close()
db = TinyDB('db.json')
Articles = Query()


cpath = os.getcwd()+"/collections/"


def downloadImage(url,dirpath,fname,ext):
    urllib.request.urlretrieve(url, f"{dirpath}/{fname}.{ext}")

def getArticle(url):
    return db.search((where('url')==url) & (where('collected')==False))

def collectImages(url,article):
    if(len(article)>0):
        title = article[0]['title']
        dirpath = cpath+title+"/images/raw"
        if not os.path.exists(dirpath):
            try:
                os.makedirs(dirpath)
            except:
                print("\u0020Unable to create folders.\r")
                return 0
        for i,method in enumerate(article[0]['content']):
            for j,step in enumerate(method['steps']):
                fname = f"m{i+1}_s{j+1}"
                ext = step['s_img'].split('.')[-1]
                downloadImage(step['s_img'],dirpath,fname,ext)
        db.update({'collected':True},where('url')==url)
        print("\u0020Finished Collecting Images.")

    else:
        print("\u0020Article Not Found [or] Already collected.\r")

loader = (': ','\u02D9\u02D9',' :','..')
@animation.wait(loader,'\u2744\u0020Collecting\u0020')
def Collect(url):
    article = getArticle(url)
    collectImages(url,article)

# Collect("How to Place Houseplants Around Your Home: 13 Steps")