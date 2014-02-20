from flask import Flask, request, session, redirect, url_for,render_template
import config
import urllib
import json
import datetime
import requests
from bson import json_util
from dateutil import parser
from bson.json_util import dumps
from bson.objectid import ObjectId
from flask.ext.mongoengine import MongoEngine
from pymongo import MongoClient
import os
os.chdir(config.dir)

app = Flask('Mesh')
app.secret_key = 'datsupasecretappdawg'

client = MongoClient('localhost', 27017)
db = client.Mesh_DB

f = open('index.html', 'r')
idx = f.read();

#define filters for use with jinja2
def datetimeformat(value,format='%Y-%m-%d'):
    return parser.parse(value).strftime('%B %d, %Y')
def namefusername(value):
    return db.users.find_one({'username':value})['name']
def goalnamefid(value):
    goalid = ObjectId(value)
    if db.goals.find_one({'_id':goalid}):
        return db.goals.find_one({'_id':goalid})['name']
    else:
        return "Goal does not exist"

app.jinja_env.filters['datetimeformat'] = datetimeformat
app.jinja_env.filters['namefusername'] = namefusername
app.jinja_env.filters['goalnamefid'] = goalnamefid

#begin main app functions

def addGoal(name,desc,start,end,pplArr=[]):
    tryuser = db.users.find_one({"username":session['email']})
    pplArr = [{"username":session['email'],"picture":session['picture']}]
    goal = {"name": name, "description": desc, "people" : pplArr, "start": start, "end": end, "completed": [],"comments":[],"incentives":[]}
    goals = db.goals
    goal_id = goals.insert(goal) 
    for friend in set(tryuser['friends']):
        frienduser = db.users.find_one({"username":friend})
        frienduser['feed'].append({'picture':session['picture'],'message':session['name'] + ' just added the goal '+name,'date':datetime.datetime.now(),'type':'goaladd','id':tryuser['_id']})       
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

    db.tasks.update({'_id':taskid},{'$pull':{'people':{'username':session['email']}}} )
    db.tasks.update({'_id':taskid},{'$push':{'completed':{'username':session['email'],'picture':session['picture']}}} )
    tryuser = db.users.find_one({"username":session["email"]})
    trytask = db.tasks.find_one({"goalid":goalid,"_id":taskid})
    if comment != "":
        trytask['comments'].append({'message':comment,'username':session['email'],'name':tryuser['name'],'picture':session['picture']})
    print trytask
    #this may not work at all
#    updateFeedArr = trytask['people'] + trytask['completed']
#    print updateFeedArr
#    for user in updateFeedArr:
#        print user
#        frienduser = db.users.find_one({"username":user})
#        print frienduser
#        if frienduser:
#            frienduser['feed'].append({'message':session['name'] + ' just completed a goal ','name':session['name'],'picture':session['picture'],'date':datetime.datetime.now(),'type':'goalcomplete','id':tryuser['_id']})       
#            db.users.save(frienduser)
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

    task = {"goalid":goalid,"end": end, "name": name, "description": desc, "people": [{'username':session['email'],'picture':session['picture']}], "completed":[], "comments":[],"incentives":[]}
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

#begin url routes 
 
@app.route('/')
def index():
    if 'email' not in session:
        return idx
    else:
        tryuser = db.users.find_one({'username':session['email']})
        trygoals = db.goals.find({'people.username':session['email']})
        me = sorted(tryuser['feed'], key=lambda item: item['date'],reverse=True) 
        goals = trygoals
        tasks = db.tasks.find({'people.username':session['email']}).sort([('end',1)])
#TODO can't figure out how to get the normal sort to work. weird. oh well.
        todo = []
        for item in tasks:
            todo.append(item)
        todo = sorted(todo, key=lambda item: datetimeformat(item['end']),reverse=False)
        return render_template('dashboard.html',me=me,goals=goals,user=tryuser,todo=todo)

#TODO change this to be more like the goaltree page (i.e. add a template for the page) 
@app.route('/goals')
def goals():
    tryuser = db.users.find_one({'username':session['email']})
    trygoals = db.goals.find({'people.username':session['email']})
    return render_template('goals.html',me=tryuser,goals=trygoals)

@app.route('/goals/<goal>')
def goaltree(goal):
    trygoal = db.goals.find_one({'name':goal})
    goalid =  trygoal['_id']
    tasks = db.tasks.find({'goalid':goalid})
    todo = []
    for item in tasks:
        todo.append(item)
    todo = sorted(todo, key=lambda item: datetimeformat(item['end']),reverse=True)
    return render_template('goaltree.html',tasks=todo,goal=trygoal,today=datetime.datetime.now().date())

