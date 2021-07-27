from fastapi import FastAPI,Request

app = FastAPI()


@app.post("/payload")
async def read_item(req: Request):
    body = await req.json()
    event = req.headers.get("X-Github-Event")
    print(type(body))
    print(event)
    pr_status = body["pull_request"]["merged"]
    if event == "pull_request" and pr_status == True:
        print("PR number is: ", body["number"])
        print("Created by: ",  body["sender"]["login"])
        print("No. of Files Changed: ",  body["changed_files"])

