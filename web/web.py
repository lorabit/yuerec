# all the imports
import sqlite3
from flask import Flask, request, session, g, redirect, url_for, \
     abort, render_template, flash, json, send_file
import settings
import time
import Image
import os



app = Flask(__name__)
app.config.from_object(settings)

def connect_db():
    return sqlite3.connect(app.config['DATABASE'])


@app.route("/")
def index():
	pList = g.db.execute('select resouces.id,pid,resouces.tid,threads.location,uid from resouces left join threads on threads.tid = resouces.tid where deleted=0 order by resouces.id desc limit 20').fetchall()
	return render_template('index.html',pList = pList)

@app.route("/loadMore/<id>")
def loadMore(id):
	pList = g.db.execute('select resouces.id,pid,resouces.tid,threads.location,uid from resouces left join threads on threads.tid = resouces.tid where resouces.id<? and deleted=0 order by resouces.id desc limit 20',(id,))
	return json.dumps(pList.fetchall())

@app.route("/photo/<pid>")
def loadPhoto(pid):
	if os.path.exists('../images/w300'+pid)==False:
		im = Image.open('../images/'+pid)
		oW = im.size[0]
		oH = im.size[1]
		cim = im.resize((300,oH*300/oW))
		cim.save('../images/w300'+pid)
	return send_file('../images/w300'+pid, mimetype='image/jpg')

@app.route("/search/<keyword>")
def search(keyword):
	pList = g.db.execute('select resouces.id,pid,resouces.tid,threads.location,uid from resouces left join threads on threads.tid = resouces.tid where location like ? and deleted=0 order by resouces.id desc limit 20',('%'+keyword+'%',)).fetchall()
	return render_template('search.html',pList = pList,keyword = keyword)

@app.route("/search/<keyword>/loadMore/<id>")
def searchLoadMore(keyword,id):
	pList = g.db.execute('select resouces.id,pid,resouces.tid,threads.location,uid from resouces left join threads on threads.tid = resouces.tid where resouces.id<? and location like ? and deleted=0 order by resouces.id desc limit 20',(id,'%'+keyword+'%',)).fetchall()
	return json.dumps(pList)

@app.route("/photo/<pid>/delete")
def deletePhoto(pid):
	g.db.execute('update resouces set deleted = 2 where pid=?',(pid,));
	g.db.commit()
	return json.dumps({"msg":"success"})



@app.before_request
def before_request():
    g.db = connect_db()

@app.teardown_request
def teardown_request(exception):
    db = getattr(g, 'db', None)
    if db is not None:
        db.close()

if __name__ == "__main__":
    app.run(host = app.config['HOST'],port = app.config['PORT'])
