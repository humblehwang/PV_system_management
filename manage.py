from flask_script import Manager, Server
from module import app


"""
from datetime import datetime
import logging
import os



file_name = "{:%Y-%m-%d}".format(datetime.now()) + '.log'


    
FORMAT = '%(asctime)s %(levelname)s: %(message)s'
logging.basicConfig(level=logging.NOTSET,filename=file_name, filemode='w', format=FORMAT)



logging.debug('debug message')
logging.info('info message')
logging.warning('warning message')
logging.error('error message')
logging.critical('critical message')
"""


# set up the app
manager = Manager(app)
# set python manage.py runserver as run server finction
manager.add_command('runserver', Server())

# Set up the manage 
@manager.shell
def make_shell_context():
    return dict(app=app)

if __name__ == '__main__':
    manager.run()