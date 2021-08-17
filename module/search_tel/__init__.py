from flask import Blueprint, render_template

search_tel_api = Blueprint('search_tel', __name__)

from . import controller