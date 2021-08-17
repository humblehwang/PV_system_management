from flask import Blueprint, render_template
import os

edit_api = Blueprint('edit', __name__)

from . import controller
