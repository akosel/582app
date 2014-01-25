from flask import Flask, request, session, redirect, url_for,render_template
import urllib
import json
import datetime
import requests
from bson import json_util
from bson.json_util import dumps
from bson.objectid import ObjectId
from flask.ext.mongoengine import MongoEngine
from pymongo import MongoClient
app = Flask('Mesh')
app.secret_key = 'datsupasecretappdawg'

client = MongoClient('localhost', 27017)
db = client.Mesh_DB

f = open('index.html', 'r')
idx = f.read();

f = open('dashboard.html', 'r')
dashboard = f.read();

def addGoal(name,desc,start,end,taskArr,pplArr=[]):
    tryuser = db.users.find_one({"username":session['email']})
    pplArr = [session['email']]
    goal = {"name": name, "desc": desc, "people" : pplArr, "start": start, "end": end, "tasks": taskArr, "completed": []}
    goals = db.goals
    goal_id = goals.insert(goal) 
    for friend in set(tryuser['friends']):
        frienduser = db.users.find_one({"username":friend})
        frienduser['feed'].append({'message':session['name'] + ' just added the goal '+name,'name':session['name'],'picture':session['picture'],'date':datetime.datetime.now(),'type':'goaladd','id':tryuser['_id']})       
        db.users.save(frienduser)
    return dumps(goal)

def addUser(username, name, picture):
    user ={"username": username, "name": name, "picture": picture, "friends": [], "friendrequest": [], "feed": [] }
    users = db.users
    user_id = users.insert(user)
    print user_id


def sendFriendRequest(friend):
    tryuser = db.users.find_one({"username":session['email']})
    frienduser = db.users.find_one({"username": friend})
    print tryuser['_id']
    if(tryuser):
        #tryuser['feed'] = []
        #tryuser['friendrequest'] = []
        frienduser['feed'].append({'message':session['name'] + ' sent you a friend request','name':session['name'],'picture':session['picture'],'date':datetime.datetime.now(),'type':'friendrequest','id':tryuser['_id']})       
        frienduser['friendrequest'].append(session['email'])       
        db.users.save(frienduser)
        return json.dumps(frienduser['friendrequest'])

def acceptFriendRequest(friendid):
    tryuser = db.users.find_one({"username":session['email']})
    frienduser = db.users.find_one({"_id":ObjectId(friendid)})
    if(tryuser):
        tryuser['friendrequest'].remove(frienduser['username'])
        tryuser['friends'].append(frienduser['username'])
        tryuser['feed'].append({'message':frienduser['name'] + ' is now your friend!','name':frienduser['name'],'picture':frienduser['picture'],'date':datetime.datetime.now(),'type':'acceptfriend','id':tryuser['_id']})       
        db.users.save(tryuser);
    if(frienduser):
        frienduser['friends'].append(session['email']) 
        tryuser['feed'] = [d for d in tryuser['feed'] if d.get('name') != frienduser['name'] or d.get('type') != 'friendrequest']
        db.users.save(tryuser);

def getFeed():
    tryuser = db.users.find_one({"username":session['email']})
    if(tryuser):
            return dumps(tryuser['feed'])

def getFriendRequests():
    tryuser = db.users.find_one({"username":session['email']})
    if(tryuser):
            return json.dumps(tryuser['friendrequest'])

tArr=[]
def addTask(duedate,name, desc):
    task = {"duedate": duedate, "name": name, "description": desc, "people": [session['email']], "completed":[], "comments": []}
    tArr.append(task)
    print tArr
    return task

def addNewTask(goalname,duedate,name,desc): 
    task = {"duedate": duedate, "name": name, "description": desc, "people": [session['email']], "completed":[], "comments": []}
    trygoal = db.goals.find_one({"name":goalname})
    trygoal['tasks'].append(task)
    db.goals.save(trygoal)
    return dumps(trygoal)
     

def joinTask(goalname, taskname):
    trygoal= db.goals.find_one({"name": goalname})
    if trygoal:
        elements = trygoal['tasks']
        for element in elements:
            if element['name'] == taskname:
                element['people'].append(session['email'])
                db.goals.save(trygoal)

def taskComplete(goalname, taskname):
    trygoal= db.goals.find_one({"name": goalname})
    if trygoal:
        elements = trygoal['tasks']
        for element in elements:
            if element['name'] == taskname:
                element['completed'].append(session['email'])
                db.goals.save(trygoal)
            #print trygoal['tasks'][element]['name']

def goalComplete(name):
    trygoal= db.goals.find_one({"name": goalname})
    if trygoal:
        trygoal['completed'].append(session['email'])
        db.goals.save(trygoal)

def postComment(goalname, taskname, newcomment):
    trygoal= db.goals.find_one({"name": goalname})
    if trygoal:
        elements = trygoal['tasks']
        for element in elements:
            if element['name'] == taskname:
                element['comments'].append({"Name": session['name'], "Post:" : newcomment, "Date": datetime.datetime.now()})
                db.goals.save(trygoal)

def getToDoList():
    return
    
redirect_uri = 'http://localhost:5000/callback'
client_id = '11874174533.apps.googleusercontent.com'  # get from https://code.google.com/apis/console
client_secret = 'ep1Pdcf1P1ulDMsXmigo9JXq'

auth_uri = 'https://accounts.google.com/o/oauth2/auth'
token_uri = 'https://accounts.google.com/o/oauth2/token'
scope = ('https://www.googleapis.com/auth/userinfo.profile',
         'https://www.googleapis.com/auth/userinfo.email','https://www.googleapis.com/auth/plus.login')
