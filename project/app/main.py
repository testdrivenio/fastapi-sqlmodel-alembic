import asyncio
import logging
import pathlib
from pathlib import Path
from fastapi.logger import logger as fast_logger
import uvicorn
import sys
from scheduler import app as app_rocketry
from api import app as app_fastapi

logger = logging.getLogger(__name__)

config_path = Path(__file__).with_name("logging_config.json")


class Server(uvicorn.Server):
    """Customized uvicorn.Server

    Uvicorn server overrides signals and we need to include
    Rocketry to the signals."""

    def handle_exit(self, sig: int, frame) -> None:
        app_rocketry.session.shut_down()
        return super().handle_exit(sig, frame)


async def main():
    """Run Rocketry and FastAPI"""
    cwd = pathlib.Path(__file__).parent.resolve()
    server = Server(config=uvicorn.Config(app_fastapi,
                                          workers=1,
                                          loop="asyncio",
                                          port=8000,
                                          host='0.0.0.0',
                                          log_config=f"{cwd}/config_log.ini",
                                          reload=True
                                          ))

    api = asyncio.create_task(server.serve())
    scheduler = asyncio.create_task(app_rocketry.serve())

    await asyncio.wait([scheduler, api])


# in any file that import fn setup_logger from the above 'logger_config.py', you can set up local logger like:

if __name__ == "__main__":
    # Run both applications
    asyncio.run(main())
