# -*- coding: utf-8 -*-

#########################################################################
## This scaffolding model makes your app work on Google App Engine too
## File is released under public domain and you can use without limitations
#########################################################################

## if SSL/HTTPS is properly configured and you want all HTTP requests to
## be redirected to HTTPS, uncomment the line below:
# request.requires_https()

import json

if False:
    from gluon.dal import DAL, Field
    from gluon.contrib.pysimplesoap.server import request
    from papyon.event import session
    from re import T
    from gluon.contrib.pysimplesoap.client import response

if not request.env.web2py_runtime_gae:
    ## if NOT running on Google App Engine use SQLite or other DB
    if request.env.remote_addr=='127.0.0.1':
        db = DAL('sqlite://fcheck.sqlite')
    else:
        #db = DAL('sqlite://fcheck.sqlite', folder='/home/dotcloud/data')
        db = DAL('mysql://fansubcheck:yE3xEAiFW9@fansubcheck.mysql.fluxflex.com:3306/fansubcheck')
#        with open('/home/dotcloud/environment.json') as f:
#            env = json.load(f)
#        db = DAL('mysql://'+env['DOTCLOUD_DATA_MYSQL_LOGIN']+':'+env['DOTCLOUD_DATA_MYSQL_PASSWORD']+"@"+env['DOTCLOUD_DATA_MYSQL_HOST']+":"+str(env['DOTCLOUD_DATA_MYSQL_PORT'])+'/mysql')
    #db = DAL('mysql://fansubcheck:yE3xEAiFW9@fansubcheck.mysql.fluxflex.com:3306/fansubcheck')
else:
    ## connect to Google BigTable (optional 'google:datastore://namespace')
    db = DAL('google:datastore')
    ## store sessions and tickets there
    session.connect(request, response, db = db)
    ## or store session in Memcache, Redis, etc.
    ## from gluon.contrib.memdb import MEMDB
    ## from google.appengine.api.memcache import Client
    ## session.connect(request, response, db = MEMDB(Client()))

## by default give a view/generic.extension to all actions from localhost
## none otherwise. a pattern can be 'controller/function.extension'
response.generic_patterns = ['*'] if request.is_local else []
## (optional) optimize handling of static files
# response.optimize_css = 'concat,minify,inline'
# response.optimize_js = 'concat,minify,inline'

#########################################################################
## Here is sample code if you need for
## - email capabilities
## - authentication (registration, login, logout, ... )
## - authorization (role based authorization)
## - services (xml, csv, json, xmlrpc, jsonrpc, amf, rss)
## - old style crud actions
## (more options discussed in gluon/tools.py)
#########################################################################

from gluon.tools import Auth, Crud, Service, PluginManager, prettydate
auth = Auth(db, hmac_key=Auth.get_or_create_key())
crud, service, plugins = Crud(db), Service(), PluginManager()

## create all tables needed by auth if not custom tables

########################################
db.define_table('auth_user',
    Field('username', type='string',
          label=T('Username')),
    Field('first_name', type='string',
          label=T('First Name')),
    Field('last_name', type='string',
          label=T('Last Name')),
    Field('email', type='string',
          label=T('Email')),
    Field('password', type='password',
          readable=False,
          label=T('Password')),
    Field('created_on','datetime',default=request.now,
          label=T('Created On'),writable=False,readable=False),
    Field('modified_on','datetime',default=request.now,
          label=T('Modified On'),writable=False,readable=False,
          update=request.now),
    Field('registration_key',default='',
          writable=False,readable=False),
    Field('reset_password_key',default='',
          writable=False,readable=False),
    Field('registration_id',default='',
          writable=False,readable=False),
    format='%(username)s',
    migrate=settings.migrate)

db.auth_user.first_name.requires = IS_NOT_EMPTY(error_message=auth.messages.is_empty)
db.auth_user.last_name.requires = IS_NOT_EMPTY(error_message=auth.messages.is_empty)
db.auth_user.password.requires = CRYPT(key=auth.settings.hmac_key)
db.auth_user.username.requires = IS_NOT_IN_DB(db, db.auth_user.username)
db.auth_user.registration_id.requires = IS_NOT_IN_DB(db, db.auth_user.registration_id)
db.auth_user.email.requires = (IS_EMAIL(error_message=auth.messages.invalid_email),
                               IS_NOT_IN_DB(db, db.auth_user.email))
db.auth_user.first_name.writable = True
db.auth_user.last_name.writable  = True
db.auth_user.username.writable = True
db.auth_user.email.writable  = True
auth.settings.create_user_groups = False
auth.define_tables(migrate = settings.migrate)

## configure email
mail=auth.settings.mailer
mail.settings.server = 'smtp.gmail.com:587'
mail.settings.sender = 'thomas.dallagnese@gmail.com'
mail.settings.login = 'thomas.dallagnese@gmail.com:csg4ever'

## configure auth policy
auth.settings.registration_requires_verification = False
auth.settings.registration_requires_approval = False
auth.settings.reset_password_requires_verification = True

## if you need to use OpenID, Facebook, MySpace, Twitter, Linkedin, etc.
## register with janrain.com, write your domain:api_key in private/janrain.key
from gluon.contrib.login_methods.rpx_account import use_janrain, RPXAccount
#use_janrain(auth,filename='private/janrain.key')
#auth.settings.actions_disabled.append('retrieve_username')
from gluon.contrib.login_methods.extended_login_form import ExtendedLoginForm
# define where to go after RPX login
if request.vars._next:
    url = "http://www.fansubcheck.com/fansubcheck/default/user/login?_next=%s" % request.vars._next
else:
    url = "http://www.fansubcheck.com/fansubcheck/default/user/login"
other_form = RPXAccount(request, api_key='56b1a6942038b92a67db2c17ba4bd2ce1dbf5dd8', domain='fansubcheck', url=url)
auth.settings.login_form = ExtendedLoginForm(auth, other_form, signals=['token'])

#########################################################################
## Define your tables below (or better in another model file) for example
##
## >>> db.define_table('mytable',Field('myfield','string'))
##
## Fields can be 'string','text','password','integer','double','boolean'
##       'date','time','datetime','blob','upload', 'reference TABLENAME'
## There is an implicit 'id integer autoincrement' field
## Consult manual for more options, validators, etc.
##
## More API examples for controllers:
##
## >>> db.mytable.insert(myfield='value')
## >>> rows=db(db.mytable.myfield=='value').select(db.mytable.ALL)
## >>> for row in rows: print row.id, row.myfield
#########################################################################


mail.settings.server = settings.email_server
mail.settings.sender = settings.email_sender
mail.settings.login = settings.email_login
