#coding=utf-8
from pyramid.view import view_config
from wtforms import Form, FileField, TextField, validators
from hermes.lib import save_torrent
import logging 
import os
import bencode
import hashlib
import datetime
from hermes.model import DBSession
from hermes.model.db import Torrent
from hermes.lib import get_current_user
log = logging.getLogger(__name__)

class AddTorrentForm(Form):
    name = TextField('Torrent name', [validators.Required()])
    torrent_file = FileField('File')
    def validate_torrent_file(form,field):
        if not getattr(field.data, 'filename', None):
            raise validators.ValidationError('You need to supply a torrentfile')
@view_config(route_name='addtorrent', renderer='/addtorrent.mako', permission='view')
def addtorrent(context, request):
    u = get_current_user(request)
    announce_url = ('http://%s/%s/announce' % (request.registry.settings['hostname'], u.passkey)).encode('utf-8')
    if request.method=="POST":
        form = AddTorrentForm(request.params)
        if form.validate():
            
            filename = save_torrent(form.torrent_file.data, request)
            abs_filename = os.path.join(request.registry.settings['torrent_dir'], filename)
            info = bencode.bencode(bencode.bdecode(open(abs_filename).read())['info'])
            name = form.name.data
            info_hash = hashlib.sha1(info).hexdigest()
            log.error('INFOHASH: '+info_hash)
            torrent = Torrent()
            torrent.info_hash = info_hash
            torrent.name = unicode(name) 
            torrent.info = {}
            torrent.uploaded_time = datetime.datetime.now()
            torrent.torrent_file = filename
            torrent.last_checked = datetime.datetime.now()
            DBSession.add(torrent)
            DBSession.commit()
            log.error(filename)
        return {'form': form, 'announce': announce_url}
    else:
        form = AddTorrentForm()
        return {'form': form, 'announce': announce_url}
