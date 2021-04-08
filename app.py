from flask import Flask, request, url_for, redirect, render_template, json, jsonify
import random
import os
import sqlite3
import base64

cwd = str(os.path.dirname(os.path.realpath(__file__))) + "\\memeDB.db"

###START DB CREATION###
memeDB = sqlite3.connect(cwd)
memeCursor = memeDB.cursor()
memeCursor.execute('''CREATE TABLE IF NOT EXISTS Memes
        (ID                  INT PRIMARY KEY     NOT NULL,
        NAME                TEXT                NOT NULL,
        DATA                TEXT                NOT NULL);''')
memeDB.commit()

#Inserts default image as first db entry

memeDB.close()

###START PAGE ROUTING###
app = Flask(__name__) 

#INDEX PAGE ROUTE
@app.route('/', methods=['GET', 'POST'])
def index():
        memeDB = sqlite3.connect(cwd)
        memeCursor = memeDB.cursor()
        memeCursor.execute("select * from Memes")
        Id = str(random.randint(1, (len(memeCursor.fetchall()))))
        statement = "select DATA from Memes where ID=" + Id
        source0 = memeCursor.execute(statement)
        source = str(memeCursor.fetchall())
        source = source.strip("[]()\'")
        source = source[:-2]
        memeDB.commit()
        memeDB.close()
        #displays index page with random meme from db
        return render_template('index.html', source = source)

#GET MEME ROUTE
@app.route('/getMeme', methods=['GET'])
def getMeme():
        #redirects to index page
        return redirect(url_for('index'))

###DATABASE OPERATORS###

#ADD MEME ROUTE
@app.route('/addMeme', methods=['POST'])
def addMeme():
        memeDB = sqlite3.connect(cwd)
        memeCursor = memeDB.cursor()
        memeCursor.execute("select * from Memes")

        data = request.form["source"]
        Id = len(memeCursor.fetchall()) + 1
        name = request.form["name"]

        memeDB.execute("INSERT INTO Memes(ID,NAME,DATA) \
            VALUES(?, ?, ?)", (Id, name, data))
        memeDB.commit()
        memeDB.close()
        #adds meme && returns to index page
        return redirect(url_for('index'))

###START SERVER###
if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=80)