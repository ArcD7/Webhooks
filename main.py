from fastapi import FastAPI, Request, HTTPException
import subprocess
import os
from hashlib import sha256
import hmac
import json

app = FastAPI()


@app.post("/payload")
async def read_item(req: Request):
    body = await req.json() # Payload body in string.
    event = req.headers.get("X-Github-Event") # Extracts the type of EVENT from the request header. 
    request_hash = req.headers.get("X-Hub-Signature-256") # Extracts the hash value from the request header.
    payload_body = await req.body() # Payload body in bytes, required for creating hash locally.
    
    # We need to verify whether the request is coming from the right source(GitHub).
    verify = verify_signature(payload_body, request_hash)
    # If the request is verified, then we'll proceed with our process.
    if verify:
        print("Event Type:", event)
        # This checks for the Event type - eg: pull_request, ping, push.
        if event == "pull_request":
            pr_status = body["pull_request"]["merged"] # THis specifies whether PR is merged or not.
            print("PR Status:", body["action"]) # Action parameter specifies whether the PR is OPEN or CLOSED.
            print("Is Merged:", pr_status)
            # We'll proceed with the git pull process only if Event type is PR and is closed.
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
            else: # This will run if PR is open. 
                print("A new Pull Request has been generated for:", body["pull_request"]["head"]["repo"]["name"])
                print("PR number is:", body["number"])
                print("Created by:",  body["sender"]["login"])
    else:
        raise HTTPException(status_code=401, detail="Invlaid Token")

# This function creates a hash from the secret token and then compares it with the one that was in the request. 
# Returns a Boolean values
def verify_signature(payload_body, request_hash):
    hmac_hash = hmac.new(os.environ['SECRET_TOKEN'].encode("utf-8"), payload_body, digestmod=sha256)
    expected_signature = "sha256=" + hmac_hash.hexdigest() # Prefix added as per GitHub Signature format.
    return hmac.compare_digest(expected_signature, request_hash)
