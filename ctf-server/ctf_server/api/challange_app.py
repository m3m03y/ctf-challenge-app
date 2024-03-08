"""Setup for main challange app"""

import fastapi
from . import flag_routes


def create_app():
    """Initialize main app"""
    app = fastapi.FastAPI()
    app.include_router(flag_routes.router)
    return app
