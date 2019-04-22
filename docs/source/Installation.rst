Installation guide
========================

Requirements
-----------------------

**Python**

Python 3.7.* is required because of some features and better performance


**External packages requirement**


* ``PyQt5`` - Graphical interface
* ``click`` - Console interface
* ``antlr4-python3-runtime`` - Knowledge base language parser
* ``multi_key_dict`` - Package for multi key dictionary support


Installation
-----------------------

It is recommended to use virtual environment because of possible problem with PyQt version conflicts.

.. code-block:: bash

    git clone https://gitlab.fit.cvut.cz/bi-zns_pracovni/zna_framework_python
    cd zns_framework_python
    pip install -r requirements.txt # use flag -user if your are not using virtual environment


Documentation build
-----------------------

You can build local documentation from source files.

.. code-block:: bash

   cd docs
   pip install -r requirements.txt

   make html   # For windows make.bat html

Those commands will create ``Index.html`` file in ``docs/_build`` folder. This file is index page of the documentation.


Python 3.7 installation
-------------------------

Installation of python 3.7 could be tricky. You can find tutorials on the internet, but there is some notes for
installation.

Windows
*********

For the windows user I recommend to use Anaconda_ distribution. You will get whole Python installation with integration
to the system and also virtual environments support with few steps in GUI installation. Also if you are using
PyCharm, in the new version (2019) PyCharm support Anaconda distribution, so some features are implemented directly
to IDE.

.. warning::

   If you have some older Anaconda installation on your system, it is recommended to uninstall whole distribution
   and install new one with Python 3.7. If you only update the distribution, there could be some problems
   with PyQt dependencies.


.. _Anaconda: https://www.anaconda.com/distribution/


Linux - Ubuntu / Mint
************************

Python 3.7 is not added to apt yet. You need to install Python 3.7 from other original source. Don't worry,
it is so hard.

.. code-block:: bash

   cd /usr/src
   sudo wget https://www.python.org/ftp/python/3.7.2/Python-3.7.2.tgz  # Download Python

   sudo tar xzf Python-3.7.2.tgz # Extract python source

   cd Python-3.7.2
   sudo ./configure --enable-optimizations
   sudo make altinstall # Install python under python3.7 (don't replace old python version)

