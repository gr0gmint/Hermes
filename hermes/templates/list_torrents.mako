<%inherit file="/base.mako" />
<table>
<tr>
<td><b>Name</b></td>
<td><b>Seeders</b></td>
<td><b>Leechers</b></td>
</tr>
%for i in torrents:
<tr>
<td><a href='/get_torrent/${i.torrent_id}'>${i.name |h}</a></td>
<td>
${i.seeders}
</td>
<td>
${i.leechers}
</td>
</tr>    
%endfor
</table>
