#!/usr/bin/env bash

if [ "${DEBUG}" ]; then
    set -x
fi

source "$(dirname $0)/functions.sh"

SU_EMAIL='root@localhost'

set -e

path=$(get_path)

pushd "${path}" > /dev/null
cat << EOF | ./manage.py shell
from sys import exit
from spacextickets.accounts.models import User

if User.objects.filter(email="root@localhost").exists():
  su = User.objects.get(email="$SU_EMAIL")
  su.delete()
else:
  print("Super user account doesn't exist!")
  exit(1)
EOF
popd > /dev/null
exit 0