Installation guide
========================

Requirements
*********************

**Python**

Python 3.7.* is required because of some features and better performance


**External packages requirement**


* ``PyQt5`` - Graphical interface
* ``click`` - Console interface
* ``antlr4-python3-runtime`` - Knowledge base language parser
* ``multi_key_dict`` - Package for multi key dictionary support


Installation
************************

It is recommended to use virtual environment because of possible problem with PyQt version conflicts.

.. code-block:: bash

    git clone https://gitlab.fit.cvut.cz/bi-zns_pracovni/zna_framework_python
    cd zns_framework_python
    pip install -r requirements.txt


Documentation build
*************************

You can build local documentation from source files.

.. code-block:: bash

   cd docs
   pip install -r requirements.txt

   make html   # For windows make.bat html

Those commands will create ``Index.html`` file in ``docs/_build`` folder. This file is index of the documentation.