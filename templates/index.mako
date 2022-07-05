<%inherit file="base.mako"/>

% for task in data["tasks"]:
    ##  % if last_date != post["when"].split()[0][0:10]:
    ##       <div class="date">${mako_imp.format_date(post["when"].split()[0][0:10])}</div>  
    ##  % endif
    <div class="titulek"><a href="/${task.id}">${task.title}</a></div>
    <div class="obsah">${task.content}</div>
    <div class="time_created">${task.time_created}</div>
    <div class="time_expired">${task.time_expired}</div>
     <div class="postend">• • •</div>
% endfor
