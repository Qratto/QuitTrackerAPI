from fastapi import FastAPI

app = FastAPI()

@app.get("/health", status_code=200)
async def check_work():
    return {"status": "ok"}