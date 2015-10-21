import os

from paste import deploy
from paste import httpserver


current_dir = os.path.dirname(__file__)

def run():
    prop_dir = os.path.join(current_dir, '..', 'etc', 'bareon')

    application = deploy.loadapp(
        'config:{prop_dir}/bareon-api-paste.ini'.format(prop_dir=prop_dir),
        name='main',
        relative_to='.')

    httpserver.serve(application, host='127.0.0.1', port='9322')
