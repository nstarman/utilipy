#!/usr/bin/env python
# -*- coding: utf-8 -*-

#############################################################################
""" parallel_map code with support for LenGen generator expressions.

LenGen generators are generator functions wrapped with LenGen
see ..collections.generators
The advantage of using generators as input is to move all expensive
    calculations to inside the parallelized code.

This code is modified from code in galpy, which in turn sourced code
from Brian Refsdal. galpy attribution to Brian Refsdal below.

#############################################################################

Brian Refsdal's parallel_map, from astropython.org
Not sure what license this is released under, but until I know better:

Copyright (c) 2010, Brian Refsdal
All rights reserved.

Redistribution and use in source and binary forms, with or without
modification, are permitted provided that the following conditions are
met:

1. Redistributions of source code must retain the above copyright
notice, this list of conditions and the following disclaimer.

2. Redistributions in binary form must reproduce the above copyright
notice, this list of conditions and the following disclaimer in the
documentation and/or other materials provided with the distribution.

3. The name of the author may not be used to endorse or promote
products derived from this software without specific prior written
permission.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
"AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT
HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
(INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

#############################################################################
Planned Features
experimental: support for arbitary generators if a len is provided to
    parallel_map via _lenseq

"""


#############################################################################
# Imports

from __future__ import print_function
import platform
import numpy as np

try:
    # May raise ImportError
    import multiprocessing

except ImportError as e:
    _multi = False
else:
    _multi = True

try:
    # May raise NotImplementedError
    _ncpus = multiprocessing.cpu_count()
except NotImplementedError as e:
    _ncpus = 1

try:
    # from tqdm.autonotebook import tqdm as TQDM
    from tqdm import tqdm as TQDM
except ImportError:
    # class TQDM(object):
    #     """docstring for TQDM"""

    #     def __init__(self, x, *args, **kw):
    #         super(TQDM, self).__init__()
    #         self.x = x

    #     def __call__(self, x, *args, **kw):
    #         return self.x

    #     def set_postfix(self, *args, **kw):
    #         pass
    TQDM = lambda x, *args, **kw: x

# Custom Imports
from ..collections.generators import LenGen

#############################################################################
# Code


__all__ = ('parallel_map',)


def worker(f, ii, chunk, out_q, err_q, lock, tqdm=TQDM):
    """
    A worker function that maps an input function over a
    slice of the input iterable.

    :param f  : callable function that accepts argument from iterable
    :param ii  : process ID
    :param chunk: slice of input iterable
    :param out_q: thread-safe output queue
    :param err_q: thread-safe queue to populate on exception
    :param lock : thread-safe lock to protect a resource
         ( useful in extending parallel_map() )
    """
    # initializing
    vals = []
    sec = '\tWorker {}: len={}'.format(ii, len(chunk))

    # iterate over slice
    for val in tqdm(chunk, leave=True, desc=sec):
        try:
            result = f(val)
        except Exception as e:
            err_q.put(e)
            return

        vals.append(result)

    # output the result and task ID to output queue
    out_q.put((ii, vals))


def run_tasks(procs, err_q, out_q, num, tqdm=TQDM, _print=False):
    """
    A function that executes populated processes and processes
    the resultant array. Checks error queue for any exceptions.

    :param procs: list of Process objects
    :param out_q: thread-safe output queue
    :param err_q: thread-safe queue to populate on exception
    :param num : length of resultant array

    """
    # function to terminate processes that are still running.
    die = (lambda vs: [v.terminate() for v in vs if v.exitcode is None])

    try:
        for proc in procs:
            proc.start()

        # tqdm.set_postfix(tqdm, status='joining tasks')

        for proc in procs:
            proc.join()

    except Exception as e:
        # kill all slave processes on ctrl-C
        try:
            die(procs)
        finally:
            raise e

    else:
        # tqdm.set_postfix(status='finished tasks')
        pass

    if not err_q.empty():
        # kill all on any exception from any one slave
        try:
            die(procs)
        finally:
            raise err_q.get()

    # Processes finish in arbitrary order. Process IDs double
    # as index in the resultant array.
    results = [None] * num  # TODO I think I can speed this up
    while not out_q.empty():
        idx, result = out_q.get()
        results[idx] = result

    # Remove extra dimension added by array_split
    return list(np.concatenate(results))


