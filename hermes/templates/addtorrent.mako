<%inherit file="/base.mako" />
<%namespace file="/common.mako" import="*" />
<h3>Your announce url: ${announce}</h3>
<form action="/addtorrent" enctype="multipart/form-data" method="post">
${renderform(form)}
<input type="submit" value="Upload torrent" />
</form>
