#!/bin/bash

if [ $# -eq 2 ]
then
    wget --load-cookies /tmp/cookies.txt "https://drive.usercontent.google.com/download?id=${1}&export=
    download&authuser=0&confirm=$(wget --quiet --save-cookies /tmp/cookies.txt --keep-session-cookies 
        --no-check-certificate "https://drive.usercontent.google.com/uc?id=${1}&export=download" -O- | 
        sed -rn 's/.*confirm=([0-9A-Za-z_]+).*/\1\n/p')&id=https://drive.usercontent.google.com/uc?id=${1}&authuser=0&export=download" -O ${2} && rm -rf /tmp/cookies.txt
else
    echo "Not correct args"
    echo ${1}
fi