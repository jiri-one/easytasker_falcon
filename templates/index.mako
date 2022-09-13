<%inherit file="base.mako"/>
<b>Nacházíte se v kategorii: 
% if data["tasks_type"] == "finished":
    Dokončené úkoly
% elif data["tasks_type"] == "expired":
    Prošlé úkoly
% else:
    Aktuální úkoly
% endif
</b>
% for task in data["tasks"]:
    <div class="task">
    <div class="title"><a href="/${task.id}">${task.title}</a>
    % if data["tasks_type"] != "finished":
    <div style="float: right;">
    <form action="" method="post">
    <input type="submit" name="finished_${task.id}" id="finished_${task.id}" value="ÚKOL DOKONČEN" disabled="disabled"/>

    <input type="checkbox" onchange="document.getElementById('finished_${task.id}').disabled = !this.checked;" />

    </form></div>
    % endif
    </div>
    <div class="content">${task.content}</div>
    <div class="hr" style="padding-left:15px;padding-right:15px;"><hr></div>
    <div class="time_created">Úkol vytvořen: ${format_dt(task.time_created)}</div>
    <div class="time_expired">Úkol vyřešit do: ${format_dt(task.time_expired)}</div>
    <div class="hr" style="padding-left:15px;padding-right:15px;"><hr></div>
    % if task.attach:
        <div class="content">Tento úkol má přílohu: <a href="/files/${task.attach.parent.name + '/' + task.attach.name}">/files/${task.attach.parent.name + '/' + task.attach.name}</a></div>
    % endif
    <div class="postend" style="text-align:center">• • •</div>
    </div>
% endfor
