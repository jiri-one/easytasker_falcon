import falcon
from datetime import datetime
from helpers import Authorize, render_template
from db import cwd, check_password, db_users, query
from uuid import uuid4

@falcon.before(Authorize())
class TaskerResource(object):
    @falcon.after(render_template, "index.mako")
    def on_get(self, req, resp):
        """Handles GET requests on index (/)"""
        resp.text = "fadfasdf"
        # start, end = slice_posts(1) # number one is here hardcoded, because index is always page one
        # index_posts = list(posts.order_by(r.desc("when")).slice(start, end).run(req.context.conn)) # get index post (page 1) from RethinkDB
        # posts_count = posts.count().run(req.context.conn) # get number of all posts
        # page_count = ceil(posts_count / posts_per_page) # get number of pages
        # pages = list(range(1,page_count+1))	# list of all pages
        # resp.text = {"posts": index_posts, "pages": pages} # sending data to make tepmplate in resp.text


class LoginResource(object):
    @falcon.before(Authorize())
    @falcon.after(render_template, "login.mako")
    def on_get(self, req, resp):
        if resp.context.authorized == 1:
                raise falcon.HTTPSeeOther("/")
        else:
            resp.text = {}
    
    def on_post(self, req, resp):
        login = req.get_param("login")
        passwd = req.get_param("password")
        if check_password(passwd, db_users.search(query.name == login)[0]["password"]):
            new_cookie = str(uuid4())
            db_users.update({'cookie_uuid': new_cookie}, query.name == login)
            resp.set_cookie('cookie_uuid', new_cookie,
                            max_age=72000, secure=True)
            resp.set_cookie('user', login,
                            max_age=72000, secure=True)
            raise falcon.HTTPSeeOther("/")
        else:
            raise falcon.HTTPUnauthorized(
                title="Bad login or password! (Špatné jméno nebo heslo!)")

    
    def on_get_logout(self, req, resp):
        resp.unset_cookie('cookie_uuid')
        resp.unset_cookie('user')
        raise falcon.HTTPSeeOther("/login")

# falcon.API instances are callable WSGI apps
app = falcon.App(media_type=falcon.MEDIA_HTML)
app.req_options.auto_parse_form_urlencoded = True # that needed because of forms
app.add_static_route("/templates", cwd / "templates", downloadable=True, fallback_filename=None)
app.add_static_route("/files", cwd / "files", downloadable=True, fallback_filename=None)


# Resources are represented by long-lived class instances
easytasker = TaskerResource()
login = LoginResource()
app.add_route('/', easytasker)
app.add_route('/login', login)
app.add_route('/logout', login, suffix="logout")




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