profile_uri = 'https://www.googleapis.com/oauth2/v1/userinfo'
 
 
@app.route('/')
def index():
    if 'email' not in session:
        return idx
    else:
        tryuser = db.users.find_one({'username':session['email']})
        trygoals = db.goals.find({'people':session['email']})
        me = sorted(tryuser['feed'], key=lambda item: item['date'],reverse=True) 
        goals = trygoals
        print trygoals.count()
        return render_template('dashboard.html',me=me,goals=goals,user=tryuser)
#TODO change this to be more like the goaltree page (i.e. add a template for the page) 
@app.route('/goals')
def goals():
    f = open('goals.html', 'r')
    content = f.read()
    return content

@app.route('/friends')
def friends():
    f = open('friends.html', 'r')
    content = f.read()
    return content

@app.route('/newgoal')
def newgoals():
    f = open('newgoal.html', 'r')
    content = f.read()
    return content

@app.route('/newgoal', methods=['POST'])
def postnewgoals():
    print "!!!!!!"
    print request.form
    return ""

@app.route('/goals/<goal>')
def goaltree(goal):
    trygoal = db.goals.find_one({'name':goal})
    goal = trygoal     
    return render_template('goaltree.html',goal=goal,today=datetime.datetime.now().date())
 
@app.route('/logout')
def logout():
    session.pop('email', '')
    session.pop('name','')
    session.pop('picture','')
    return redirect(url_for('index'))

@app.route('/sendfriendreq/<username>')
def sendfriendreq(username):
    return sendFriendRequest(username)

@app.route('/acceptfriendreq/<id>')
def acceptfriendreq(id):
    acceptFriendRequest(id)
    return dashboard


@app.route('/getfriendrequests')
def getfriendrequests():
    return getFriendRequests() 
 
@app.route('/me')
def me():
    tryuser = db.users.find_one({"username":session['email']})
#TODO put this in its own function, although this might be OKAY. Wait and see...
    goals = db.goals.find({'people':session['email']})
    obj = {}
    if(goals):
        obj['goals'] = goals
    if(tryuser):
        obj['image'] = tryuser['picture']
        obj['name'] = tryuser['name']
        obj['username'] = tryuser['username']
        obj['newsfeed'] = tryuser['feed']
        return dumps(obj)

@app.route('/getgoals')
def getgoals():
    trygoal = db.goals.find()
    return dumps(trygoal,default=json_util.default)

@app.route('/getusers')
def getusers():
    users = db.users.find()
    return dumps(users,default=json_util.default)

@app.route('/getfeed')
def newsfeed():
    return getFeed()

@app.route('/addtask/<goalname>/<enddate>/<title>/<description>')
def addtask(goalname,enddate,title,description):
    return addNewTask(goalname,enddate,title,description)


@app.route('/addgoal/<title>/<description>/<startdate>/<enddate>/<taskArr>')
def addgoal(title,description,startdate,enddate,taskArr):
    taskArr = json.loads(taskArr)
    myTasks = []
    print taskArr
    for task in taskArr:
        myTasks.append(addTask(taskArr[task]['end'],taskArr[task]['title'],taskArr[task]['description']))
    addGoal(title,description,startdate,enddate,myTasks)
    return dashboard
    
@app.route('/getfriends')
def getfriends():
    tryuser = db.users.find_one({"username":session['email']})
    if(tryuser): 
        obj = {}
        obj['friends'] = tryuser['friends']
        return json.dumps(obj)
    else:
        return json.dumps({'error':'no username found'})

@app.route('/purgeall')
def purgeall():
    #tryuser = db.users.find_one({'username':session['email']})
    #db.goals.remove()
    if(tryuser):
        tryuser['feed'] = []
      #  tryuser['friends'] = []
       # tryuser['friendrequest'] = []
        db.users.save(tryuser) 
        return dumps(tryuser)
    #return dumps(db.goals.find())
    
 

@app.route('/login')
def login():
    # Step 1
    params = dict(response_type='code',
                  scope=' '.join(scope),
                  client_id=client_id,
                  approval_prompt='force',  # or 'auto'
                  redirect_uri=redirect_uri)
    url = auth_uri + '?' + urllib.urlencode(params)
    return redirect(url)
 
 
@app.route('/callback')
def callback():
    if 'code' in request.args:
        # Step 2
        code = request.args.get('code')
        data = dict(code=code,
                    client_id=client_id,
                    client_secret=client_secret,
                    redirect_uri=redirect_uri,
                    grant_type='authorization_code')
        r = requests.post(token_uri, data=data)
        # Step 3
        access_token = r.json()['access_token']
        r = requests.get(profile_uri, params={'access_token': access_token})
        print r.json()
        tryuser = db.users.find_one({"username": r.json()['email']})
        pic = ' ';
        if('picture' in r.json()):
            pic = r.json()['picture']
            session['picture'] = pic    
         #   if tryuser['picture'] != pic:
         #      tryuser['picture'] = pic
         #     db.users.save(tryuser)
        if not tryuser:
            addUser(r.json()['email'], r.json()['name'], pic)
        session['email'] = r.json()['email']
        session['name'] = r.json()['name']
        return redirect(url_for('index'))
    else:
        return 'ERROR'
 
if __name__ == '__main__':
    app.run(debug=True)
