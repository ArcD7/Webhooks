#!/usr/bin/expect -f
cd /path/to/repository
spawn git pull
expect "name"
send "<Username>\r"
expect "ass"
send "<Password>\r"
interact
