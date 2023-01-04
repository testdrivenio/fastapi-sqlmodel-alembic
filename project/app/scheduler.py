import logging

from rocketry import Rocketry

app = Rocketry(execution="async")

@app.task('every 1 minutes')
async def do_things():
    logging.info("SEXOOOOOOOO")


if __name__ == "__main__":
    app.run()