from typing import Iterable

import fastapi
import uvicorn
from facet import ServiceMixin
from fastapi.middleware.cors import CORSMiddleware
from loguru import logger

from .uvicorn_server import UvicornServer


class BaseAPIService(ServiceMixin):
    def __init__(
        self,
        title: str,
        version: str,
        port: int = 8000,
    ):
        self._title = title
        self._version = version
        self._port = port

    def get_app(self) -> fastapi.FastAPI:
        app = fastapi.FastAPI(
            title=self._title,
            version=self._version,
        )

        app.service = self
        self.setup_app(app=app)

        return app

    def setup_app(self, app: fastapi.FastAPI):
        pass

    async def start(self):
        config = uvicorn.Config(app=self.get_app(), host="localhost", port=self._port)
        server = UvicornServer(config)

        logger.info("Start API service {name}", name=self._title)
        self.add_task(server.serve())

    async def stop(self):
        logger.info("Stop API service {name}", name=self._title)
