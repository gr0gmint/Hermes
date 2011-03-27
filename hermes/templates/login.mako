<%inherit file="/base.mako" />
<%namespace file="/common.mako" import="*" />
%if error:
<div class="errormessage">
${error}
</div>
%endif
<form action='/login' method='post'>
${renderform(form)}
<input type="submit" value="Login" />
</form>
