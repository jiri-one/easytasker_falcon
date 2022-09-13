<%inherit file="base.mako"/>
<%  
    actual = ""
    finished = ""
    expired = ""
    if "tasks_type" in data:
        if data["tasks_type"] == "actual":
            actual = "checked"
        elif data["tasks_type"] == "finished":
            finished = "checked"
        elif data["tasks_type"] == "expired":
            expired = "checked"
    else:
        actual = "checked"
%>

<center>
<div class="title" style="text-align:center;"><b>Vyhledávání:</b></div>
<div class="search_form">
<form method="post" action="" accept-charset="UTF-8" enctype="multipart/form-data">
	<label for="search">Zadejte text, který chcete hledat:</label>
	<input type="text" name="search" placeholder="Vyhledávací pole" value="${data.get("searched_word", "")}"><br>
    Ve kterých úkolech chcete vyhledávat?
    <input type="radio" id="actual" name="tasks" value="actual" ${actual} />
    <label for="actual">Aktuální úkoly</label>
    <input type="radio" id="finished" name="tasks" value="finished" ${finished} />
    <label for="finished">Dokončené úkoly</label>
    <input type="radio" id="expired" name="tasks" value="expired" ${expired} />
    <label for="expired">Prošlé úkoly</label><br>
	<input type="submit" value="Hledej">
</form>
</div>
</center>
% if "tasks" in data:
    % for task in data["tasks"]:
        <div class="task">
        <div class="title"><a href="/${task.id}">${task.title}</a>
        % if data["tasks_type"] != "finished":
        <div style="float: right;">
        <form action="/" method="post">
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
% endif
