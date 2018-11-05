#!/bin/bash
#
# This script can retrieve backware
# dependencies from a SBo repository
# 

SBO_REPO_DIR="/var/lib/sbopkg/SBo-git/"

function on_error
{
  echo -e "\033[91m${@}\033[0m"
  exit 1
}


function list_deps
{
  echo -e "\033[93m[+]Reverse dependencies for: \033[97m${@}\033[0m"
    for PKG in $(find ${SBO_REPO_DIR} -type f -iname "*.info" | xargs fgrep ${1} | grep REQUIRES | cut -d: -f1)
  do
        DEP=$(basename ${PKG} .info)
        if [ "${DEP}" != "${1}" ];
        then
          echo -e "\033[95m '-> $(basename ${PKG} .info)\033[0m"
        fi
  done
}

if [ $# -eq 1 ]; then
  list_deps $1
else
  on_error "Usage: $0 <package name>"
fi
