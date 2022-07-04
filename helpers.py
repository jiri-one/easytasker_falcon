# from unidecode import unidecode
from os import chdir
from pathlib import Path
from mako.lookup import TemplateLookup
from db import cwd, db_users, query

# change to current working directory
chdir(cwd)

# mako templates settings
templatelookup = TemplateLookup(directories=['templates'],
                                module_directory='/tmp/mako_modules',
                                collection_size=500,
                                output_encoding='utf-8',
                                encoding_errors='replace',
                                # imports=['from mako_imports import mako_imp']
                                )


def render_template(req, resp, resource, template):
	"""@falcon.after decorator for Mako templates - works on GET and POST methodes"""
	mytemplate = templatelookup.get_template(template)
	resp.text = mytemplate.render(data=resp.text)
