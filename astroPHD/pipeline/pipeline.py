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
# from .util import LogFile, ObjDict


###############################################################################
### Parameters

# _LOGFILE = LogFile(header=False)  # LogPrint, which is compatible with LogFile


##############################################################################
### Multi-Linked List

# TODO implement many-to-many version

class Node:
    """
    """

    def __init__(self, data):
        self.item = data
        self.nref = None
        self.pref = None
    # /def


# -------------------------------------------------------------------------
# from https://stackabuse.com/doubly-linked-list-with-python-examples/

# TODO implement many-to-many version
# but this requires being able to resolve call order based on dependency

class DoublyLinkedList:
    def __init__(self, start_node=None):
        self.start_node = start_node

    # TODO


##############################################################################
### Pipeline

class Pipeline(object):

    def __init__(self, *steps):
        """
        steps : list
            action class needs a .run method
        """

        self.steps = steps
        # TODO process functions which are not PipelineFunctions as (name, func)
        # TODO steps should be a multi-linked list

        return
    # /def

    def run(self, startkw={}, **stepsargs):
        """
        """

        kw = startkw  # input for first step

        #
        if set(startkw.keys()).difference(self.steps[0]._inargnames):
            raise ValueError

        for step in self.steps:

#             stepkw = {k: kw[k] for k in step._inargnames if k in kw}
            stepkw = kw  # TODO some check that a) passing right args b) not passing extra args?
            stepkw.update(stepsargs.get(step.name, {}))

            # print(step.name, stepkw, step._defaults, step._outargnames)

            # TODO put this inside step.run()
            for n1, n2 in step._inargnames.items():
                if n1 in kw:
                    stepkw[n2] = stepkw.pop(n1)

            # print(step.name, stepkw, step._defaults)

            kw = step.run(**stepkw)

            # print('kw:', kw)

        return kw
    # /def


# -------------------------------------------------------------------------

# def make_pipeline(steps):
#     # TODO get name of each step automatically using inspect
#     return SequentialPipeline(steps)
# # /def 

# -------------------------------------------------------------------------

##############################################################################
### END
