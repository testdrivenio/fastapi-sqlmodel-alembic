from rocketry import Rocketry

app = Rocketry(execution="async")


# Create some tasks

@app.task('every 5 seconds')
async def do_things():
    print("la muñeca fea")

if __name__ == "__main__":
    app.run()