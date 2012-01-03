from gluon.storage import Storage
settings = Storage()

settings.migrate = True
settings.title = 'Fansub Check'
settings.subtitle = 'No more speedsub!'
settings.author = '$p00ky'
settings.author_email = 'Sp00ky@erogaki.com'
settings.keywords = ''
settings.description = ''
settings.layout_theme = 'Default'
settings.database_uri = 'sqlite://storage.sqlite'
settings.security_key = '4b6290ab-0939-4a43-8d13-39d49874ca88'
settings.email_server = 'localhost'
settings.email_sender = 'you@example.com'
settings.email_login = ''
settings.login_method = 'local'
settings.login_config = ''
settings.plugins = ['translate', 'sortable', 'comments', 'wiki', 'multiselect', 'attachments', 'jqmobile', 'dropdown', 'tagging', 'rating']
