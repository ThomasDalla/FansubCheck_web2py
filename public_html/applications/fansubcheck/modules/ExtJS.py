__author__ = 'thomas'

import simplejson

def getExtPaging(request, limit=10):
    start= 0
    orderQuery= None
    filterQuery = None
    if request.vars.start:
        start=int(request.vars.start)
    if request.vars.limit:
        limit=int(request.vars.limit)+int(request.vars.start)
    if request.vars.sort:
        sort=simplejson.loads(request.vars.sort)[0]
        d= ""
        if sort['direction']=='ASC':
            d="~"
        orderQuery= d + sort['property']
#    if request.vars.filter:
#        filter=simplejson.loads(request.vars.filter)[0]
#        if filter['type'] == "numerical" or filter['type'] == 'date':
#            if filter['comparison']=="gt":
#                comp = ">"
#            elif filter['comparison']=="lt":
#                comp="<"
#            else:
#                comp="=="
#            filterQuery= filter['field'] + comp + str(filter['value'])
#        elif filter['type'] == "boolean":
#            if filter['value']:
#                filterQuery = filter['field']==True
#            else:
#                filterQuery = filter['field']==False
    return start, limit, orderQuery, filterQuery