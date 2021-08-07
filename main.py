from fastapi import FastAPI, Request, HTTPException
import subprocess
import os
from hashlib import sha256
import hmac
import json

app = FastAPI()


@app.post("/payload")
async def read_item(req: Request):
    body = await req.json()
    event = req.headers.get("X-Github-Event")
    request_hash = req.headers.get("X-Hub-Signature-256")
    payload_body = await req.body()
    #print(type(payload_body))
    verify = verify_signature(payload_body, request_hash)
    #print(verify)
    if verify:
        print("Event Type:", event)
        if event == "pull_request":
            pr_status = body["pull_request"]["merged"]
            print("PR Status:", body["action"])
            print("Is Merged:", pr_status)
            if event == "pull_request" and pr_status == True:
                print("A new Pull Request has been merged for:", body["pull_request"]["head"]["repo"]["name"])
                print("Title of PR:", body["pull_request"]["title"])
                print("PR number is:", body["number"])
                print("Created by:",  body["sender"]["login"])
                print("Head branch is:", body["pull_request"]["head"]["ref"])
                branch = body["pull_request"]["base"]["ref"]
                print("Base branch is:", body["pull_request"]["base"]["ref"])
                print("No. of Files Changed:",  body["pull_request"]["changed_files"])
                subprocess.run("/path/to/sub-script", env={"BRANCH" : branch})
            else:
                print("A new Pull Request has been generated for:", body["pull_request"]["head"]["repo"]["name"])
                print("PR number is:", body["number"])
                print("Created by:",  body["sender"]["login"])
    else:
        raise HTTPException(status_code=401, detail="Invlaid Token")


def verify_signature(payload_body, request_hash):
    hmac_hash = hmac.new(os.environ['SECRET_TOKEN'].encode("utf-8"), payload_body, digestmod=sha256)
    expected_signature = "sha256=" + hmac_hash.hexdigest()
    return hmac.compare_digest(expected_signature, hash_val)
