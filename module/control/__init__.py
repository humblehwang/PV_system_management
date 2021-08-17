from flask import Blueprint, render_template
import os

control_api = Blueprint('control', __name__)

from . import controller
