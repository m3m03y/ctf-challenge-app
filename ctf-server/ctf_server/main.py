"""Main module"""

import logging
from api.challange_app import create_app

logging.basicConfig(level=logging.DEBUG)
app = create_app()
