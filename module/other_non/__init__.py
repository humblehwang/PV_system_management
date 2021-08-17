from flask import Blueprint, render_template

other_non_api = Blueprint('otherNon', __name__)

from . import controller