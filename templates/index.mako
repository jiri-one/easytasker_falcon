<%inherit file="base.mako"/>

% for task in data["tasks"]:
    <div class="task">
    <div class="titulek"><a href="/${task.id}">${task.title}</a></div>
    <div class="obsah">${task.content}</div>
    <div class="time_created">${task.time_created.strftime('%c')}</div>
    <div class="time_expired">${task.time_expired.strftime('%c')}</div>
    <div class="postend">• • •</div>
    </div>
% endfor
