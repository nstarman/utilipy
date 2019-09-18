#!/bin/bash

###############################################################################
### Notes
# only works on linux/mac environment, TODO: make general version
#
#
###############################################################################


###############################################################################
### RUN

# Read correct Anaconda environment
source envs/main_env.sh

# Activate the correct Anaconda environment
source activate ./envs/$main_env

# Open a jupyter notebook
jupyter lab ./

###############################################################################
### ChangeLog
# file written by James Lane
# rewritten by Nathaniel Starkman for arbitary Anaconda env, not prespecified

###############################################################################
### END
