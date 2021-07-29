from fastapi import FastAPI,Request
import subprocess

app = FastAPI()


@app.post("/payload")
async def read_item(req: Request):
    body = await req.json()
    event = req.headers.get("X-Github-Event")
    print("Event Type:", event)
    if event == "pull_request":
        pr_status = body["pull_request"]["merged"]
        print("Is Merged:", pr_status)
        if event == "pull_request" and pr_status == True:
            print("A new Pull Request has been merged for:", body["pull_request"]["head"]["repo"]["name"])
            print("Title of PR:", body["pull_request"]["title"])
            print("PR number is:", body["number"])
            print("Created by:",  body["sender"]["login"])
            print("Head branch is:", body["pull_request"]["head"]["ref"])
            print("Base branch is:", body["pull_request"]["base"]["ref"])
            print("No. of Files Changed:",  body["pull_request"]["changed_files"])
            subprocess.call("/path/to/script")
        else:
            print("A new Pull Request has been generated for:", body["pull_request"]["head"]["repo"]["name"])
            print("PR number is:", body["number"])
            print("Created by:",  body["sender"]["login"])
