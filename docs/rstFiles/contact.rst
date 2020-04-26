Sphinx Documentation
====================

Documentation is crucial in the maintenance of the code along time.
Because of that Sphinx documentation was implemented on this project.

Before each release is necessary to guarantee that the following points are ensured:

- Document the methods inside class and use the typing annotations.
- Increment methods to the SumUpTable with a brief description.
- Add one example of their function and usage in MODULENAME_RSTIndex.rst file. (*optional*)
- Update the **release version** in two files (setup.py and conf.py)
- Update **release data** in conf.py

To preview the actual state of the final html please run the commands below inside *docs* directory:

.. code-block:: bash

    make clean
    make html

Contact
=======

For any further suggestion / bug report / support, don't hesitate to contact by emailing ruisergioluis@gmail.com
or preferentially opening an issue in github |projectName| repository.

About
=====

| |projectName| : |projectVersion|
| was developed by Rui Sousa-Luis.

Latest release at: |projectReleaseData|

