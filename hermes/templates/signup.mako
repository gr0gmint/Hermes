<%inherit file="/base.mako" />
<%namespace file="/common.mako" import="renderform" />
<form action='/signup' method="post">
${renderform(form)}
<input type="submit" value="Signup" />
</form>
