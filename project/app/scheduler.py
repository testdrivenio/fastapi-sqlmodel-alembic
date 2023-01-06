import logging

from rocketry import Rocketry

logging.basicConfig(level=logging.INFO)
mylogger = logging.getLogger(__name__)

app = Rocketry(execution="async")
product_status_cache = {}

@app.task('every 5 minutes')
async def do_things():

    product_status_cache.clear()
    mylogger.info("Product status cache cleared")


if __name__ == "__main__":
    app.run()