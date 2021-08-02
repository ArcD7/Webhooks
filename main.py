from fastapi import FastAPI,Request
import subprocess
import os
import base64
from hashlib import sha256
import hmac

app = FastAPI()


@app.post("/payload")
async def read_item(req: Request):
    body = await req.json()
    event = req.headers.get("X-Github-Event")
    hash_val = req.headers.get("X-Hub-Signature-256")
    verify_signature(body, hash_val)
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
            print("Base branch is:", body["pull_request"]["base"]["ref"])
            print("No. of Files Changed:",  body["pull_request"]["changed_files"])
            subprocess.call("/home/archit/Webhooks/pull.sh")
        else:
            print("A new Pull Request has been generated for:", body["pull_request"]["head"]["repo"]["name"])
            print("PR number is:", body["number"])
            print("Created by:",  body["sender"]["login"])

def verify_signature(body, hash_val):
    hmac_hash = hmac.new(str(os.environ['SECRET_TOKEN']).encode("utf-8"), str(body).encode("utf-8"), digestmod=sha256)
    expected_signature = hmac_hash.hexdigest()
    print(expected_signature)
    print(hash_val)
    if expected_signature != hash_val:
        raise Exception('Warning: the webhook signatures do not match!')
    print('The webhook signatures match!')

