#!/bin/bash

if [ -z "$1" ]; then
    echo '请提供注释'
    exit 1
fi


git_push()
{
    local desc=$1

    git add -A .
    git commit -m "$desc"
    git push -u origin master
}


git_push "$1"
