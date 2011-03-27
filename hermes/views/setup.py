from pyramid.view import view_config
from hermes.model import DBSession
from hermes.model.db import Principal

@view_config(route_name='setup')
def setup(context, request):
    #Setup principals
    try:
        p = Principal('group:user')
        p = Principal('group:admin')
        DBSession.add(p)
        DBSession.commit()
    except:
        DBSession.rollback()
    
