"""
k3jobq is a manager to create cuncurrent tasks.
It processes a series of inputs with functions concurrently and
return once all threads are done::

    def add1(args):
        return args + 1

    def printarg(args):
        print(args)

    k3jobq.run([0, 1, 2], [add1, printarg])
    # > 1
    # > 2
    # > 3
"""

__version__ = "0.1.2"
__name__ = "k3jobq"

from .jobq import (
    EmptyRst,
    Finish,
    run,
    stat,
    JobManager,

    JobWorkerError,
    JobWorkerNotFound,
)

from .works import (
    limit_job_speed,
)

__all__ = [
    'EmptyRst',
    'Finish',
    'run',
    'stat',
    'JobManager',

    'JobWorkerError',
    'JobWorkerNotFound',
    'limit_job_speed',
]
