Changes made with each ESA release are listed here. Please note that
versions prior to 1.0.0 are not listed here, but are still available on
`PyPi <https://pypi.org/project/esa/#history>`__.

Version 1.0.8
^^^^^^^^^^^^^

* Add new helper function 'to_graph'. The new function could help
  generate NetworkX graph model from the case, in two different levels:
  bus-as-node and substation-as-node. Parallel lines are preserved, and
  directedgraph is supported (currently the direction is fixed to be
  the same as real power flow).

Version 1.0.7
^^^^^^^^^^^^^

* Add new functions: get_ybus, get_jacobian

Version 1.0.6
^^^^^^^^^^^^^

* Hopefully finally fixing locale-based issues. Fixes began in 1.0.4,
  and continued in 1.0.5.
* Finalizing JOSS paper. Once published, the citation will be added to
  the top-level README and the documentation.

Version 1.0.5
^^^^^^^^^^^^^

* It turns out version 1.0.4 did not fully/correctly handle automatic
  locale setting. This version should now properly handle different
  decimal delimiters automatically.
* Bug fix: The ``additional_fields`` parameter to ``SAW``'s
  ``get_power_flow_results`` was permanently adding the
  ``additional_fields`` to the corresponding list in the ``SAW``
  object's ``SAW.POWER_FLOW_FIELDS`` attribute.

Version 1.0.4
^^^^^^^^^^^^^

* Added support for other locales by automatically detecting the
  system's decimal delimiter. This should allow users in Europe and
  elsewhere to leverage ESA. Thanks to
  `robinroche <https://github.com/robinroche>`__ for pointing out the
  problem during our `JOSS <https://joss.theoj.org/>`__ review in
  `this comment <https://github.com/openjournals/joss-reviews/issues/2289#issuecomment-643482550>`__.

Version 1.0.3
^^^^^^^^^^^^^

* New SAW attribute, ``build_date``
* New SAW attribute, ``version``
* New SAW helper method, ``get_version_and_builddate``
* Add argument ``additional_fields`` for ``get_power_flow_results`` method
  which provides an easy and consistent way to add more fields to the power
  flow result
* Updating so that ESA is compatible with Simulator version 17. Note
  that this does not imply ESA has been tested with versions 16, 18, 19,
  or 20. However, ESA *should* work with all these versions.
* Added case files for Simulator versions 16-22(beta) and renamed the cases
  accordingly (suffixed with ``pws_version_<version goes here>.pwb``.
* Updated documentation to discuss different versions of Simulator.

Version 1.0.2
^^^^^^^^^^^^^

* Add area number to the power flow result
* Update the citation section
* Fix a bug in the test file that will result in a failure if some
  default names are changed in PowerWorld

Version 1.0.1
^^^^^^^^^^^^^

* Add new functions: update_ui, OpenOneline and CloseOneline
* Add documents to meet the requirement of JOSS
* Add one more example into the documentation
* Update the coverage_to_rst.py so that it's more clear that the errors
  that get printed during testing are as expected.
* Update the release process
* Fix minor typos

Version 1.0.0
^^^^^^^^^^^^^

ESA version 1.0.0 is the first ESA release in which 100% of SimAuto
functions are wrapped, and testing coverage is at 100%.
