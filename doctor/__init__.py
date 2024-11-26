from flask import Blueprint

doctor_bp = Blueprint('doctor', __name__, template_folder='templates')

from . import routes