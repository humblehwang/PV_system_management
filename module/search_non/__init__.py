from flask import Blueprint, render_template

search_non_api = Blueprint('searchNon', __name__)

from . import controller