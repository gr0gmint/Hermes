from pyramid.view import view_config
from hermes.model import DBSession
from hermes.model.db import Torrent

@view_config(route_name='browse', renderer='/list_torrents.mako')
def list_torrents(context, request):
    torrents = DBSession.query(Torrent).all()
    return {'torrents': torrents}
    
