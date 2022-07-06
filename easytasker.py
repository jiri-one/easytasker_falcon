import falcon
from datetime import datetime
from locale import setlocale, LC_TIME
# internal imports
from helpers import render_template
from login import LoginResource, Authorize
from db import cwd, get_tasks, get_task_from_db, Task

# set global local to czech version of time (I am using english everywhere ...)
setlocale(LC_TIME, "cs_CZ.utf8")


@falcon.before(Authorize())
class TaskerResource(object):
    @falcon.after(render_template, "index.mako")
    def on_get(self, req, resp):
        """Handles GET requests on index (/)"""
        tasks = get_tasks(req.get_param("tasks"))
        resp.text = {"tasks": tasks}


    @falcon.after(render_template, "task.mako")
    def on_get_task(self, req, resp, task_id):
        resp.text = get_task_from_db(task_id)
    
    
    @falcon.after(render_template, "new_task.mako")
    def on_get_new_task(self, req, resp):
        resp.text = {}
    
    def on_post_new_task(self, req, resp):
        form = req.get_media()
        print(form)
        task_data = {}
        for part in form:
            if part.name == 'filename':
                # here will be best to check if the file exists already
                with open(cwd / f"files/{part.filename}", "wb") as dest:
                    while True:
                        chunk = part.stream.read(4096)
                        if not chunk:
                            break
                        dest.write(chunk)
                task_data["attach"] = cwd / f"files/{part.filename}"
            
            else:
                task_data[part.name] = part.data.decode()

        new_task = Task(title=task_data["task_title"],
                        content=task_data["task_content"],
                        time_expired=datetime.fromisoformat(task_data["time_expired"]),
                        attach=task_data.get("attach"),
                        )
        new_task.write_to_db()
        raise falcon.HTTPSeeOther(f"/{new_task.id}")
    

# falcon.API instances are callable WSGI apps
app = falcon.App(media_type=falcon.MEDIA_HTML)
app.req_options.auto_parse_form_urlencoded = True # that needed because of forms
app.add_static_route("/templates", cwd / "templates", downloadable=True, fallback_filename=None)
app.add_static_route("/files", cwd / "files", downloadable=True, fallback_filename=None)


# Resources are represented by long-lived class instances
easytasker = TaskerResource()
login = LoginResource()
app.add_route('/login', login)
app.add_route('/logout', login, suffix="logout")
app.add_route('/', easytasker)
app.add_route('/{task_id:int}', easytasker, suffix="task")
app.add_route('/new_task', easytasker, suffix="new_task")
app.add_route('/upload', easytasker, suffix="upload")


# the rest of code is not needed for server purposes
def local_run():
    from hupper import start_reloader
    from waitress import serve
    #app.resp_options.secure_cookies_by_default = False
    reloader = start_reloader('easytasker.local_run')
    # monitor an extra file
    #reloader.watch_files(['foo.ini'])
    serve(app, host='0.0.0.0', port=8000)

if __name__ == "__main__":
    local_run()
