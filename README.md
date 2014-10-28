#Setup
##Requirements
python 2.7

sqlite3

##Database
In your yuerec directory, run this:
```
sqlite3 db
```

Use following sentences to initiate database:
```
CREATE TABLE "resouces"(id integer NOT NULL PRIMARY KEY AUTOINCREMENT, tid, url, updateTime datetime, pid, deleted);
CREATE TABLE "threads"(id integer NOT NULL PRIMARY KEY AUTOINCREMENT, tid, title, content, updateTime datetime, uid, location);
```
## Config
Edit douban.py and web/settings.py to configure the app.

#Usage
Just run python douban.py to start crawling.

And run python web.py to start webserver.
