<%inherit file="base.mako"/>

% for task in data["tasks"]:
    <div class="task">
    <div class="title"><a href="/${task.id}">${task.title}</a>
    <div style="float: right;"> <button type="button">ÚKOL DOKONČEN</button></div></div>
    <div class="content">${task.content}</div>
    <div class="hr" style="padding-left:15px;padding-right:15px;"><hr></div>
    <div class="time_created">Úkol vytvořen: ${task.time_created.strftime('%c')}</div>
    <div class="time_expired">Úkol vyřešit do: ${task.time_expired.strftime('%c')}</div>
    <div class="hr" style="padding-left:15px;padding-right:15px;"><hr></div>
    % if task.attach:
        <div class="content">Tento úkol má přílohu: <a href="/files/${task.attach.parent.name + '/' + task.attach.name}">/files/${task.attach.parent.name + '/' + task.attach.name}</a></div>
    % endif
    <div class="postend" style="text-align:center">• • •</div>
    </div>
% endfor
