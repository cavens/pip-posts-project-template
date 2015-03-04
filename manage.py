import logging
logging.basicConfig(filename="posts.log", level=logging.DEBUG)
import os
from flask.ext.script import Manager
from posts import app
from getpass import getpass
from posts.database import Base


manager = Manager(app)

@manager.command
def run():
  port = int(os.environ.get('PORT',8080))
  app.run(host='0.0.0.0', port=port)

from posts.models import Post
from posts.database import session