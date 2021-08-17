from flask import Blueprint, render_template
import os

upload_api = Blueprint('upload', __name__)

from . import controller