icepyx
======

**Python tools for obtaining and working with ICESat-2 data**

|Documentation Status|  |GitHub license|  |Travis CI Status| |Code Coverage|

.. |Documentation Status| image:: https://readthedocs.org/projects/icepyx/badge/?version=latest
   :target: http://icepyx.readthedocs.io/?badge=latest

.. |GitHub license| image:: https://img.shields.io/badge/License-BSD%203--Clause-blue.svg
   :target: https://opensource.org/licenses/BSD-3-Clause

.. |Travis CI Status| image:: https://travis-ci.org/icesat2py/icepyx.svg?branch=master
    :target: https://travis-ci.org/icesat2py/icepyx

.. |Code Coverage| image:: https://codecov.io/gh/icesat2py/icepyx/branch/development/graph/badge.svg 
    :target: https://codecov.io/gh/icesat2py/icepyx

Origin and Purpose
------------------
icepyx is both a software library and a community composed of ICESat-2 data users, developers, and the scientific community. We are working together to develop a shared library of resources - including existing resources, new code, tutorials, and use-cases/examples - that simplify the process of querying, obtaining, analyzing, and manipulating ICESat-2 datasets to enable scientific discovery.

icepyx aims to provide a clearinghouse for code, functionality to improve interoperability, documentation, examples, and educational resources that tackle disciplinary research questions while minimizing the amount of repeated effort across groups utilizing similar datasets. icepyx also hopes to foster collaboration, open-science, and reproducible workflows by integrating and sharing resources.

Many of these tools began as Jupyter Notebooks developed for and during the cryosphere themed ICESat-2 Hackweek
at the University of Washington in June 2019 or as scripts written and used by the ICESat-2 Science Team members.
This project combines and generalizes these scripts into a unified framework, making them accessible for everyone.


.. _`zipped file`: https://github.com/icesat2py/icepyx/archive/master.zip
.. _`Fiona`: https://pypi.org/project/Fiona/

Installation
------------
The simplest way to install icepyx is using pip.

.. code-block::

  pip install icepyx


Windows users will need to first install `Fiona`_, please look at the instructions there. Windows users may consider installing Fiona using pipwin

.. code-block::

  pip install pipwin
  pipwin install Fiona 


Currently, updated packages are not automatically generated with each build. This means it is possible that pip will not install the latest release of icepyx. In this case, icepyx is also available for use via the GitHub repository. The contents of the repository can be download as a `zipped file`_ or cloned.

To use icepyx this way, fork this repo to your own account, then git clone the repo onto your system. 
To clone the repository:

.. code-block::

  git clone https://github.com/icesat2py/icepyx.git


Provided the location of the repo is part of your $PYTHONPATH, you should simply be able to add import icepyx to your Python document.
Alternatively, in a command line or terminal, navigate to the folder in your cloned repository containing setup.py and run

.. code-block::

  pip install -e .


Future developments of icepyx may include conda as another simplified installation option.


Examples (Jupyter Notebooks)
----------------------------

Listed below are example jupyter-notebooks

`ICESat-2_DAAC_DataAccess_Example <https://github.com/icesat2py/icepyx/blob/master/examples/ICESat-2_DAAC_DataAccess_Example.ipynb>`_

`ICESat-2_DAAC_DataAccess2_Subsetting <https://github.com/icesat2py/icepyx/blob/master/examples/ICESat-2_DAAC_DataAccess2_Subsetting.ipynb>`_

`ICESat-2_DEM_comparison_Colombia_working <https://github.com/icesat2py/icepyx/blob/master/examples/ICESat-2_DEM_comparison_Colombia_working.ipynb>`_


Citing icepyx
-------------
.. _`CITATION.rst`: ./CITATION.rst

This community and software is developed with the goal of supporting science applications. Thus, our contributors (including those who have developed the packages used within icepyx) and maintainers justify their efforts and demonstrate the impact of their work through citations. Please see  `CITATION.rst`_ for additional citation information.

Contact
-------
Working with ICESat-2 data and have ideas you want to share?
Have a great suggestion or recommendation of something you'd like to see
implemented and want to find out if others would like that tool too?
Come join the conversation at: https://discourse.pangeo.io/.
Search for "icesat-2" under the "science" topic to find us.

.. _`icepyx`: https://github.com/icesat2py/icepyx
.. _`contribution guidelines`: ./doc/source/contributing/contribution_guidelines.rst

Contribute
----------
We welcome and invite contributions to icepyx_ from anyone at any career stage and with any amount of coding experience!
Check out our `contribution guidelines`_ to see how you can contribute.

Please note that this project is released with a Contributor Code of Conduct. By participating in this project you agree to abide by its terms. |Contributor Covenant|

.. |Contributor Covenant| image:: https://img.shields.io/badge/Contributor%20Covenant-v2.0%20adopted-ff69b4.svg
   :target: code_of_conduct.md
