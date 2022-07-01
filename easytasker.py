import falcon
from datetime import datetime
from helpers import Authorize, file_path, render_template, Authorize

@falcon.before(Authorize())
class TaskerResource(object):
    
    @falcon.after(render_template, "index.mako")
    def on_get(self, req, resp):
        """Handles GET requests on index (/)"""
        start, end = slice_posts(1) # number one is here hardcoded, because index is always page one
        index_posts = list(posts.order_by(r.desc("when")).slice(start, end).run(req.context.conn)) # get index post (page 1) from RethinkDB
        posts_count = posts.count().run(req.context.conn) # get number of all posts
        page_count = ceil(posts_count / posts_per_page) # get number of pages
        pages = list(range(1,page_count+1))	# list of all pages
        resp.text = {"posts": index_posts, "pages": pages} # sending data to make tepmplate in resp.text

# falcon.API instances are callable WSGI apps
app = falcon.App(media_type=falcon.MEDIA_HTML)
app.req_options.auto_parse_form_urlencoded = True # that needed because of forms
app.add_static_route("/templates", file_path("templates"), downloadable=True, fallback_filename=None)
app.add_static_route("/files", file_path("files"), downloadable=True, fallback_filename=None)


# Resources are represented by long-lived class instances
easytasker = TaskerResource()
app.add_route('/', easytasker)



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
