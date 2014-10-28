#coding=utf-8
import requests
import time
import sqlite3
import sys
import time
import traceback
from daemonize import Daemonize
pid = "/tmp/douban.pid"
reload(sys)
sys.setdefaultencoding('utf-8')

workspace = "/Users/lorabit/douban/" 
imgPath = workspace+"images/"
pagePath = workspace+"pages/"
dbPath = workspace+"db"

refetchTime = 60*30

def findByTag(h, sTag, eTag):
	h = h[h.find(sTag)+len(sTag):]
	return h[:h.find(eTag)]

def accessPage(url):
	time.sleep(1)
	print url
	c = {'ue':"1538770275@qq.com"}
	c['dbcl2']="102845116:Vk19dKMh2n0"
	c['as']='deleted'
	r = requests.get(url,cookies = c)
	return r.text

def saveResouce(url,path):
	c = {'ue':"1538770275@qq.com"}
	c['dbcl2']="102845116:Vk19dKMh2n0"
	c['as']='deleted'
	r = requests.get(url,cookies = c, stream = True)
	with open(path, 'wb') as f:  
		for chunk in r.iter_content(chunk_size=1024):  
			if chunk: # filter out keep-alive new chunks  
				f.write(chunk)  
				f.flush()  
		f.close()

def downloadImage(tid, url):
	pid = url[url.rfind('/')+1:]
	if cur.execute("select * from resouces where pid=?",(pid,)).fetchone()!=None:
		cur.execute("update resouces set deleted = 0 where deleted=1 and pid=?",(pid,))
		#print pid+' exists'
		return
	saveResouce(url, imgPath + pid)
	cur.execute("insert into resouces(tid,url,pid,updateTime,deleted) values(?,?,?,datetime('now','localtime'),0)",(tid,url,pid));

def getUserLocation(uid):
	url = 'http://www.douban.com/group/people/'+uid
	h = accessPage(url)
	return findByTag(h,u'常居:&nbsp;\n','\n')

def grabContent(url):
	tid = url[len('http://www.douban.com/group/topic/'):-1]
	old = cur.execute("select id, updateTime from threads where tid=?",(tid,)).fetchone()
	if old!=None:
		t = time.mktime(time.strptime(old[1],"%Y-%m-%d %H:%M:%S"))
		if(time.time()-t<refetchTime):
			#print tid+' exists'
			return
		print 'refetch'
	h = accessPage(url)
	h =  h[h.find('<div id="content">'):]
	title = findByTag(h,'<h1>','</h1>')
	content = findByTag(h,'<div class="topic-content">','<div class="topic-opt clearfix">')

	#写入文件
	hFile = open(pagePath + tid +'.html','w')
	hFile.write(content)
	hFile.close()



	#写入数据库
	if old==None:
		uid = findByTag(h,u'<span class="from">来自: <a href="http://www.douban.com/group/people/','/')
		location = getUserLocation(uid)
		cur.execute("insert into threads(tid,title,content,uid,location,updateTime) values(?,?,?,?,?,datetime('now','localtime'))", (tid,title,content,uid,location));
	else:
		cur.execute("update threads set updateTime = datetime('now','localtime') where id = ?", (old[0],));

	cur.execute("update resouces set deleted = 1 where deleted = 0 and tid = ?;",(tid,));
	con.commit()
	h = content
	imgIndex = h.find('<img src="')
	while imgIndex!=-1:
		h = h[imgIndex+len('<img src="'):]
		imgUrl = h[:h.find('"')]
		downloadImage(tid, imgUrl)
		imgIndex = h.find('<img src="')
	con.commit()	
	print title
	#print content


con = sqlite3.connect(dbPath)
cur = con.cursor()
	
def main():

	while True:
		monitoredUrls = ['http://www.douban.com/group/haixiuzu/discussion?start=0','http://www.douban.com/group/haixiuzu/discussion?start=25','http://www.douban.com/group/haixiuzu/discussion?start=50','http://www.douban.com/group/446091/discussion?start=0','http://www.douban.com/group/face2face/discussion?start=0']
		for mainUrl in monitoredUrls:
			try:
				h = accessPage(mainUrl)
				startIndex = h.find('<!--- douban ad end -->')
				h = h[startIndex:]
				endIndex = h.find('</table>')
				h = h[:endIndex]

				aIndex = h.find('http://www.douban.com/group/topic/')
				while aIndex!=-1:
					h = h[aIndex:]
					endIndex = h.find('"')
					url = h[:endIndex]
					grabContent(url)
					h = h[h.find('<td nowrap="nowrap" class="time">'):]
					aIndex = h.find('http://www.douban.com/group/topic/')
			except:
				traceback.print_exc()
				print 'sleep for 60 seconds'
				time.sleep(60)
		print 'sleeping... safe to interupt'
		time.sleep(15)

main()
#daemon = Daemonize(app="douban_app", pid=pid, action=main)
#daemon.start()
