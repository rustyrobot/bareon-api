import os
import sys

from paste import deploy
from paste import httpserver

from bareon_api.common.config import CONF


current_dir = os.path.dirname(__file__)


def run():
    prop_dir = os.path.join(current_dir, '..', 'etc', 'bareon')

    application = deploy.loadapp(
        'config:{prop_dir}/bareon-api-paste.ini'.format(prop_dir=prop_dir),
        name='main',
        relative_to='.')

    httpserver.serve(application, host=CONF.host_ip, port=CONF.port)
