#!/usr/bin/env bash

if [ "${DEBUG}" ]; then
    set -x
fi

gitinspector "$1" -F htmlembedded -HlmrTw --file-types="py,sh,html,po" --since=2018-05-24 --exclude="manage.py" --exclude="migrations"
exit 0