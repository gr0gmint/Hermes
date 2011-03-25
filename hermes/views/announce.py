from pyramid.response import Response
from pyramid.view import view_config
from hermes.model import DBSession
from hermes.model.db import User,Torrent,Peer
from sqlalchemy.sql.expression import func

from bencode import bencode

import struct
import logging 

log = logging.getLogger(__name__)

def failure(reason): 
    return Response(bencode({'failure reason': reason}))

@view_config(route_name='announce')
def announce(context, request):
    if request.method == "POST":
        return failure("Invalid request type")
    passkey = request.matchdict['passkey']
    user = DBSession.query(User).filter_by(passkey=passkey).first()
    if not user:
        return failure('Invalid passkey')
    toHex = lambda x:"".join([hex(ord(c))[2:].zfill(2) for c in x])

    infohash = toHex(request.params.multi['info_hash'])
    peer_id = toHex(request.params.multi['peer_id'])
    torrent = DBSession.query(Torrent).filter_by(info_hash=infohash).first()
    peer = DBSession.query(Peer).filter_by(peer_id = peer_id).first()
    left = int(request.params['left'])
    if not peer:
        peer = Peer()
        peer.user = user
        peer.torrent = torrent
        peer.peer_id = peer_id
        peer.uploaded = 0
        peer.downloaded = 0
        peer.uploaded_total = 0
        peer.downloaded_total = 0
        peer.seeding = False

    if not torrent:
        return failure("Torrent not found")
        
    diff_uploaded = 0
    if 'uploaded' in request.params:
        diff_uploaded = int(request.params['uploaded']) - peer.uploaded
    diff_downloaded = 0
    if 'downloaded' in request.params:
        diff_downloaded = int(request.params['downloaded']) - peer.downloaded
    compactmode = False
    if 'compact' in request.params and request.params['compact'] == '1':
        compactmode=True
    peer.ip = request.environ['REMOTE_ADDR']
    peer.port = int(request.params['port'])
    
    if left == 0:
        if not peer.seeding:
            torrent.seeders += 1
        peer.seeding = True
        DBSession.add(torrent)
        DBSession.commit()
    if 'event' in request.params:
        event = request.params['event']
        if event == 'started':
            peer.active = True
            peer.uploaded = int(request.params['uploaded'])
            peer.downloaded = int(request.params['downloaded'])
            peer.uploaded_total += int(request.params['uploaded'])
            peer.downloaded_total += int(request.params['downloaded'])
        elif event == 'stopped':
            peer.active = False
            peer.uploaded = 0
            peer.downloaded = 0
            peer.uploaded_total += diff_uploaded
            peer.downloaded_total += diff_downloaded
        elif event == 'completed':
            DBSession.add(torrent)
            peer.seeding = True
            torrent.download_count += 1
            peer.active = True
            peer.uploaded = int(request.params['uploaded'])
            peer.downloaded = int(request.params['downloaded'])
            peer.uploaded_total += diff_uploaded
            peer.downloaded_total += diff_downloaded
    else:
        peer.uploaded = int(request.params['uploaded'])
        peer.downloaded = int(request.params['downloaded'])
        peer.uploaded_total += diff_uploaded
        peer.downloaded_total += diff_downloaded
    DBSession.add(peer)
    DBSession.commit()
    if compactmode:
        peers = ""
        if peer.seeding:
            log.error("peer is seeding")
            peer_objs = DBSession.query(Peer).filter_by(torrent=torrent).filter_by(active=True).filter_by(seeding=False).order_by(func.random()).limit(50).all()
        else:
            peer_objs = DBSession.query(Peer).filter_by(torrent=torrent).filter_by(active=True).filter_by(seeding=True).order_by(func.random()).limit(25).all()+DBSession.query(Peer).filter_by(torrent=torrent).filter_by(active=True).filter_by(seeding=False).order_by(func.random()).limit(25).all()
            log.error(peer_objs)
        for i in peer_objs:
            if i == peer:
                continue
            
            log.error(i.ip)
            ipsplit = i.ip.split(".")
            peers += struct.pack(">BBBBH", int(ipsplit[0]), int(ipsplit[1]),  int(ipsplit[2]), int(ipsplit[3]), i.port)
        log.error(toHex(peers))
        return Response(bencode({'interval': 1800, 'tracker id': 'Hermes', 'complete': torrent.seeders, 'incomplete': torrent.leechers, 'peers': peers}))
    if not 'no_peer_id' in request.params:
        log.error("NOT COMPACT MODE")
        peers = list()
        if peer.seeding:
            peer_objs = DBSession.query(Peer).filter_by(active=True).filter_by(torrent=torrent).filter_by(seeding=False).order_by(func.random()).limit(50).all()
        else:
            peer_objs = DBSession.query(Peer).filter_by(active=True).filter_by(torrent=torrent).filter_by(seeding=True).order_by(func.random()).limit(25).all()+DBSession.query(Peer).filter_by(active=True).filter_by(torrent=torrent).filter_by(seeding=False).order_by(func.random()).limit(25).all()
        for i in peer_objs:
            if i == peer:
                continue
            peers.append({'peer id': i.peer_id, 'ip': i.ip, 'port': i.port})
        log.error(peers)
        return Response(bencode({'interval': 1800, 'tracker id': 'Hermes', 'complete': torrent.seeders, 'incomplete': torrent.leechers, 'peers': peers}))
        
    else:
        log.error("NO_PEER_ID")
