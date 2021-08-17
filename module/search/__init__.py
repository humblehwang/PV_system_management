from flask import Blueprint, render_template

search_api = Blueprint('search', __name__)

from . import controller