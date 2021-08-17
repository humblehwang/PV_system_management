from flask import Blueprint, render_template
import os

edit_non_api = Blueprint('editNon', __name__)

from . import controller
