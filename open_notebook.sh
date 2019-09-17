#!/bin/bash

###############################################################################
### Notes
#
#
#
###############################################################################


###############################################################################
### RUN

# Read correct anaconda environment
source envs/main_env.sh

# Activate the correct anaconda environment
source activate ./envs/$main_env

# Open a jupyter notebook
jupyter lab ./

###############################################################################
### END
