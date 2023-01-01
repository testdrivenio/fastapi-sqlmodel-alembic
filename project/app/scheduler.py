from rocketry import Rocketry

app = Rocketry(execution="async")


# Create some tasks

@app.task('every 30 seconds')
async def do_things():
    print("INFOOOOO")


if __name__ == "__main__":
    app.run()