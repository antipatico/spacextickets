#!/usr/bin/env bash

if [ "${DEBUG}" ]; then
    set -x
fi

set -e

$(dirname $0)/drop-db.sh
$(dirname $0)/create-super-user.sh
$(dirname $0)/populate-db.sh
exit 0
