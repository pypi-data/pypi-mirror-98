.. role:: bash(code)
   :language: bash

curvenote
#########

The Curvenote Python client library and Command Line Interface.
Access and interact with your projects via the Curvenote API.


Installation
************

.. code-block:: bash

    ~$ python -m pip install curvenote

Retrieve your `API_TOKEN` from  `curvenote support <mailto:support@curvenote.com>`_


CLI Usage
*********

Access Curvenote projects via the command line. Get help on commands by:

.. code-block:: bash

    ~$ python -m curvenote --help

.. code-block:: bash

    ~$ python -m curvenote COMMAND --help

Command Summary
===============

 - :code:`get-me` list my user information
    .. code-block:: bash

        ~$ python -m curvenote get-me API_TOKEN

 - :code:`get-my-projects` list all projects that the current user has access to
    .. code-block:: bash

        ~$ python -m curvenote get-my-projects API_TOKEN

 - :code:`push` upload local documents into a curvenote project. :code:`.md` (import and update existing) and :code:`.ipynb` (import new only) files supported
    .. code-block:: bash

        ~$ python -m curvenote push PATH PROJECT API_TOKEN

 - :code:`pull-as-latex` create a local latex project and download contents of a Curvenote article into it
     .. code-block:: bash

        ~$ python -m curvenote push TARGET PROJECT ARTICLE API_TOKEN --version=INTEGER

Python Client Usage
*******************

From Python - get curvenote blocks:

.. code-block:: python

    >>> import curvenote
    >>> session = curvenote.Session(token=API_TOKEN)
    >>> session.me()
    >>> session.my_projects()
    >>> session.get_block_latest(PROJECT_ID, BLOCK_ID)
    >>> ...

From Python - push a local folder to a curvenote project:

.. code-block:: python

    >>> import curvenote
    >>> session = curvenote.Session(token=AUTHORIZATION_TOKEN)
    >>> proj = session.get_project("My Cool Project")
    >>> session.push_folder("./cool_stuff/", proj)
    >>> ...

There is also limited CLI functionality, though this still requires the
Python installation:

Documentation
*************

To build the documentation:
* Clone the repository
* Activate your virtual environment
* :code:`pip install -r requirements_dev.txt`
* :code:`make docs`

HTML doc pages will be written to ``./build/html/``

Development
***********

To use this library (in development):

* Clone the repository
* Activate your virtual environment
* :code:`pip install -r requirements.txt`
* Retrieve your `API_TOKEN` from  `curvenote support <mailto:support@curvenote.com>`_
