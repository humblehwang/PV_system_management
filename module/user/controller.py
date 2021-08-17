from . import user_api
from flask import render_template, request, jsonify, current_app
import time
import json
import datetime
#import execjs

# Custom Response Format
_Response = {
    "responseText": None,
    "sucess": True,
    "status_code": 200,             
    }   
thread1 = None



@user_api.route('/', methods=['GET', 'POST']) 
def login():
    return render_template("user/login.html")

@user_api.route('/signup', methods=['GET', 'POST']) 
def signup():
    return render_template("user/signup.html")

@user_api.route('/reset', methods=['GET', 'POST']) 
def reset():
    return render_template("user/reset.html")

@user_api.route('/forgot', methods=['GET', 'POST']) 
def forgot():
    return render_template("user/forgot.html")

@user_api.route('/userinfo', methods=['GET', 'POST']) 
def info():
    return render_template("user/userinfo.html")

@user_api.route('/userEmail', methods=['GET', 'POST'])	
def user():
    if request.method == 'POST':
        email = json.loads(request.data)
        print(datetime.datetime.now() ,email["user_email"],"user")
        return email["user_email"]


"""
@user_api.route('/logout', methods=['GET', 'POST']) 
def logout():
    return render_template("user/logout.html")
"""


'''
def get_js():
    f = open("./static/js/user/checklogin.js", 'r', encoding='UTF-8')
    line = f.readline()
    htmlstr = ''
    while line:
        htmlstr = htmlstr + line
        line = f.readline()
    return htmlstr

def login_required():
    jsstr = get_js()
    ctx = execjs.compile(jsstr)
    login_check = ctx.call('check_login');
    if login_check == 1:
        return True
    else:
        return False
'''