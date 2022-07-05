<%inherit file="base.mako"/>
<div class="titulek">${data.title}</a></div>
<div class="obsah">${data.content}</div>
<div class="time_created">${data.time_created.strftime('%c')}</div>
<div class="time_expired">${data.time_expired.strftime('%c')}</div>
