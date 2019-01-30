#!/usr/bin/env bash
set -e
./scripts/clear-all.sh
./scripts/setup-venv.sh
source venv/bin/activate
pushd spacextickets
./manage.py compilemessages
popd
./scripts/refresh-db.sh
deactivate
