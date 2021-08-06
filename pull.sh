#!/usr/bin/expect -f
cd /home/archit/Webhooks

echo "$BRANCH"
#check the current branch --- git branch

# if git branch == $ from python branch
# and no commits pending 
# then run git pull
# else run git stash then git pull 
# else run git checkout to python branch
# run git pull

spawn git pull
#expect "name"
#send "<Username>\r"
#expect "ass"
#send "<Password>\r"
interact
