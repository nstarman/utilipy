# !/usr/bin/env bash

# bash script to pull branch & update all submodules

# TO USE:
#  1) cd to this directory
#  2) check this script is executable with:
#     >> chmod +x gitpull.sh
#  3) run with:
#     >> bash gitpull.sh

###############################
# SCRIPT

# pull branch
git pull

# update submodules
git submodule update --recursive --remote

# Below this is for first time you get submodule
# git submodule update --init --recursive

###############################
# END
