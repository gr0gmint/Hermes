<%!
    from hermes.model import DBSession
    from hermes.model.db import User
%>
<!DOCTYPE html>
<%
if 'username' in request.session:
    user = DBSession.query(User).filter_by(username=request.session['username']).first()
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

<span>Uploaded: ${user.uploaded} </span><span>Downloaded: ${user.downloaded} </span>
%if user.downloaded != 0:
    <span>Ratio: ${float(user.uploaded)/user.downloaded}</span>
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
