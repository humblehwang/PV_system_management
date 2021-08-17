from flask import Blueprint, render_template
import os

other_api = Blueprint('other', __name__)

from . import controller