<%inherit file="base.mako"/>
<div class="task">
<div class="title"><a href="/${data.id}">${data.title}</a>

<div style="float: right;">
<form action="" method="post">
<input type="submit" name="delete_${data.id}" id="delete_${data.id}" value="SMAZAT ÚKOL" disabled="disabled"/>

<input type="checkbox" onchange="document.getElementById('delete_${data.id}').disabled = !this.checked;" />

</form></div></div>
<div class="content">${data.content}</div>
<div class="hr" style="padding-left:15px;padding-right:15px;"><hr></div>
<div class="time_created">Úkol vytvořen: ${format_dt(data.time_created)}</div>
<div class="time_expired">Úkol vyřešit do: ${format_dt(data.time_expired)}</div>
<div class="hr" style="padding-left:15px;padding-right:15px;"><hr></div>
% if data.attach:
    <div class="content">Tento úkol má přílohu: <a href="/files/${data.attach.parent.name + '/' + data.attach.name}">/files/${data.attach.parent.name + '/' + data.attach.name}</a></div>
% endif
<div class="postend" style="text-align:center">• • •</div>
</div>
