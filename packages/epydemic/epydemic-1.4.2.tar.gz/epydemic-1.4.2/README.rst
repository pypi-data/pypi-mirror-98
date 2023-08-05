epydemic: Epidemic simulations on networks in Python
=====================================================

.. image:: https://badge.fury.io/py/epydemic.svg
    :target: https://badge.fury.io/py/epydemic

.. image:: https://readthedocs.org/projects/pyepydemic/badge/?version=latest
    :target: https://pyepydemic.readthedocs.io/en/latest/index.html

.. image:: https://api.travis-ci.com/simoninireland/epydemic.svg?branch=master
    :target: http://travis-ci.com/github/simoninireland/epydemic

.. image:: https://coveralls.io/repos/github/simoninireland/epydemic/badge.svg?branch=master
    :target: https://coveralls.io/github/simoninireland/epydemic?branch=master


Overview
--------

``epydemic`` is a Python library that implements simulations of epidemic
(and other) processes on networks. Epidemic processes are very
important in both network science and its applications. The most
common application is to study the ways in which diseases progress in
different network conditions, depending on their infectiousness and
other properties.

``epydemic`` provides simulation under synchronous and stochastic (Gillespie) dynamics,
using the well-known ``networkx`` package to represent and manipulate
networks. It supports a generic model for compartmented models of
disease with several standard models provided and which can be
extended to other, more complex, diseases. It also supports other
network processes such as addition-deletion networks.

``epydemic`` is built on top of the ``epyc`` experiment management library,
allowing simulations to be conducted at scale on individual machines,
multicore machines, and parallel computing clusters.


Installation
------------

You can install ``epydemic`` directly from PyPi using ``pip``:

::

   pip install epydemic

The master distribution of ``epydemic`` is hosted on GitHub. To obtain a
copy, just clone the repo:

::
   
    git clone git@github.com:simoninireland/epydemic.git
    cd epydemic
    python setup.py install


   
Documentation
-------------

API documentation for `epydemic` is available on `ReadTheDocs <https://pyepydemic.readthedocs.io/en/latest/>`_
(please note the slightly different project name).



Author and license
------------------

Copyright (c) 2017-2020, Simon Dobson <simoninireland@gmail.com>

Licensed under the `GNU General Public License v2 or later (GPLv2+) <http://www.gnu.org/licenses/gpl.html>`_.

