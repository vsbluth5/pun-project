# ---- YOUR APP STARTS HERE ----
# -- Import section --

import os
from flask import Flask
from flask import render_template, request, redirect, session, url_for
from flask_pymongo import PyMongo

from bson.objectid import ObjectId

# -- Initialization section --
app = Flask(__name__)

# name of database
app.config['MONGO_DBNAME'] = 'punDB' 

# URI of database for read/write provileges
app.config['MONGO_URI'] = 'mongodb+srv://person1:pVoEoiSZnPw0omb8@cluster0-vmzkd.mongodb.net/punDB?retryWrites=true&w=majority'


# This is for the session
#  If using Python 3, use a string
app.secret_key = '_5#y2L"F4Q8z\n\xec]/'

mongo = PyMongo(app)

# LOGIN
@app.route('/login', methods=['POST'])
def login():
    users = mongo.db.users
    login_user = users.find_one({'name' : request.form['username']})

    if login_user:
        if request.form['password'] == login_user['password']:
            session['username'] = request.form['username']
            return redirect(url_for('display_main'))
        return redirect(url_for('gologin'))
    return render_template('signup.html') 

# SIGN UP
@app.route('/signup', methods=['POST', 'GET'])
def signup():
    if request.method == 'POST':
        users = mongo.db.users
        existing_user = users.find_one({'name' : request.form['username']})

        if existing_user is None:
            users.insert({'name' : request.form['username'], 'password' : request.form['password']})
            session['username'] = request.form['username']
            return redirect(url_for('display_main'))

        return 'That username already exists! Try logging in.'

    return render_template('signup.html')

# INDEX
@app.route('/')
@app.route('/index')
def index():
    pun_collection = mongo.db.puns
    pun_documents = pun_collection.find({})
    # print(pun_collection.count_documents({}))    #how to get count of documents (records)
    return render_template("index.html", records=pun_documents)

# GO TO LOGIN
@app.route('/gologin')
def go_to_login():
    return render_template('login.html')

# DISPLAY MAINPAGE
@app.route('/mainpage')
def display_main():
    pun_collection = mongo.db.puns
    pun_documents = pun_collection.find({})
    return render_template("mainpage.html", records=pun_documents)


# ADD PUNS
@app.route('/add')
def add():
    pun_collection = mongo.db.puns
    mylist = [
        { "phrase": "How do construction workers party? They raise the roof.", "keyword1": "construction", "keyword2": "wprkers", "rating":0},
        { "phrase": "A chicken crossing the road is truly poultry in motion.", "keyword1": "motion", "keyword2": "chicken", "rating":0},
        { "phrase": "The other day I held the door open for a clown. I thought it was a nice jester.", "keyword1": "clowns", "keyword2": "humor", "rating":0},
        { "phrase": "What did one plant say to another? What's stomata?", "keyword1": "plants", "keyword2": "gardening", "rating":0},
        { "phrase": "I've been to the dentist many times so I know the drill.", "keyword1": "drill", "keyword2": "dentist", "rating":0},
        { "phrase": "I thought Santa was going to be late, but he arrived in the Nick of time.", "keyword1": "santa", "keyword2": "time", "rating":0},
        { "phrase": "What do you call a person rabid with wordplay? An energizer punny.", "keyword1": "favorite", "keyword2": "chicken", "rating":0},
        { "phrase": "The grammarian was very logical. He had a lot of comma sense.", "keyword1": "logical", "keyword2": "sense", "rating":0},
        { "phrase": "I was struggling to figure out how lightning works, but then it struck me", "keyword1": "lightning", "keyword2": "memory", "rating":0},
        { "phrase": "The two pianists had a good marriage. They always were in a chord.", "keyword1": "piano", "keyword2": "music", "rating":0},
        { "phrase": "She had a photographic memory but never developed it.", "keyword1": "memory", "keyword2": "photo", "rating":0},
        { "phrase": "Santa Claus' helpers are known as subordinate Clauses", "keyword1": "santa", "keyword2": "clause", "rating":0}
   ]
        
    pun_collection.insert_many(mylist)
    # print(collection.count_documents({}))    #how to get count of documents (records)
    return redirect(url_for('display_main'))

#remove all
@app.route('/remove')
def emptyDatabase():
    # define a variable for the collection you want to connect to
    pun_collection = mongo.db.puns
    pun_collection.remove({})
    # print(songs.count_documents({}))    #how to get count of documents (records)
    return redirect(url_for('display_main'))

# COLLECT USER-SUBMITTED PUNS
@app.route('/pun/new', methods=['GET', 'POST'])
def new_event():
    if request.method == "GET":
        #return render_template('new_event.html')
        return "Need to add a page here"
    else:
        phrase = request.form['phrase']
        key1 = request.form['key1'].lower()
        key2 = request.form['key2'].lower()
        pun_collection = mongo.db.puns
        pun_collection.insert({'phrase': phrase, 'keywprd1': key1, 'keyword2': key2, 'lister': session['username'], "rating":0})
        return redirect(url_for('display_main'))

#SORT by rating
@app.route('/sort/phrase')
def sort_puns():
    pun_collection = mongo.db.puns
    pun_documents=pun_collection.find({}).sort('rating', -1 )  #1 means ascending, -1 is descending
    return render_template('mainpage.html', records=pun_documents)
    #return redirect(url_for('display_main'))


# SHOW KEYWORD PAGE
@app.route('/find/keyword', methods=['GET', 'POST'])
def find_keyword():
    if request.method == "GET":
        #return render_template('new_event.html')
        return "Find Artist: Need to add something here"
    else:
        key = request.form['key']
        pun_collection = mongo.db.puns
        pun_list = pun_collection.find({'keyword1': key})
        return render_template('puns.html', theKey = key, records = pun_list)


# SHOW PUN PAGE
@app.route('/find/<pun_id>')
def find_song(pun_id):
    #print(punphrase)
    pun_collection = mongo.db.puns
    pun = pun_collection.find_one({'_id': ObjectId(pun_id)})
    return render_template('pun_info.html', pun =  pun)

#Update fields
@app.route('/update/<pun_id>', methods=['GET', 'POST'])
def changeSong(pun_id):
    if request.method == "GET":
        #return render_template('new_event.html')
        return "Returning to update: Need to add a page here"
    else:
        myquery = { "_id": ObjectId(pun_id) }
        pun_phrase = request.form['phrase']
        key1 = request.form['key1']
        key2 = request.form['key2']
        rate = request.form['rating']
        newvalues = { "$set": { "phrase": pun_phrase, "keyword1" : key1, "keyword2":key2, "rating": rate, "lister":session['username'] } }

        pun_collection = mongo.db.puns
        pun_collection.update_one(myquery, newvalues)
        return redirect(url_for('display_main'))

#REMOVE 
@app.route('/remove/<pun_id>')
def remove_song(pun_id):
    myquery = { "_id": ObjectId(pun_id) }
    pun_collection = mongo.db.puns
    pun_collection.delete_one(myquery)
    return redirect(url_for('display_main'))

# LOGOUT
@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))

# PUNS BY USER
@app.route('/profile/<name>')
def listings(name):
    print (name)
    pun_collection = mongo.db.puns
    pun_documents = pun_collection.find({'lister' : name})
    return render_template('listings.html', puns = pun_documents, lister = name)

# GO TO GENERATE
@app.route('/generate')
def go_generate():
    print("Calling generate")
    return render_template('generate.html')