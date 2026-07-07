from flask import Blueprint
from app.auth import routes

auth = Blueprint('auth', __name__, template_folder='templates')
