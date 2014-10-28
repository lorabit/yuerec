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

Just run python douban.py to start crawling.
