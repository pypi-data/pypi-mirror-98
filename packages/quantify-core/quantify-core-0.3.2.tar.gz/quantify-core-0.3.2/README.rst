=============
Quantify-core
=============

.. image:: https://gitlab.com/quantify-os/quantify-core/badges/develop/pipeline.svg
    :target: https://gitlab.com/quantify-os/quantify-core/pipelines/

.. image:: https://img.shields.io/pypi/v/quantify-core.svg
    :target: https://pypi.org/pypi/quantify-core
.. image:: https://app.codacy.com/project/badge/Grade/32265e1e7d3f491fa028528aaf8bfa69
    :target: https://www.codacy.com/gl/quantify-os/quantify-core/dashboard?utm_source=gitlab.com&amp;utm_medium=referral&amp;utm_content=quantify-os/quantify-core&amp;utm_campaign=Badge_Grade
    :alt: Code Quality
.. image:: https://app.codacy.com/project/badge/Coverage/32265e1e7d3f491fa028528aaf8bfa69
    :alt: Coverage
    :target: https://www.codacy.com/gl/quantify-os/quantify-core/dashboard?utm_source=gitlab.com&amp;utm_medium=referral&amp;utm_content=quantify-os/quantify-core&amp;utm_campaign=Badge_Coverage
.. image:: https://readthedocs.com/projects/quantify-quantify-core/badge/?version=latest&token=2f68e7fc6a2426b5eb9b44bb2f764a9d75a9932f41c39efdf0a8a99bf33e6a34
    :target: https://quantify-quantify-core.readthedocs-hosted.com/en/latest/?badge=latest
    :alt: Documentation Status

.. image:: https://img.shields.io/badge/License-BSD%204--Clause-blue.svg
    :target: https://gitlab.com/quantify-os/quantify-core/-/blob/master/LICENSE
.. image:: https://img.shields.io/badge/code%20style-black-000000.svg
    :target: https://github.com/psf/black

Quantify is a python based data acquisition platform focused on Quantum Computing and solid-state physics experiments.
It is build on top of `QCoDeS <https://qcodes.github.io/Qcodes/>`_ and is a spiritual successor of `PycQED <https://github.com/DiCarloLab-Delft/PycQED_py3>`_.
Quantify currently consists of `quantify-core <https://pypi.org/project/quantify-core/>`_ and `quantify-scheduler <https://pypi.org/project/quantify-scheduler/>`_.

Take a look at the documentation for quantify-core `here <https://quantify-quantify-core.readthedocs-hosted.com/en/latest/?badge=latest>`_.

Quantify-core is the core module that contains all basic functionality to control experiments. This includes:

* A framework to control instruments.
* A data-acquisition loop.
* Data storage and analysis.
* Parameter monitoring and live visualization of experiments.


.. caution::

    This is a pre-release **alpha version**, major changes are expected. Use for testing & development purposes only.

About
--------

Quantify-core is maintained by The Quantify consortium consisting of Qblox and Orange Quantum Systems.

.. |_| unicode:: 0xA0
   :trim:


.. figure:: https://cdn.sanity.io/images/ostxzp7d/production/f9ab429fc72aea1b31c4b2c7fab5e378b67d75c3-132x31.svg
    :width: 200px
    :target: https://qblox.com
    :align: left

.. figure:: https://orangeqs.com/OQS_logo_with_text.svg
    :width: 200px
    :target: https://orangeqs.com
    :align: left

|_|


|_|

The software is free to use under the conditions specified in the license.


--------------------------
