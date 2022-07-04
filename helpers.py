# from unidecode import unidecode
from os import chdir
from pathlib import Path
from mako.lookup import TemplateLookup
from db import cwd, db_users, query
from falcon import HTTPSeeOther

# change to current working directory
chdir(cwd)

# mako settings
templatelookup = TemplateLookup(directories=['templates'],
                                module_directory='/tmp/mako_modules',
                                collection_size=500,
                                output_encoding='utf-8',
                                encoding_errors='replace',
                                # imports=['from mako_imports import mako_imp']
                                )


def render_template(req, resp, resource, template):
	"""@falcon.after decorator for Mako templates - works on GET and POST methodes"""
	# all_topics = list(topics.order_by("order").run(req.context.conn)) # this line and
	# resp.text["topics"] = all_topics # this line are here because we need refresh topic everytime, so is best to do in on one place
	mytemplate = templatelookup.get_template(template)
	resp.text = mytemplate.render(data=resp.text)

# def create_url(header):
# 	"""Function for create url adress from header of post."""
# 	header = unidecode(header).lower() # firstly make all character lower and remove diacritics
# 	pattern = re.compile(r"\W") # \W means everythink non-alphanumeric
# 	splited_header = pattern.split(header) # split header with \W
# 	splited_header = [i for i in splited_header if i] # list comprehension for remove empty strings from list
# 	url = "-".join(splited_header) # and finaly join the list splited_header with "-"
# 	return url


class Authorize(object):
    """@falcon.before decorator for authorize if successful login - works on GET and POST methodes"""
    def __call__(self, req, resp, resource, params):
        resp.context.authorized = 0
        if req.get_cookie_values('cookie_uuid') and req.get_cookie_values('user'):
            cookie_uuid = req.get_cookie_values('cookie_uuid')[0]
            user = req.get_cookie_values('user')[0]
            cookie_from_db = db_users.search(query.name == user)[0]["cookie_uuid"]
            if cookie_uuid == cookie_from_db:
                resp.context.authorized = 1
        else:
            resp.unset_cookie('cookie_uuid') # only for sure
            resp.unset_cookie('user')
            if req.relative_uri != "/login":
                raise HTTPSeeOther("/login")
