# DO NOT EDIT!!! built with `python _building/build_setup.py`
import setuptools
setuptools.setup(
    name="k3jobq",
    packages=["k3jobq"],
    version="0.1.2",
    license='MIT',
    description='k3jobq processes a series of inputs with functions concurrently',
    long_description='# k3jobq\n\n[![Build Status](https://travis-ci.com/pykit3/k3jobq.svg?branch=master)](https://travis-ci.com/pykit3/k3jobq)\n![Python package](https://github.com/pykit3/k3jobq/workflows/Python%20package/badge.svg)\n[![Documentation Status](https://readthedocs.org/projects/k3jobq/badge/?version=stable)](https://k3jobq.readthedocs.io/en/stable/?badge=stable)\n[![Package](https://img.shields.io/pypi/pyversions/k3jobq)](https://pypi.org/project/k3jobq)\n\nk3jobq processes a series of inputs with functions concurrently\n\nk3jobq is a component of [pykit3] project: a python3 toolkit set.\n\n\nk3jobq is a manager to create cuncurrent tasks.\nIt processes a series of inputs with functions concurrently and\nreturn once all threads are done::\n\n    def add1(args):\n        return args + 1\n\n    def printarg(args):\n        print(args)\n\n    k3jobq.run([0, 1, 2], [add1, printarg])\n    # > 1\n    # > 2\n    # > 3\n\n\n\n# Install\n\n```\npip install k3jobq\n```\n\n# Synopsis\n\n```python\n\n#!/usr/bin/env python\n\nimport k3jobq\n\nif __name__ == "__main__":\n\n    def add1(args):\n        return args + 1\n\n    def multi2(args):\n        return args * 2\n\n    def printarg(args):\n        print(args)\n\n    k3jobq.run([0, 1, 2], [add1, printarg])\n    # > 1\n    # > 2\n    # > 3\n\n    k3jobq.run((0, 1, 2), [add1, multi2, printarg])\n    # > 2\n    # > 4\n    # > 6\n\n    # Specify number of threads for each job:\n\n    # Job \'multi2\' uses 1 thread.\n    # This is the same as the above example.\n    k3jobq.run(list(range(3)), [add1, (multi2, 1), printarg])\n    # > 2\n    # > 4\n    # > 6\n\n    # Create 2 threads for job \'multi2\':\n\n    # As there are 2 thread dealing with multi2, output order will not be kept.\n    k3jobq.run(list(range(3)), [add1, (multi2, 2), printarg])\n    # Output could be:\n    # > 4\n    # > 2\n    # > 6\n\n    # Multiple threads with order kept:\n\n    # keep_order=True to force to keep order even with concurrently running.\n    k3jobq.run(list(range(3)), [add1, (multi2, 2), printarg],\n               keep_order=True)\n    # > 2\n    # > 4\n    # > 6\n\n    # timeout=0.5 specifies that it runs at most 0.5 second.\n    k3jobq.run(list(range(3)), [add1, (multi2, 2), printarg],\n               timeout=0.5)\n\n    # Returning *k3jobq.EmptyRst* stops delivering result to next job:\n\n    def drop_even_number(i):\n        if i % 2 == 0:\n            return k3jobq.EmptyRst\n        else:\n            return i\n\n    k3jobq.run(list(range(10)), [drop_even_number, printarg])\n    # > 1\n    # > 3\n    # > 5\n    # > 7\n    # > 9\n\n```\n\n#   Author\n\nZhang Yanpo (张炎泼) <drdr.xp@gmail.com>\n\n#   Copyright and License\n\nThe MIT License (MIT)\n\nCopyright (c) 2015 Zhang Yanpo (张炎泼) <drdr.xp@gmail.com>\n\n\n[pykit3]: https://github.com/pykit3',
    long_description_content_type="text/markdown",
    author='Zhang Yanpo',
    author_email='drdr.xp@gmail.com',
    url='https://github.com/pykit3/k3jobq',
    keywords=['concurrent', 'python', 'job', 'thread', 'queue'],
    python_requires='>=3.0',

    install_requires=['semantic_version~=2.8.5', 'jinja2~=2.11.2', 'PyYAML~=5.3.1', 'sphinx~=3.3.1', 'k3ut~=0.1.7', 'k3thread~=0.1.0'],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Libraries',
    ] + ['Programming Language :: Python :: 3.6', 'Programming Language :: Python :: 3.7', 'Programming Language :: Python :: 3.8', 'Programming Language :: Python :: Implementation :: PyPy'],
)
