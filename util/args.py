import argparse
from flask_script import Manager, Server

parser = argparse.ArgumentParser()
parser.add_argument("--t", help="increase output verbosity")
parser.add_argument("runserver", help="increase output verbosity", )
args = parser.parse_args()
if args.t:
    print("verbosity turned on")

# class argument():
#  def __init__(self, dict1):
#   self.host = dict1['host']