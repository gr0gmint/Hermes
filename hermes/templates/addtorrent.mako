<%inherit file="/base.mako" />
<%namespace file="/common.mako" import="*" />
<form action="/addtorrent" enctype="multipart/form-data" method="post">
${renderform(form)}
<input type="submit" value="Upload torrent" />
</form>
