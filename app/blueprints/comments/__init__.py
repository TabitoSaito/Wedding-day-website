from flask import Blueprint

comment_bp = Blueprint(
    'comments',
    __name__,                 
    template_folder='templates',
    static_folder='static',
    url_prefix='/comments',
    static_url_path="/comments"
)

from . import routes