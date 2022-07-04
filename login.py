import falcon
from uuid import uuid4
# internal imports
from helpers import render_template
from db import cwd, check_password, db_users, query


class Authorize(object):
    """@falcon.before decorator for authorize if successful login - works on GET and POST methodes"""

    def __call__(self, req, resp, resource, params):
        resp.context.authorized = 0
        if req.get_cookie_values('cookie_uuid') and req.get_cookie_values('user'):
            cookie_uuid = req.get_cookie_values('cookie_uuid')[0]
            user = req.get_cookie_values('user')[0]
            cookie_from_db = db_users.search(query.name == user)[
                0]["cookie_uuid"]
            if cookie_uuid == cookie_from_db:
                resp.context.authorized = 1
        else:
            resp.unset_cookie('cookie_uuid')  # only for sure
            resp.unset_cookie('user')
            if req.relative_uri != "/login":
                raise falcon.HTTPSeeOther("/login")

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
