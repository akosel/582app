dir = '/home/akosel/webapps/582app/582app'
import os
os.chdir()

redirect_uri = 'http://mesh.aaronkosel.com/callback'
client_id = '1002378619889-0le313ehld4fr9eod10le621vt40pfag.apps.googleusercontent.com'
client_secret = 'f1uLmhwWzjHO6KrQT9rLkimi'

auth_uri = 'https://accounts.google.com/o/oauth2/auth'
token_uri = 'https://accounts.google.com/o/oauth2/token'
scope = ('https://www.googleapis.com/auth/userinfo.profile',
         'https://www.googleapis.com/auth/userinfo.email','https://www.googleapis.com/auth/plus.login')
profile_uri = 'https://www.googleapis.com/oauth2/v1/userinfo'
 
