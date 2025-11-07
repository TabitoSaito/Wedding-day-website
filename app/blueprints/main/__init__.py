from flask import Blueprint
"""
Blueprint: main

contains routes for main content e.g. home, timeline
"""

main_bp = Blueprint(
    'main',
    __name__,                 
    template_folder='templates',
    static_folder='static',
    url_prefix='/',
    static_url_path='/main'
)

from . import routes