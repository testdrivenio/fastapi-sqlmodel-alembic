import asyncio
import uvicorn
import sys
from scheduler import app as app_rocketry
from api import app as app_fastapi


class Server(uvicorn.Server):
    """Customized uvicorn.Server

    Uvicorn server overrides signals and we need to include
    Rocketry to the signals."""

    def handle_exit(self, sig: int, frame) -> None:
        app_rocketry.session.shut_down()
        return super().handle_exit(sig, frame)


async def main():
    """Run Rocketry and FastAPI"""

    log_config = uvicorn.config.LOGGING_CONFIG
    log_config["formatters"]["access"]["fmt"] = "[%(levelname)s %(asctime)s]  -  %(message)s"

    sys.stdout = open('info.logs', 'w')
    sys.stderr = sys.stdout
    server = Server(config=uvicorn.Config(app_fastapi,
                                          workers=1,
                                          loop="asyncio",
                                          port=8000,
                                          host='0.0.0.0'))

    api = asyncio.create_task(server.serve())
    scheduler = asyncio.create_task(app_rocketry.serve())

    await asyncio.wait([scheduler, api])



# in any file that import fn setup_logger from the above 'logger_config.py', you can set up local logger like:

if __name__ == "__main__":


    # Run both applications
    asyncio.run(main())