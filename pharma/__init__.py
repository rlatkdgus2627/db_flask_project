from flask import Blueprint

patient_bp = Blueprint('pharma', __name__, template_folder='templates')

from . import routes