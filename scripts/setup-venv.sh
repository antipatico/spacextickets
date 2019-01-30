#!/usr/bin/env bash
set -e
python3 -m pip install virtualenv --user
python3 -m virtualenv venv
source venv/bin/activate
python3 -m pip install -r requirements.txt
deactivate
