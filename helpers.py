# from unidecode import unidecode
from os import chdir
from pathlib import Path
from mako.lookup import TemplateLookup
from datetime import datetime
from db import cwd

# change to current working directory
chdir(cwd)

# mako templates settings
templatelookup = TemplateLookup(directories=['templates'],
                                module_directory='/tmp/mako_modules',
                                collection_size=500,
                                output_encoding='utf-8',
                                encoding_errors='replace',
                                imports=['from helpers import format_dt']
                                )

def format_dt(dt: datetime):
    months = ('ledna', 'února', 'března', 'dubna', 'května', 'června', 'července', 'srpna', 'září', 'října', 'listopadu', 'prosince')
    days = ('Pondělí', 'Úterý', 'Středa', 'Čtvrtek', 'Pátek', 'Sobota', 'Neděle')
    return f"{days[dt.weekday()]} {dt.day}. {months[dt.month-1]}, {dt.strftime('%H:%M:%S')}"
    
def render_template(req, resp, resource, template):
	"""@falcon.after decorator for Mako templates - works on GET and POST methodes"""
	mytemplate = templatelookup.get_template(template)
	resp.text = mytemplate.render(data=resp.text)
