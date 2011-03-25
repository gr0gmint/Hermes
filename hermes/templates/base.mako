<!DOCTYPE html>
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
