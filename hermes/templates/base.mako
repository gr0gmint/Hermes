<!DOCTYPE html>
<%!
    from hermes.model import DBSession
    from hermes.model.db import User
    notation = ['KB', 'MB', 'GB', 'TB']
%>
<%
if 'username' in request.session:
    user = DBSession.query(User).filter_by(username=request.session['username']).first()
    upload_notation = 'B'
    uploaded = user.uploaded
    download_notation = 'B'
    downloaded = user.downloaded
    for i in range(0, len(notation)):
        if user.uploaded > 10**(3+i*3):
            upload_notation = notation[i]
            uploaded = user.uploaded / float(10**(3+i*3))
        if user.downloaded > 10**(3+i*3):
            download_notation = notation[i]
            downloaded = user.downloaded / float(10**(3+i*3))
else:
    user = None
%>
<html>
<head>
<title>
Hermes
</title>
<meta http-equiv="content-type" content="text/html; charset=utf-8"/>
<meta name="description" content="description"/>
<meta name="keywords" content="keywords"/> 
<meta name="author" content="author"/> 
</head>
<body>
<div id="topbar">
%if user:

<span>Uploaded: ${uploaded} ${upload_notation} </span><span>Downloaded: ${downloaded} ${download_notation} </span>
%if user.downloaded != 0:
    <span>Ratio: ${"%.2f" % (float(user.uploaded)/user.downloaded)}</span>
%else:
    <span>Ratio: infinite</span>
%endif
%endif
</div>
<div id="flashmessage">
%if 'flashmessage' in request.session:
    ${request.session['flashmessage']}
    <%
    del request.session['flashmessage']
    request.session.save()
    %>
%endif
</div>
<div id="flasherror">
%if 'flasherror' in request.session:
    ${request.session['flasherror']}
    <%
    del request.session['flasherror']
    request.session.save()
    %>
%endif
</div>
${self.body()}
</body>
</html>
