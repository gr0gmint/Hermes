from pyramid.view import view_config
from hermes.model import DBSession
from hermes.model.db import Torrent
@view_config(route_name='index', renderer='/index.mako')
def index(context, request):
    return {}
