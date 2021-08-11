#!/bin/bash -i
ssh # An alias in bashrc which run the ssh-agent.
ssh_add # An alias in bashrc which provides the private key to the agent.

cd /path/to/directory # The path to your git repository.

# This command will save the name of current branch in a variable.
current_branch=$(git branch | grep "*" | sed 's/*//' | sed 's/^ *//g')

# This command will check the current status of the branch for any commited or uncommited file.
git_status=$(git status | sed -n '2p' | sed 's/:\+$//')
staged_commits="Changes to be committed"
unstaged_commits="Changes not staged for commit"

# Checks whether the current branch is same as the branch for which the PR has been generated.
if [[ "$current_branch" == "$BRANCH" ]]; then
	# If the branch is same and there are changes to be commited then,
        if [[ "$git_status" == "$staged_commits" || "$git_status" == "$unstaged_commits" ]]; then
                git stash 			# Stash the code
                git pull			# Pull code from the origin
        # In case the working tree is clean, the changes will be pulled directly.
	else
                git pull
        fi  # FOR loop closed.
# If the current branch is not the same as the one for which PR has been generated.
else
	# If there are changes to be commited then,
        if [[ "$git_status" == "$staged_commits" || "$git_status" == "$unstaged_commits" ]]; then
                git stash 			# Stash the code
                git checkout $BRANCH 		# Checkout the branch
                git pull			# Pull code from the origin
        # In case the working tree is clean, checkout the branch and pull from origin.
	else
                git checkout $BRANCH   	
                git pull
	fi
fi # Main FOR loop closed.
