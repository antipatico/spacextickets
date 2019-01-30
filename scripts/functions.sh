#!/usr/bin/env bash

get_path() {
    if [ -f "spacextickets/manage.py" ]; then
        echo "spacextickets"
    elif [ -f "manage.py" ]; then
        echo "."
    elif [ -f "../spacextickets/manage.py" ]; then
        echo "../spacextickets"
    elif [ -f "../../spacextickets/manage.py" ]; then
        echo "../../spacextickets"
    else
        echo "ERROR: Can't determine manage.py location." >&2
        exit 1
    fi
}