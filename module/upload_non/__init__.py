from flask import Blueprint, render_template
import os

upload_non_api = Blueprint('upload_non', __name__)

from . import controller