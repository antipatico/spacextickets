#!/usr/bin/env bash

if [ "${DEBUG}" ]; then
    set -x
fi

source "$(dirname $0)/functions.sh"

set -e

path=$(get_path)

pushd "${path}" > /dev/null
rm -f db.sqlite3
./manage.py migrate
popd > /dev/null
exit 0