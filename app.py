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
#this essentially doesn't work. need to mess with it later.
def datetimeformat(value,format='%Y-%m-%d'):
    return value[4:16]

app.jinja_env.filters['datetimeformat'] = datetimeformat

def addGoal(name,desc,start,end,pplArr=[]):
    tryuser = db.users.find_one({"username":session['email']})
    pplArr = [session['email']]
    goal = {"name": name, "description": desc, "people" : pplArr, "start": start, "end": end, "completed": [],"comments":[],"incentives":[]}
    goals = db.goals
    goal_id = goals.insert(goal) 
    for friend in set(tryuser['friends']):
        frienduser = db.users.find_one({"username":friend})
        frienduser['feed'].append({'message':session['name'] + ' just added the goal '+name,'date':datetime.datetime.now(),'type':'goaladd','id':tryuser['_id']})       
        db.users.save(frienduser)
    return dumps(goal)

#add a comment
#for api need to receive name of goal-task pair, name of commenter, add message to feed of others on the goal, 
#comments need username, name, message, id of commenter, index of goal?/name of goal?...I think I should pass an id to each task

def completeTask(goalid,taskid,comment=""):
    if type(goalid) == unicode or type(goalid) ==str:
        goalid = ObjectId(goalid)

    if type(taskid) == unicode or type(taskid) ==str:
        taskid = ObjectId(taskid)

    tryuser = db.users.find_one({"username":session["email"]})
    trytask = db.tasks.find_one({"goalid":goalid,"_id":taskid})
    print trytask,tryuser 

    trytask['people'].remove(tryuser['username'])
    trytask['completed'].append(tryuser['username'])
    trytask['comments'].append({'message':comment,'username':session['email'],'name':tryuser['name'],'picture':session['picture']})
    #this may not work at all
    updateFeedArr = trytask['people'] + trytask['completed']
    for user in updateFeedArr.remove(session['email']):
        frienduser = db.users.find_one({"username":user})
        if frienduser:
            frienduser['feed'].append({'message':session['name'] + ' just completed a goal ','name':session['name'],'picture':session['picture'],'date':datetime.datetime.now(),'type':'goalcomplete','id':tryuser['_id']})       
            db.users.save(frienduser)
    db.tasks.save(trytask)
    return dumps(trytask) 

def addUser(username, name, picture):
    user ={"username": username, "name": name, "picture": picture, "friends": [], "friendrequests": [], "feed":[], "brainstorms":[], "goalrequests":[]}
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

def addTask(goalid,end,name,desc): 
    if type(goalid) == unicode or type(goalid) ==str:
        goalid = ObjectId(goalid)
    task = {"goalid":goalid,"end": end, "name": name, "description": desc, "people": [session['email']], "completed":[], "comments":[],"incentives":[]}
    db.tasks.insert(task)
    return dumps(task)

def taskComplete(goalid, taskid):
    trygoal= db.goals.find_one({"_id": goalid})
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
        todo = db.tasks.find({'people':session['email']})
        return render_template('dashboard.html',me=me,goals=goals,user=tryuser,todo=todo)

#TODO change this to be more like the goaltree page (i.e. add a template for the page) 
@app.route('/goals')
def goals():
    tryuser = db.users.find_one({'username':session['email']})
    trygoals = db.goals.find({'people':session['email']})
    return render_template('goals.html',me=tryuser,goals=trygoals)

@app.route('/goals/<goal>')
def goaltree(goal):
    trygoal = db.goals.find_one({'name':goal})
    goalid =  trygoal['_id']
    trytasks = db.tasks.find({'goalid':goalid})
    return render_template('goaltree.html',tasks=trytasks,goal=trygoal,today=datetime.datetime.now().date())

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
    if(tryuser):
        return dumps(tryuser)

@app.route('/getgoals')
def getgoals():
    trygoal = db.goals.find()
    return dumps(trygoal,default=json_util.default)

@app.route('/gettasks')
def gettasks():
    trytasks = db.tasks.find()
    return dumps(trytasks,default=json_util.default)

@app.route('/getusers')
def getusers():
    users = db.users.find()
    return dumps(users,default=json_util.default)

@app.route('/getfeed')
def newsfeed():
    return getFeed()

@app.route('/addtask/<goalid>/<enddate>/<title>/<description>')
def addtask(goalid,enddate,title,description):
    return addTask(goalid,enddate,title,description)

@app.route('/completetask/<goalid>/<taskid>/<comment>')
def completetask(goalid,taskid,comment):
    return completeTask(goalid,taskid,comment)
    
@app.route('/addgoal/<title>/<description>/<startdate>/<enddate>/<taskArr>/<friendArr>')
def addgoal(title,description,startdate,enddate,taskArr,friendArr):
    tryuser = db.users.find_one({'username':session['email']});
    for friend in friendArr.split(','):
        print friend
        tryfriend = db.users.find_one({'username':str(friend)})
        print tryfriend
        tryfriend['goalrequests'].append(title) 
        tryfriend['feed'].append({'message':session['name'] + ' asked if you want to do a goal','date':datetime.datetime.now(),'type':'goalrequest','id':tryuser['_id']})
        print tryfriend
    return "" 
    taskArr = json.loads(taskArr)
    myTasks = []
    addGoal(title,description,startdate,enddate,myTasks)
    trygoal = db.goals.find_one({'name':title,'description':description})
    for task in taskArr:
        addTask(trygoal['_id'],taskArr[task]['end'],taskArr[task]['title'],taskArr[task]['description']);
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

#@app.route('/purgeall')
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
