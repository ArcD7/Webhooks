#!/bin/bash -i
ssh
ssh_add

cd /path/to/script
echo "$BRANCH"

current_branch=$(git branch | grep "*" | sed 's/*//' | sed 's/^ *//g')
echo "$git_branch"

git_status=$(git status | grep "Changes to be committed")
echo "$git_status"

#check the current branch is same as git branch output
if [ $current_branch==$BRANCH ]; then
        if [ "$git_status"=="Changes to be committed" ]; then
                git stash
                git pull
        else
                git pull
        fi
else
        if [ $git_status== "Changes to be committed" ]; then
                git stash
                git checkout $BRANCH
                git pull
        else
                git checkout $BRANCH
                git pull
	fi
fi