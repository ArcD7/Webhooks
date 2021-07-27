from fastapi import FastAPI,Request

app = FastAPI()


@app.post("/payload")
async def read_item(req: Request):
    body = await req.json()
    event = req.headers.get("X-Github-Event")
    print(event)
    if event == "pull_request":
