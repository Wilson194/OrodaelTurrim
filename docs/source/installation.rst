Installation guide
========================

Requirements
*********************

**Python**

Python 3.5+ is required, Python 3.7 is recommended ( 2x faster in soe cases )


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