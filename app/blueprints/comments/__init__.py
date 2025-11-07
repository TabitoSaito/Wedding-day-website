from flask import Blueprint
"""
Blueprint: comments

contains routes for comments/congratulations e.g. route to show all comments
"""

comment_bp = Blueprint(
    'comments',
    __name__,                 
    template_folder='templates',
    static_folder='static',
    url_prefix='/comments',
    static_url_path="/comments"
)

from . import routes