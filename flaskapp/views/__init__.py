from flask import g
from flaskapp import app
from flaskapp.main import sitemap

@app.before_request
def register_sitemap():
    g.sitemap = sitemap
