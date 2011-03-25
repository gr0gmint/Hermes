from pyramid.view import view_config
from hermes.model import DBSession
from hermes.model.db import Torrent
from pyramid.response import Response
import os
@view_config(route_name='get_torrent')
def get_torrent(context, request):
    id_ = request.matchdict['id']
    
    torrent = DBSession.query(Torrent).filter_by(torrent_id = id_).first()
    abs_filename = os.path.join(request.registry.settings['torrent_dir'], torrent.torrent_file)
    f = open(abs_filename)
    return Response( headerlist=[('Content-Type', 'application/x-bittorrent'), ('Content-Disposition', 'attachment; filename='+torrent.name+".torrent")], app_iter=f)
