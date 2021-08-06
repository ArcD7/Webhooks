#!/bin/bash -i
ssh
ssh_add

cd /home/archit/Webhooks
echo "$BRANCH"

git_branch=$(git branch | grep "*" | sed 's/*//' | sed 's/^ *//g')
echo "$git_branch"

git_status=$(git status | grep "Changes to be committed")
echo "$git_status"

#check the current branch is same as git branch output
if [ $git_branch=="local" ]; then
	if [ "$git_status"=="Changes to be committed" ]; then
		echo "git stash"
		git pull
	else
		git pull
	fi
else
	if [ $git_status== "Changes to be committed" ]; then
		echo "Perform git stash"
		echo "Perform git checkout to the specific branch"
		echo "Perform git pull"
	else
		echo "Perform git checkout to the specific branch"
		echo "Perform git pull"
	fi

fi

