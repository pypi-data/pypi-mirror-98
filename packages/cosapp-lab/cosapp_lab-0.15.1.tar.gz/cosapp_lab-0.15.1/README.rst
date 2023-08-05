============================================================================
CosApp Lab - Toolbox for managing and deploying CoSApp powered dashboards.
============================================================================

The primary goal of **CoSApp Lab** is to help users transform theirs existing CoSApp 
library into a interactive dashboard with almost no additional development or
configuration.

**************
Documentation
**************
A more detailed **CoSApp Lab** documentation is available at:

https://cosapplab.readthedocs.io
   

*************
Installation
*************

Stable release
================

The easiest way to obtain `cosapp_lab` is to install the conda package:

.. code-block:: console

    conda install cosapp_lab

`cosapp_lab` is also available on PyPI but since `pythonocc-core` is not, users can install `cosapp_lab` with *pip* but the 3D viewer widget will not work.

.. code-block:: console

    pip install cosapp_lab

*JupyterLab* is not a direct dependency of *cosapp_lab* but users need to have JupyterLab (>3.0) in order to create the CoSApp dashboard in notebook.  

Development
=============

Setup development environment
------------------------------

.. code-block:: python

    # create a new conda environment
    conda create -n cosapplab -c conda-forge python jupyterlab nodejs
    conda activate cosapplab

    # download cosapp_lab from gitlab
    git clone --recursive https://gitlab.com/cosapp/cosapp_lab.git

    # install JS dependencies, build and install JupyterLab extension in development mode 
    cd cosapp_lab
    jlpm install
    jlpm build:all
    jlpm install:extension

    # install cosapp_lab in editable mode
    python -m pip install -e .

Testing
----------


.. code-block:: python

    # Test python code
    python -m pytest

    # Test typescript code
    jlpm test



Build documents
----------------

.. code-block:: console

    cd docs
    sphinx-build -b html -d _build/doctrees . _build

