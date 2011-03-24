from pyramid.reponse import Response
from pyramid.view import view_config
from hermes.model import DBSession
from hermes.model.db import User,Torrent,Peer
from sqlalchemy.sql.expression import func

from bencode import bencode

@view_config(route_name='announce')
def announce(context, request):
    if request.method == "POST":
        #return Error("100", "Invalid request type")
    passkey = request.matchdict['passkey']
    user = DBSession.query(User).filter_by(passkey=passkey).first()
    if not u:
        #return Error("900", 'Invalid passkey')
    infohash = request.params['info_hash']
    torrent = DBSession.query(Torrent).filter_by(info_hash=infohash).first()
    peer = DBSession.query(Peer).filter_by(peer_id = request.params['peer_id']).first()
    if not peer:
        peer = Peer()
        peer.user = user
        peer.torrent = torrent
        peer.peer_id = request.params['peer_id']

    if not torrent:
        #return Error("200", "Torrent not found")
        
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
    
    if int(request.params['downloaded']) > 1024:
        peer.seeding = False
    
    if 'event' in request.params:
        event = request.params['event']
        if event == 'started':

            peer.uploaded = int(request.params['uploaded'])
            peer.downloaded = int(request.params['downloaded'])
            peer.uploaded_total += int(request.params['uploaded'])
            peer.downloaded_total += int(request.params['downloaded'])
            if not peer.active:
                if peer.seeding:
                    torrent.seeders+=1
                else:
                    torrent.leechers +=1
                DBSession.add(torrent)
            peer.active = True
        elif event == 'stopped':
            if peer.active:
                if peer.seeding:
                    torrent.seeders-=1
                else:
                    torrent.leechers-=1
                DBSession.add(torrent)
            peer.active = False
            peer.uploaded = 0
            peer.downloaded = 0
            peer.uploaded_total += diff_uploaded
            peer.downloaded_total += diff_downloaded
        elif event == 'completed':
            if not peer.seeding:   
                torrent.seeders += 1
            if peer.active:
                torrent.leechers -= 1
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
        pass#GOGO COMPACT        
    if not 'no_peer_id' in request.params:
        peers = list()
        if peer.seeding:
            peer_objs = DBSession(Peer).filter_by(torrent=torrent).filter_by(seeding=True).order_by(func.random()).limit(50).all()
        else:
            peer_objs = DBSession(Peer).filter_by(torrent=torrent).filter_by(seeding=True).order_by(func.random()).limit(25).all()+DBSession(Peer).filter_by(torrent=torrent).filter_by(seeding=False).order_by(func.random()).limit(25).all()
        for i in peer_objs:
            peers.append({'peer id': i.peer_id, 'ip': i.ip, 'port': i.port})
        return Response(bencode({'interval': 1800, 'tracker id': 'Hermes', 'complete': torrent.seeders, 'incomplete': torrent.leechers, 'peers': peers}))
        
