if False:
    import db
    from gluon.dal import Field
    from re import T
    from gluon import settings
    from gluon.validators import IS_LENGTH, IS_NOT_EMPTY, IS_UPLOAD_FILENAME
    from db import auth

def generateKey():
    #from Crypto.Random import random
    import random
    from datetime import datetime
    from hashlib import sha256, md5
    return md5(sha256(str(random.getrandbits(256))).digest()+str(datetime.now().isoformat())).hexdigest()

########################################
db.define_table('balise',
    Field('name', type='string', notnull=True, required=True,
          label=T('Name')),
    auth.signature,
    format='%(name)s',
    migrate=False)

db.define_table('balise_archive',db.balise,Field('current_record','reference balise',readable=False,writable=False))

########################################
db.define_table('error_type',
    Field('name', type='string', notnull=True, required=True,
          label=T('Name')),
    auth.signature,
    format='%(name)s',
    migrate=False)

db.define_table('error_type_archive',db.error_type,Field('current_record','reference error_type',readable=False,writable=False))


db.define_table('comment',
    Field('sub', type='reference sub',
          label=T('Sub')),
    Field('user', type='reference auth_user',
          label=T('User')),
    Field('date_added', type='datetime',
          label=T('Date Added')),
    Field('error_types', type='list:reference error_type',
          label=T('Error Type')),
    Field('balises', type='list:reference balise',
          label=T('Balise')),
    Field('content', type='text', notnull=True, required=True,
          label=T('Content')),
    auth.signature,
    format='%(content)s',
    migrate=settings.migrate)

db.define_table('comment_archive',db.comment,Field('current_record','reference comment',readable=False,writable=False))

########################################
db.define_table('sub',
    Field('episode', type='reference episode',
          label=T('Episode')),
    Field('start_time', type='string',
          label=T('Start Time')),
    Field('end_time', type='string',
          label=T('End Time')),
    Field('style', type='string',
          label=T('Style')),
    Field('actor', type='string',
          label=T('Actor')),
    Field('is_comment', type='boolean',
          label=T('Is Comment')),
    Field('text', type='string',
          label=T('Text')),
    Field('is_finalized', type='boolean',
          label=T('Is Finalized')),
    Field('needs_discussion', type='boolean',
          label=T('Needs Discussion')),
    Field('comments_nb', type='integer', default=0,
          label=T('Number of Comments')),
    Field('lastcomment_date', type='datetime',
          label=T('Last Comment Date')),
    auth.signature,
    format='%(sub_id)d %(text)s',
    migrate=settings.migrate)

db.define_table('sub_archive',db.sub,Field('current_record','reference sub',readable=False,writable=False))

########################################
db.define_table('episode',
    Field('file', type='upload',
          label=T('ASS/SSA File'), autodelete=True, required=True, requires=IS_UPLOAD_FILENAME(extension='ssa|ass|srt')),
    Field('name', type='string',  notnull=True,
          label=T('Name'), required=True, requires=IS_LENGTH(minsize=3)),
    Field('video_link', type='string',
          label=T('Video Link'), required=True, requires=IS_LENGTH(minsize=10)),
    Field('comments_nb', type='integer', default=0,
          label=T('Number of Comments ')),
    Field('subs_nb', type='integer', default=0,
          label=T('Number of Subs')),
    Field('lastcomment_date', type='datetime', default=None,
          label=T('Last Comment Date')),
    Field('is_h', type='boolean',
          label=T('Is H'), default=False),
    Field('is_public', type='boolean',
          label=T('Is Public'), default=True),
    Field('allow_qcteam', type='boolean',
          label=T('Allow FansubCheck QC Team'), default=True),
    Field('is_finished', type='boolean', default=False,
          label=T('Is Finished')),
    Field('key', type='string', default=generateKey(),
          label=T('Key')),
    auth.signature,
    format='%(name)s',
    migrate=settings.migrate)

#db.episode.virtual_subs_nb = Field.Virtual(lambda row: db(db.sub.episode == row.episode.id).count())
#db.episode.virtual_comments_nb = Field.Virtual(lambda row: db(db.sub.episode == row.episode.id).select())

db.episode.file.readable= False
db.episode.comments_nb.writable= False
db.episode.comments_nb.readable= False
db.episode.lastcomment_date.writable= False
db.episode.lastcomment_date.readable= False
db.episode.key.writable= False
#db.episode.key.readable= False
db.define_table('episode_archive',db.episode,Field('current_record','reference episode',readable=False,writable=False))

