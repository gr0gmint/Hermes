<%def name="renderform(form)">
<table>

%for field in form:
<tr>
<td>${field.label}:</td><td>    ${field}</td>
%if field.errors:
</tr>
<tr>
 <td></td><td><ul class='errorlist'>
    %for error in field.errors:
        <li>${error}</li>
    %endfor
    </ul></td>
%endif
</tr>
%endfor
</table>
</%def>
