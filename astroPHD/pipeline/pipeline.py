#!/usr/bin/env python
# -*- coding: utf-8 -*-

# ----------------------------------------------------------------------------
#
# TITLE   : src initialization
# AUTHOR  : Nathaniel Starkman
# PROJECT : Palomar 5 in Gaia DR2
#
# ----------------------------------------------------------------------------

### Docstring and Metadata
"""main initialization file

TODO CHANGE from single folder paradigm to the scripts folder format
"""

__author__ = "Nathaniel Starkman"

##############################################################################
### Imports

# Project-Specific
from .util import LogFile, ObjDict


###############################################################################
### Parameters

_LOGFILE = LogFile(header=False)  # PrintLog, which is compatible with LogFile


##############################################################################
### Pipeline

class SequentialPipeline(object):
    """docstring for ClassName"""

    def __init__(self, steps):
        """
        steps : list
            (name, action)
            action class needs a .run method
        """
        self.steps = steps

        return
    # /def

    def run(startkw, # **stepsargs
            ):
        """
        startkw :
            starting kwargs
        # stepsargs: dict
        #     {step name: {dict of kwargs}}

        TODO
            options on the steps?
            right now each step can only pass input directly to next event
        """
        res = startkw  # input for first step

        for name, step in steps:

            inreskw = {k: res[k] for k in step._input_kwargs_names}
            inreskw.update(stepsargs.get(name, {}))

            res = step.run(pipeline_mode=True, **inreskw)

        return res
    # /def

    def describe_pipeline():
        print('TODO')

    # @classmethod
    # def decorator(cls, func=None):
    #     print('TODO')
    #     return


# -------------------------------------------------------------------------

def make_pipeline(steps):
    # TODO get name of each step automatically using inspect
    return SequentialPipeline(steps)

# -------------------------------------------------------------------------

##############################################################################
### END