@app.route('/friends')
def friends(): 
    users = db.users.find({'username':{'$ne':session['email']}})
    goals = db.goals.find({'people.username':session['email']})
    friends = []
    for goal in goals:
        for person in goal['people']:
            if person['username'] != session['email'] and person not in friends:
                    friends.append(person)    
    return render_template('friends.html',friends=friends)

@app.route('/newgoal')
def newgoals():
    users = db.users.find({'username':{'$ne':session['email']}})
    return render_template('newgoal.html',users=users) 
 
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

@app.route('/getusers/<username>')
def getuser(username):
    tryuser = db.users.find_one({'$or':[{"username":username},{"name":{'$regex':username}}]})
    if(tryuser):
        return dumps(tryuser)
    else:
        return "No users called %s. Try an e-mail address" % username

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
def completetaskshare(goalid,taskid,comment):
    return completeTask(goalid,taskid,comment)

@app.route('/completetask/<goalid>/<taskid>')
def completetasknotnow(goalid,taskid):
    return completeTask(goalid,taskid)

@app.route('/removetask/<taskid>')
def removetask(taskid):
    db.tasks.remove({'_id':ObjectId(taskid)})
    return dumps(db.tasks.find())

#TODO remove every task with this goal id 
@app.route('/removegoal/<goalid>')
def removegoal(goalid):
    db.goals.remove({'_id':ObjectId(goalid)})
    db.tasks.remove({'goalid':ObjectId(goalid)})
    return dumps(db.tasks.find())

@app.route('/deleted')
def goaldeleted():
    return "Goal Deleted!"

@app.route('/joingoal/<goalid>')
def joingoal(goalid):
    if type(goalid) == unicode or type(goalid) ==str:
        goalid = ObjectId(goalid)

    db.goals.update({'_id':goalid},{'$push':{'people':{'username':session['email'],'picture':session['picture']}}} )
    db.tasks.update({'goalid':goalid},{'$push':{'people':{'username':session['email'],'picture':session['picture']}}})
    db.users.update({'username':session['email']},{'$pull':{'feed':{'id':goalid}}}) 
    db.users.update({'username':session['email']},{'$pull':{'goalrequests':{'goalid':goalid}}}) 
        
    return 'Goal accepted!'

@app.route('/addgoal/<title>/<description>/<startdate>/<enddate>/<taskArr>/<friendArr>')
def addgoal(title,description,startdate,enddate,taskArr,friendArr):
    tryuser = db.users.find_one({'username':session['email']});
    taskArr = json.loads(taskArr)
    myTasks = []
    addGoal(title,description,startdate,enddate,myTasks)
    trygoal = db.goals.find_one({'name':title,'description':description})
    
    for task in taskArr:
        if task:
            addTask(trygoal['_id'],taskArr[task]['end'],taskArr[task]['title'],taskArr[task]['description']);

    for friend in friendArr.split(','):
        tryfriend = db.users.find_one({'username':str(friend)})
        print tryfriend
        tryfriend['goalrequests'].append({'goalid': trygoal['_id'] , 'requesterid': tryuser['_id'] , 'date' : datetime.datetime.now()})
        tryfriend['feed'].append({'picture':session['picture'],'message':session['name'] + ' asked if you want to do a goal','date':datetime.datetime.now(),'type':'goalrequest','id':trygoal['_id']})
        print tryfriend
        db.users.save(tryfriend)
    return '<h1>You did it</h1>' + dumps(trygoal)
    
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
                  scope=' '.join(config.scope),
                  client_id=config.client_id,
                  approval_prompt='force',  # or 'auto'
                  redirect_uri=config.redirect_uri)
    url = config.auth_uri + '?' + urllib.urlencode(params)
    return redirect(url)
 
 
@app.route('/callback')
def callback():
    if 'code' in request.args:
        # Step 2
        code = request.args.get('code')
        data = dict(code=code,
                    client_id=config.client_id,
                    client_secret=config.client_secret,
                    redirect_uri=config.redirect_uri,
                    grant_type='authorization_code')
        r = requests.post(config.token_uri, data=data)
        # Step 3
        access_token = r.json()['access_token']
        r = requests.get(config.profile_uri, params={'access_token': access_token})
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
