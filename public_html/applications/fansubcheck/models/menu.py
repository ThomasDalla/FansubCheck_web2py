response.title = settings.title
response.subtitle = settings.subtitle
response.meta.author = '%(author)s <%(author_email)s>' % settings
response.meta.keywords = settings.keywords
response.meta.description = settings.description
response.menu = [
(T('Home'),URL('default','index')==URL(),URL('default','index'),[]),
#(T('Episodes'),URL('default','episodes_manage')==URL(),URL('default','episodes_manage'),[]),
#(T('Subs'),URL('default','subs_manage')==URL(),URL('default','subs_manage'),[]),
#(T('Balises'),URL('default','balises_manage')==URL(),URL('default','balises_manage'),[]),
#(T('Types'),URL('default','error_types_manage')==URL(),URL('default','error_types_manage'),[]),
#(T('Comments'),URL('default','comments_manage')==URL(),URL('default','comments_manage'),[]),
(T('Public QC List'),URL('default','public_qc_list')==URL(),URL('default','public_qc_list'),[]),
(T('My QC List'),URL('default','qc_list')==URL(),URL('default','qc_list'),[]),
(T('Add a QC'),URL('default','add_qc')==URL(),URL('default','add_qc'),[]),
]