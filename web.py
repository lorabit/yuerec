# all the imports
import sqlite3
from flask import Flask, request, session, g, redirect, url_for, \
     abort, render_template, flash
import setting

# configuration
DATABASE = '../db'
DEBUG = True
SECRET_KEY = 'development key'
USERNAME = 'admin'
PASSWORD = 'default'

app = Flask(__name__)
app.config.from_object(setting)

@app.route("/")
def index():
    render_template('index.html')

if __name__ == "__main__":
    app.run()