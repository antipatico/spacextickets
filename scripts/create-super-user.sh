#!/usr/bin/env bash

if [ "${DEBUG}" ]; then
    set -x
fi

source "$(dirname $0)/functions.sh"

SU_EMAIL='root@localhost'
SU_PASSWORD='hunter2'
SU_NAME='root'
SU_SURNAME='root'

set -e

[ -n "$1" ] && SU_EMAIL="$1"
[ -n "$2" ] && SU_PASSWORD="$2"

path=$(get_path)

pushd "${path}" > /dev/null
cat << EOF | ./manage.py shell
from sys import exit
from spacextickets.accounts.models import User

if not User.objects.filter(email="${SU_EMAIL}").exists():
  User.objects.create_superuser(email="${SU_EMAIL}", password="${SU_PASSWORD}", first_name="${SU_NAME}", last_name="${SU_SURNAME}")
else:
  print("Super user account already exists!")
  exit(1)
EOF
popd > /dev/null
exit 0
