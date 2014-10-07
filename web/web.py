# all the imports
import sqlite3
from flask import Flask, request, session, g, redirect, url_for, \
     abort, render_template, flash, json, send_file
import settings




app = Flask(__name__)
app.config.from_object(settings)

def connect_db():
    return sqlite3.connect(app.config['DATABASE'])


@app.route("/")
def index():
	pList = g.db.execute('select resouces.id,pid,resouces.tid,threads.location,uid from resouces left join threads on threads.tid = resouces.tid order by resouces.id desc limit 20').fetchall()
	return render_template('index.html',pList = pList)

@app.route("/loadMore/<id>")
def loadMore(id):
	pList = g.db.execute('select resouces.id,pid,resouces.tid,threads.location,uid from resouces left join threads on threads.tid = resouces.tid where resouces.id<? order by resouces.id desc limit 20',(id,))
	return json.dumps(pList.fetchall())

@app.route("/photo/<pid>")
def loadPhoto(pid):
	return send_file('../images/'+pid, mimetype='image/jpg')

@app.route("/search/<keyword>")
def search(keyword):
	pList = g.db.execute('select resouces.id,pid,resouces.tid,threads.location,uid from resouces left join threads on threads.tid = resouces.tid where location like ? order by resouces.id desc limit 20',('%'+keyword+'%',)).fetchall()
	return render_template('search.html',pList = pList,keyword = keyword)

@app.route("/search/<keyword>/loadMore/<id>")
def searchLoadMore(keyword,id):
	pList = g.db.execute('select resouces.id,pid,resouces.tid,threads.location,uid from resouces left join threads on threads.tid = resouces.tid where resouces.id<? and location like ? order by resouces.id desc limit 20',(id,'%'+keyword+'%',)).fetchall()
	return json.dumps(pList)



@app.before_request
def before_request():
    g.db = connect_db()

@app.teardown_request
def teardown_request(exception):
    db = getattr(g, 'db', None)
    if db is not None:
        db.close()

if __name__ == "__main__":
    app.run()