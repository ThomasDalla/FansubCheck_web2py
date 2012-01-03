# -*- coding: utf-8 -*-
### required - do no delete

if False:
    from models.db import db, auth, service
    from gluon.html import URL
    from gluon.sqlhtml import SQLFORM
    from gluon.contrib.pysimplesoap.server import request
    from gluon.contrib.pysimplesoap.client import response
    from gluon.http import redirect

import ssa_parser, ExtJS
from datetime import datetime

def user(): return dict(form=auth())
def download(): return response.download(request,db)
def call(): return service()
### end requires
def index():
    return dict()

def error():
    message=""
    if 'error_message' in request.vars:
        message= request.vars['error_message']
    elif len(request.args)>=1:
        message=request.args[0]
    if len(message)>0:
        response.flash= message
    return dict(message=message)

@auth.requires_login()
def episodes_manage():
    form = SQLFORM.smartgrid(db.episode,onupdate=auth.archive)
    return locals()

@auth.requires_login()
def subs_manage():
    form = SQLFORM.smartgrid(db.sub,onupdate=auth.archive)
    return locals()

@auth.requires_login()
def error_types_manage():
    form = SQLFORM.smartgrid(db.error_type,onupdate=auth.archive)
    return locals()

@auth.requires_login()
def balises_manage():
    form = SQLFORM.smartgrid(db.balise,onupdate=auth.archive)
    return locals()

@auth.requires_login()
def comments_manage():
    form = SQLFORM.smartgrid(db.comment,onupdate=auth.archive)
    return locals()

@auth.requires_login()
def update_test():
    from gluon.tools import Crud
    crud = Crud(db)
    return dict(form=crud.update(db.balise, request.args(0)))

@auth.requires_login()
def add_qc():
    if 'flash' in request.vars:
        response.flash= request.vars['flash']
    form = SQLFORM(db.episode, fields=['name', 'file', 'video_link', 'is_h', 'is_public', 'allow_qcteam'])
    if form.process().accepted:
       try:
           subs = ssa_parser.importSubsFromSSA(request.vars.file.value)
       except Exception, e:
           response.flash = "Errors importing the subs (%s)" % e.message
           db(db.episode.id == form.vars.id).delete()
       else:
           try:
               subsNb=0
               for s in subs:
                   if 'Text' in s and len(s['Text'])>0:
                       actor= None
                       if 'Actor' in s:
                           actor= s['Actor']
                       db.sub.insert(episode=form.vars.id
                           ,start_time= s['Start']
                           ,end_time= s['End']
                           ,style= s['Style']
                           ,text= s['Text']
                           ,actor= actor)
                       subsNb+=1
                   db(db.episode.id == form.vars.id).update(subs_nb=subsNb)
           except Exception, e:
               response.flash= "Errors inserting the subs in the database (%s)" % e.message
           else:
               response.flash = 'Uploaded! Found %d subs' % subsNb
    return dict(form=form)

@auth.requires_login()
def my_qc_list():
    start, limit, orderQuery, filterQuery = ExtJS.getExtPaging(request)
#    return dict(locals())
#    if filter != None:
#        episodes= db((db.episode.created_by == auth.user.id) & (filterQuery)).select(limitby=(start,limit),orderby=orderQuery)
#    else:
    totalCount= db(db.episode.created_by == auth.user.id).count()
    episodes= db(db.episode.created_by == auth.user.id).select(limitby=(start,limit),orderby=orderQuery)
    return dict(episodes = episodes,
                totalCount=totalCount,
                metaData= {"totalProperty": "totalCount"})

def get_public_qc_list():
    start, limit, orderQuery, filterQuery = ExtJS.getExtPaging(request)
#    return dict(locals())
#    if filter != None:
#        episodes= db((db.episode.created_by == auth.user.id) & (filterQuery)).select(limitby=(start,limit),orderby=orderQuery)
#    else:
    totalCount= db(db.episode.is_public == True).count()
    episodes= db(db.episode.is_public == True).select(limitby=(start,limit),orderby=orderQuery)
    return dict(episodes = episodes,
                totalCount=totalCount,
                metaData= {"totalProperty": "totalCount"})

def public_qc_list():
    if 'flash' in request.vars:
        response.flash= request.vars['flash']
    publicEpisodesNb= db(db.episode.is_public == True).count()
    if not publicEpisodesNb>0:
        response.flash= "There is no public QC yet... Login and upload one!"
    return locals()

@auth.requires_login()
def qc_list():
    if 'flash' in request.vars:
        response.flash= request.vars['flash']
    if not db(db.episode.created_by == auth.user.id).count()>0:
        message= "You do not have any QC. Upload a QC first ;)"
        redirect(URL('default','add_qc?flash='+message))
    else:
        return locals()

@auth.requires_login()
def show_qc():
    id=None
    key=None
    episode = None
    #start, limit, orderQuery, filterQuery = ExtJS.getExtPaging(request, limit=50)
    if len(request.args)>=2:
        id = request.args[0]
        key = request.args[1]
        episode= db((db.episode.id==id)&(db.episode.key==key)).select().first()
        #subs = db((db.sub.episode == id) & (db.episode.key==key)).select(limitby=(start,limit))
    if episode:
        return locals()
    else:
        message= "Invalid QC"
        redirect(URL('default','qc_list?flash='+message))

@auth.requires_login()
def subs_list():
    id=None
    key=None
    subs = None
    totalCount=0
    start, limit, orderQuery, filterQuery = ExtJS.getExtPaging(request, limit=50)
    if orderQuery is not None:
        orderQuery = orderQuery.replace("comments_nb","sub.comments_nb")
        orderQuery = orderQuery.replace("lastcomment_date","sub.lastcomment_date")
    if len(request.args)>=2:
        id = request.args[0]
        key = request.args[1]
        totalCount= db((db.sub.episode == id) & (db.episode.key==key)).count()
        subs = db((db.sub.episode == id) & (db.episode.key==key)).select(db.sub.ALL,limitby=(start,limit),orderby=orderQuery)
    return dict(subs = subs,
                totalCount=totalCount,
                metaData= {"totalProperty": "totalCount"})

@auth.requires_login()
def get_comments():
    totalCount= 0
    comments= None
    if len(request.args)>=1:
        subId= request.args[0]
        comments= db((db.comment.sub == subId) & (db.auth_user.id == db.comment.user)).select(db.comment.ALL, db.auth_user.username)
        totalCount= len(comments)
    return dict(comments = comments,
                totalCount=totalCount,
                metaData= {"totalProperty": "totalCount"})

@auth.requires_login()
def call_qc():
    return service()

@service.json
def post_comment():
    success=False
    msg="Unknown Error"
    try:
        content = request.vars['comment_content']
        sub_id = request.vars['sub_id']
        episode_id = request.vars['episode_id']
    except:
        success= False
        msg= "Could not read the content or the IDs"
    else:
        # insert the comment man!
        if content is not None and len(content)>0:
            db.comment.insert(sub=sub_id, user=auth.user.id, content=content)
            now = datetime.now()
            db(db.sub.id==sub_id).update(comments_nb=db.sub.comments_nb+1,lastcomment_date=now)
            db(db.episode.id==episode_id).update(comments_nb=db.episode.comments_nb+1,lastcomment_date=now)
            success= True
            msg= "Comment inserted!"
        else:
            msg="Please enter a valid comment"
            success=False
    return dict(msg=msg, success=success)