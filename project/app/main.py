from fastapi import FastAPI

app = FastAPI()


@app.get("/ping")
async def pong():
    return {"ping": "pong!"}
