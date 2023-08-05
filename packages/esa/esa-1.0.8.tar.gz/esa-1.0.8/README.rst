Easy SimAuto (ESA)
==================
.. image:: https://img.shields.io/pypi/v/esa.svg
   :target: https://pypi.org/project/esa/
.. image:: https://joss.theoj.org/papers/10.21105/joss.02289/status.svg
   :target: https://doi.org/10.21105/joss.02289
.. image:: https://img.shields.io/pypi/l/esa.svg
   :target: https://github.com/mzy2240/ESA/blob/master/LICENSE

Easy SimAuto (ESA) is an easy-to-use Python package that simplifies
interfacing with PowerWorld's Simulator Automation Server (SimAuto). ESA
wraps all PowerWorld SimAuto functions, and also provides helper
functions to further simplify working with SimAuto. Wherever possible,
data is returned as Pandas DataFrames, making analysis a breeze. ESA is
well tested and fully `documented`_.

`Documentation`_
----------------

For quick-start directions, installation instructions, API reference,
examples, and more, please check out ESA's `documentation`_.

If you have your own copy of the ESA repository, you can also view the
documentation locally by navigating to the directory ``docs/html`` and
opening ``index.html`` with your web browser.

Citation
--------

If you use ESA in any of your work, please use the citation below.

.. code:: latex

    @article{ESA,
      doi = {10.21105/joss.02289},
      url = {https://doi.org/10.21105/joss.02289},
      year = {2020},
      publisher = {The Open Journal},
      volume = {5},
      number = {50},
      pages = {2289},
      author = {Brandon L. Thayer and Zeyu Mao and Yijing Liu and Katherine Davis and Thomas J. Overbye},
      title = {Easy SimAuto (ESA): A Python Package that Simplifies Interacting with PowerWorld Simulator},
      journal = {Journal of Open Source Software}
    }

Installation
------------

Please refer to ESA's `documentation <https://mzy2240.github
.io/ESA/html/installation.html>`__ for full, detailed installation
directions. In many cases, ESA can simply be installed by:

.. code:: bat

    python -m pip install esa

Testing Coverage
----------------

The ESA team works hard to ensure ESA is well tested, and we strive for
100% testing coverage. The table below shows the most up-to-date
testing coverage data for ESA, using `coverage
<https://pypi.org/project/coverage/>`__.

.. table:: ESA's testing coverage as of 2021-03-09 (Git commit: 90d968d)
    :widths: auto
    :align: left

    +-----------------+-------------------+-----------------+-----------------+--------------------+
    | Name            |   Num. Statements |   Missing Lines |   Covered Lines |   Percent Coverage |
    +=================+===================+=================+=================+====================+
    | esa/__init__.py |                 2 |               0 |               2 |                100 |
    +-----------------+-------------------+-----------------+-----------------+--------------------+
    | esa/saw.py      |               515 |               0 |             515 |                100 |
    +-----------------+-------------------+-----------------+-----------------+--------------------+

License
-------

`MIT <https://choosealicense.com/licenses/mit/>`__

Contributing
------------

We welcome contributions! Please read ``contributing.md``.

.. _documentation: https://mzy2240.github.io/ESA/
.. _documented: https://mzy2240.github.io/ESA/
