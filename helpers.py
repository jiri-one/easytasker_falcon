# from unidecode import unidecode
from os import chdir
from pathlib import Path
from mako.lookup import TemplateLookup
from db import cwd

# change to current working directory
chdir(cwd)

# mako settings
templatelookup = TemplateLookup(directories=['templates'],
                                module_directory='/tmp/mako_modules',
                                collection_size=500,
                                output_encoding='utf-8',
                                encoding_errors='replace',
                                #imports=['from mako_imports import mako_imp']
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
        pass
	# 	resp.context.authorized = 0
	# 	if req.get_cookie_values('cookie_uuid'):
	# 		cookie_uuid = req.get_cookie_values('cookie_uuid')[0]
	# 		for author in list(authors.run(req.context.conn)):
	# 			if author["cookie"] == cookie_uuid:
	# 				resp.context.authorized = 1
	# 				break
	# 		else: # this part is here, because is possibility to try to access admin sites from another browser with old cookies
	# 			if resp.context.authorized != 1:
	# 				resp.unset_cookie('cookie_uuid')
	# 				resp.set_cookie('redir_from', req.relative_uri, path="/",   max_age=600, secure=True)
	# 				raise HTTPSeeOther("/login")

	# 	elif self.only_admin == 1 and resp.context.authorized == 0:
	# 		resp.unset_cookie('cookie_uuid') # only for sure
	# 		resp.unset_cookie('redir_from')
	# 		resp.set_cookie('redir_from', req.relative_uri, path="/",   max_age=600, secure=True)
	# 		raise HTTPSeeOther("/login")
