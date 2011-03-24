from hermes.model import Base
from dripple.model import Base, DBSession
from sqlalchemy import Table, Column, Integer, String, MetaData, ForeignKey, DateTime, PickleType, Boolean, Index
from sqlalchemy.orm import relationship, backref
import datetime


class Torrent(Base):
    __tablename__ = 'torrents'
    id = Column(Integer, primary_key=True)
    info_hash = Column(String)
    name = Column(String)
    desc = Column(String)
    info = Column(PickleType)
    torrent_file = Column(String)
    uploaded_time = Column(DateTime)
    download_count = Column(Integer, default=0)
    seeders = Column(Integer)
    leechers = Column(Integer)
Index('infohash', Torrent.info_hash)



class Friendship(Base):
    __tablename__ = 'friendships'
    friendship_id = Column(Integer, primary_key=True)
    userone_id = Column(Integer, ForeignKey('users.user_id'))
    usertwo_id = Column(Integer, ForeignKey('users.user_id'))
    accepted = Column(Boolean)

class Principal(Base):
    __tablename__ = 'principals'
    def __init__(self, name):
        self.principal_name = name
    principal_id = Column(Integer, primary_key=True)
    
    principal_name = Column(String, unique=True)
    

class User(Base):
    __tablename__ = 'users'
    def __init__(self, username, password):
        self.username = username
        self.password = hashlib.sha1(password).hexdigest()
    user_id = Column(Integer, primary_key=True)
    username = Column(String, unique=True)
    password = Column(String)
    friendships = relationship(Friendship, primaryjoin = (Friendship.userone_id==user_id), backref='userone')
    awaiting_friendships = relationship(Friendship, primaryjoin = (Friendship.usertwo_id == user_id), backref='usertwo')
    principals = relationship(Principal, secondary=PrincipalMembers.__table__)
    passkey = Column(String)
    uploaded = Column(Integer)
    downloaded = Column(Integer)
Index('indpasskey', User.passkey)


class Peer(Base):
    __tablename__ = 'peers'
    id = Column(Integer, primary_key=True)
    peer_id = Column(String)
    torrent_id = ForeignKey('torrents.id')
    torrent = relation(Torrent, backref='peers')
    user_id = ForeignKey('users.id')
    user = relation(User, backref='activity')
    ip = Column(String)
    port = Column(Integer)
    active = Column(Boolean)
    uploaded = Column(Integer, default=0)
    downloaded = Column(Integer, default=0)
    uploaded_total = Column(Integer, default=0)
    downloaded_total = Column(Integer, default=0)
    seeding = Column(Boolean, default=False)
    
Index('torrentid', Peer.torrent_id)
