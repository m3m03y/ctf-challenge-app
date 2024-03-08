"""Main module"""

import logging
from ctf_server.api.challange_app import create_app

logging.basicConfig(level=logging.DEBUG)
app = create_app()