def parallel_map(function, sequence, func_args=[], func_kw={}, numcores=None,
                 _lenseq=None, _progressbar=True, _print=False):
    """
    A parallelized version of the native Python map function that
    utilizes the Python multiprocessing module to divide and
    conquer sequence.

    :param function: callable function that accepts argument from iterable
    :param sequence: iterable sequence
    :param numcores: number of cores to use
    """
    if not callable(function):
        raise TypeError(f"input function {function} is not callable")

    if not np.iterable(sequence):
        raise TypeError(f"input {sequence} is not iterable")

    if _progressbar:
        tqdm = TQDM
    else:
        tqdm = lambda x, *args, **kw: x

    size = len(sequence)

    func = lambda x: function(x, *func_args, **func_kw)

    if not _multi or size == 1:
        return map(func, sequence)

    if numcores is None:
        numcores = _ncpus

    if platform.system() == 'Windows':  # JB: don't think this works on Win
        return list(map(func, sequence))

    # Returns a started SyncManager object which can be used for sharing
    # objects between processes. The returned manager object corresponds
    # to a spawned child process and has methods which will create shared
    # objects and return corresponding proxies.
    manager = multiprocessing.Manager()

    # Create FIFO queue and lock shared objects and return proxies to them.
    # The managers handles a server process that manages shared objects that
    # each slave process has access to. Bottom line -- thread-safe.
    out_q = manager.Queue()
    err_q = manager.Queue()
    lock = manager.Lock()

    # if sequence is less than numcores, only use len sequence number of
    # processes
    if size < numcores:
        numcores = size

    # group sequence into numcores-worth of chunks
    if issubclass(sequence.__class__, LenGen):
        inds = np.array_split(np.arange(len(sequence)), numcores)
        sequence = [sequence.islice(ii[0], ii[-1] + 1) for ii in inds]
    elif _lenseq is not None:  # might be generator-like
        try:  # try straight numpy splitting
            sequence = np.array_split(sequence, numcores)
        except np.AxisError as e:  # try it as a generator
            inds = np.array_split(np.arange(_lenseq), numcores)
            sequence = LenGen(sequence, _lenseq)
            try:
                sequence = [sequence.islice(ii[0], ii[-1] + 1) for ii in inds]
            except Exception as e:
                raise Exception('could not split or slice')
    else:
        try:  # try straight numpy splitting
            sequence = np.array_split(sequence, numcores)
        except np.AxisError as e:  # try it as a generator
            raise np.AxisError('axis supplied was invalid. If generator, need _lenseq')

            # if _lenseq is not None:
            #     inds = np.array_split(np.arange(_lenseq), numcores)
            #     sequence = LenGen(sequence, _lenseq)
            #     try:
            #         sequence = [sequence.islice(ii[0], ii[-1] + 1) for ii in inds]
            #     except Exception as e:
            #         raise Exception('could not split or slice')
            # else:
            #     raise ValueError('need _lenseq')

    procs = [multiprocessing.Process(target=worker,
                                     args=(func, ii, chunk,
                                           out_q, err_q, lock, tqdm))
             for ii, chunk in enumerate(tqdm(sequence, desc='Master Loop'))]

    return run_tasks(procs, err_q, out_q, numcores, tqdm=tqdm, _print=_print)


if __name__ == "__main__":
    """
    Unit test of parallel_genmap()

    Create an arbitrary length list of references to a single
    matrix containing random floats and compute the eigenvals
    in serial and parallel. Compare the results and timings.
    """

    import time

    numtasks = 5
    size = (512, 512)

    vals = np.random.rand(*size)
    f = np.linalg.eigvals

    iterable = [vals] * numtasks

    print('Running np.linalg.eigvals %iX on matrix size [%i,%i]' %
          (numtasks, size[0], size[1]))

    tt = time.time()
    presult = parallel_map(f, iterable)
    print('parallel map in %g secs' % (time.time() - tt))

    tt = time.time()
    result = map(f, iterable)
    print('serial map in %g secs' % (time.time() - tt))

    assert (np.asarray(result) == np.asarray(presult)).all()
