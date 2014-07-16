#! /usr/bin/env python

import os
import sys
import multiprocessing as mp
import subprocess
import time
import signal
from Queue import Empty
import numpy as np
import csv
import datetime
import json

F_LIST = [
    '__job__activity',
    'job_num',
    'job_tot',
    'duration_sec',
    'duration_min',
    'pid',
    'time_stamp',
    'cmd']


# ============================================================================
def _worker(q, verbose=False, suppress_cmd=True, suppress_stdout=False,
            suppress_stderr=False):

    # --- set destination of stderr and stdout
    stdout = subprocess.PIPE if suppress_stdout else None
    stderr = subprocess.PIPE if suppress_stderr else None

    # --- loop forever until sentinal is received
    while True:
        # --- pull the job params from the queue
        job_num, job_tot, cmd, stay_alive = q.get()

        # --- die if sentinal received
        if not stay_alive:
            q.task_done()
            return

        # --- take care of special case of not verbose but show commands
        if (not verbose) and (not suppress_cmd):
            print cmd
            sys.stdout.flush()

        # --- write starting message if verbose
        if verbose:
            # --- define a record for logging
            rec = {
                '__job__activity': '__job__start',
                'job_num': job_num,
                'job_tot': job_tot,
                'time_stamp': str(datetime.datetime.now()),
                'duration_sec': '',
                'duration_min': '',
                'pid': os.getpid(),
                'cmd': cmd,
                }
            # --- suppress command if requested
            if suppress_cmd:
                rec['cmd'] = ''

            # --- write the verbose line
            writer = csv.DictWriter(sys.stdout, F_LIST, extrasaction='ignore')
            writer.writerow(rec)
            sys.stdout.flush()

        # --- run the command under bash and wait for it to end
        then = datetime.datetime.now()
        p = subprocess.Popen(['bash', '-c', cmd], stdout=stdout,
                             stderr=stderr)
        p.wait()

        # --- compute how long the job took
        now = datetime.datetime.now()
        dt = now - then
        seconds = 3600 * 24 * dt.days + dt.seconds + dt.microseconds / 1e6
        minutes = seconds / 60.

        # --- write ending message if verbose
        if verbose:
            rec['__job__activity'] = '__job__end'
            rec['time_stamp'] = now
            rec['duration_sec'] = seconds
            rec['duration_min'] = minutes
            writer = csv.DictWriter(sys.stdout, F_LIST, extrasaction='ignore')
            writer.writerow(rec)
            sys.stdout.flush()

        # --- tell the queue that this task is done
        q.task_done()


# ============================================================================
def parallel(cmd_list, njobs=None, verbose=False, suppress_cmd=True,
             suppress_stdout=False, suppress_stderr=False,
             assume_hyperthread=True):

    # --- make sure commands are stripped
    cmd_list = [c.strip() for c in cmd_list]

    # --- fill a joinable cueue with commands
    queue = mp.JoinableQueue()

    # --- determine the number of cores
    n_cores = mp.cpu_count()
    if assume_hyperthread:
        if (n_cores % 2) == 0:
            n_cores = n_cores / 2

    # --- set the number of jobs to default if necesarry
    if njobs is None:
        njobs = n_cores

    # --- initialize an empty process list
    p_list = []

    # --- take command of of field list if it is to be suprressed
    if suppress_cmd:
        F_LIST.pop(-1)

    if verbose:
        # --- write csv header
        writer = csv.DictWriter(sys.stdout, F_LIST)
        writer.writeheader()
        sys.stdout.flush()

    # --- spin up njobs workers to tackle the queue
    for nn in range(njobs):
        p = mp.Process(target=_worker, args=(queue, verbose, suppress_cmd,
                       suppress_stdout, suppress_stderr))
        p.start()
        p_list.append(p)

    # ---
    for ind, cmd in enumerate(cmd_list):
        job_num, job_tot = ind + 1, len(cmd_list)
        keep_alive = True
        queue.put((job_num, job_tot, cmd, keep_alive))

    # --- wait until the queue is done
    queue.join()

    # --- kill workers
    for p in p_list:
        keep_alive = False
        queue.put((0, 0, '', keep_alive))
    queue.join()

    # --- wait until all processes are done
    for p in p_list:
        p.join()

# ============================================================================
if __name__ == '__main__':
    cmd_list = sys.stdin.readlines()
    parallel(cmd_list)