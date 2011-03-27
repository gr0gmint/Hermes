import os
import random
import string
import shutil
from hermes.model import DBSession
from hermes.model.db import Principal, User
def save_torrent(fieldstorage, request):
    if not getattr(fieldstorage, 'filename', None):
        return None
    ext = os.path.splitext(fieldstorage.filename)[1]
    d = [random.choice(string.letters) for x in xrange(16)]
    filename = "".join(d)+ext
    abs_filename = os.path.join(request.registry.settings['torrent_dir'], filename)
    perm_file = open(abs_filename, 'w')
    shutil.copyfileobj(fieldstorage.file, perm_file)
    fieldstorage.file.close()
    perm_file.close()
    return filename
def get_principal(name):
    p = DBSession.query(Principal).filter_by(principal_name=name).first()
    return p
def get_current_user(request):
    u = DBSession.query(User).filter_by(username=request.session['username']).first()
    return u
