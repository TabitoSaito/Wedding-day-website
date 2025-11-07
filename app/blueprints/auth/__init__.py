from flask import Blueprint
"""
Blueprint: auth

contains routes for authentication e.g. login
"""

auth_bp = Blueprint(
    'auth',
    __name__,                 
    template_folder='templates',
    static_folder='static',
    url_prefix='/auth',
    static_url_path="/auth"
)

from . import routes