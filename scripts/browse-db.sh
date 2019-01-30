#!/usr/bin/env bash

if [ "${DEBUG}" ]; then
    set -x
fi

source "$(dirname $0)/functions.sh"

set -e

path=$(get_path)
pushd "${path}" > /dev/null
sqlitebrowser db.sqlite3 > /dev/null 2>&1 &
popd > /dev/null
exit 0