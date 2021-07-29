from fastapi import FastAPI,Request
import subprocess

app = FastAPI()


@app.post("/payload")
async def read_item(req: Request):
    body = await req.json()
    event = req.headers.get("X-Github-Event")
    print("Event Type :", event)
    pr_status = body["pull_request"]["merged"]
    print("Is Merged :", pr_status)
    if event == "pull_request" and pr_status == True:
        print("PR number is: ", body["number"])
        print("Created by: ",  body["sender"]["login"])
        print("No. of Files Changed: ",  body["pull_request"]["changed_files"])
        subprocess.call("/path/to/script")
