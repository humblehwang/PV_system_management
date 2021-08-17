from flask import Blueprint, render_template
import os

user_api = Blueprint('user', __name__)

from . import controller
