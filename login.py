import falcon
from uuid import uuid4
# internal imports
from helpers import render_template, Authorize
from db import cwd, check_password, db_users, query

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
