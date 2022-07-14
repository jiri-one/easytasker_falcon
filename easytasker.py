from multiprocessing.sharedctypes import Value
import falcon
from datetime import datetime
from locale import setlocale, LC_TIME
# internal imports
from helpers import render_template
from login import LoginResource, Authorize
from db import cwd, get_tasks, get_task_from_db, remove_task_from_db, search_tasks, Task

# set global local to czech version of time (I am using english everywhere ...)
setlocale(LC_TIME, "cs_CZ.utf8")


@falcon.before(Authorize())
class TaskerResource(object):
   
    @falcon.after(render_template, "index.mako")
    def on_get(self, req, resp):
        """Handles GET requests on index (/)"""
        tasks = get_tasks(self.db, req.get_param("tasks"))
        resp.text = {"tasks": tasks, "tasks_type": req.get_param("tasks")}
    
    def on_post(self, req, resp):
        """Handles POST requests on index (/)"""
        if req.get_param("tasks") != "finished":
            for part in req.media:
                try:
                    doc_id = int(part.split("_")[1])
                    if part.split("_")[0] != "finished":
                        raise ValueError
                except ValueError:
                    falcon.HTTPBadRequest("Používejte pouze tlačítka a odkazy na stránce!")
                task = get_task_from_db(self.db, doc_id)
                task.time_finished = datetime.now()
                task.update_in_db()
            raise falcon.HTTPSeeOther("/?tasks=finished")
        else:
            falcon.HTTPBadRequest("Používejte pouze tlačítka a odkazy na stránce!")
    

    @falcon.after(render_template, "task.mako")
    def on_get_task(self, req, resp, task_id):
        task = get_task_from_db(self.db, task_id)
        if task:
            resp.text = task
        else:
            raise falcon.HTTPBadRequest(title="Neexistující ID tasku, používejte pouze tlačítka a odkazy na stránce!")
    
    
    def on_post_task(self, req, resp, task_id):
        for part in req.media:
            try:
                doc_id = int(part.split("_")[1])
                if part.split("_")[0] != "delete" or doc_id != task_id:
                    raise ValueError
            except ValueError:
                falcon.HTTPBadRequest(title="Používejte pouze tlačítka a odkazy na stránce!")
        remove_task_from_db(self.db, doc_id)
        raise falcon.HTTPSeeOther("/")

    
    @falcon.after(render_template, "new_task.mako")
    def on_get_new_task(self, req, resp):
        resp.text = {}
    
    def on_post_new_task(self, req, resp):
        task_data = {}
        for part in req.media:
            if part.name == 'filename' and part.filename:
                # here will be best to check if the file exists already
                with open(cwd / f"files/{self.user}/{part.filename}", "wb") as dest:
                    #dest.write(part.data) if you want to upload it whole
                    while True:
                        chunk = part.stream.read(512)
                        if not chunk:
                            break
                        dest.write(chunk)
                task_data["attach"] = cwd / f"files/{self.user}/{part.filename}"
            
            else:
                task_data[part.name] = part.data.decode()

        new_task = Task(title=task_data["task_title"],
                        content=task_data["task_content"],
                        time_expired=datetime.fromisoformat(task_data["time_expired"]),
                        attach=task_data.get("attach"),
                        db=self.db,
                        )
        new_task.write_to_db()
        raise falcon.HTTPSeeOther(f"/{new_task.id}")
    
    @falcon.after(render_template, "search.mako")
    def on_get_search(self, req, resp):
        resp.text = {}

    @falcon.after(render_template, "search.mako")
    def on_post_search(self, req, resp):
        for part in req.media:
            if part.name == "search":
                searched_word = part.data.decode()
            else:
                where_to_search = part.data.decode()
        tasks = search_tasks(self.db, where_to_search, searched_word)
        resp.text = {"tasks": tasks,
                     "tasks_type": where_to_search,
                     "searched_word": searched_word
                    }
        #raise falcon.HTTPSeeOther(req.url)

    

# falcon.API instances are callable WSGI apps
app = falcon.App(media_type=falcon.MEDIA_HTML)
app.add_static_route("/templates", cwd / "templates", downloadable=True, fallback_filename=None)
app.add_static_route("/files", cwd / "files", downloadable=True, fallback_filename=None)


# Resources are represented by long-lived class instances
easytasker = TaskerResource()
login = LoginResource()
app.add_route('/login', login)
app.add_route('/logout', login, suffix="logout")
app.add_route('/register', login, suffix="register")
app.add_route('/', easytasker)
app.add_route('/{task_id:int}', easytasker, suffix="task")
app.add_route('/new_task', easytasker, suffix="new_task")
app.add_route('/search', easytasker, suffix="search")


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
