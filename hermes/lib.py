import os
import random
import string
import shutil

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
