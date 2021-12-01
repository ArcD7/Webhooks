#!/bin/bash

cd /home/ubuntu/server/Webhooks
source /home/ubuntu/server/fastapi/bin/activate
source ~/.profile

exec gunicorn main:app --workers 1 --worker-class uvicorn.workers.UvicornWorker --bind 0.0.0.0:3000
