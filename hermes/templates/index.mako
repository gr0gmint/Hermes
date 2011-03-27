<%inherit file="/base.mako" />
%if 'username' in request.session:
    <a href='/browse'>Browse torrents</a><br />
    <a href='/addtorrent'>Upload torrent</a><br />
    <a href='/logout'>Logout</a><br />
%else:
    <a href='/login'>Login</a><br />
    <a href='/signup'>Signup</a><br />
    
%endif
