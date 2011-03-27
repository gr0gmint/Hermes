from pyramid.view import view_config
from hermes.model import DBSession
from hermes.model.db import Torrent
from pyramid.response import Response
import os
import bencode
from hermes.lib import get_current_user
import StringIO
@view_config(route_name='get_torrent')
def get_torrent(context, request):
    id_ = request.matchdict['id']
    u = get_current_user(request)
    torrent = DBSession.query(Torrent).filter_by(torrent_id = id_).first()
    abs_filename = os.path.join(request.registry.settings['torrent_dir'], torrent.torrent_file)
    f = open(abs_filename)
    torrentdata = f.read()
    torb = bencode.bdecode(torrentdata)
    
    torb['announce'] = ('http://%s/%s/announce' % (request.registry.settings['hostname'], u.passkey)).encode('utf-8')
    return Response(bencode.bencode(torb), headerlist=[('Content-Type', 'application/x-bittorrent'), ('Content-Disposition', 'attachment; filename=\"'+torrent.name+".torrent\"")])
