<%inherit file="base.mako"/>
<div class="task">
<div class="title"><a href="/${data.id}">${data.title}</a>
<div style="float: right;"> <button type="button">ÚKOL DOKONČEN</button></div>
</div>
<div class="content">${data.content}</div>
<div class="hr" style="padding-left:15px;padding-right:15px;"><hr></div>
<div class="time_created">Úkol vytvořen: ${data.time_created.strftime('%c')}</div>
<div class="time_expired">Úkol vyřešit do: ${data.time_expired.strftime('%c')}</div>
<div class="hr" style="padding-left:15px;padding-right:15px;"><hr></div>
% if data.attach:
    <div class="content">Tento úkol má přílohu: <a href="/files/${data.attach.parent.name + '/' + data.attach.name}">/files/${data.attach.parent.name + '/' + data.attach.name}</a>
% endif
<div class="postend" style="text-align:center">• • •</div>
</div>
