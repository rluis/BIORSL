Installation
============

To **install BIORSL modules**:

    - using *pip* (preferentially):

    .. code-block:: bash

        git clone https://github.com/rluis/BIORSL.git
        cd BIORSL
        pip3 install .

    - using *python setup.py*:

    .. code-block:: bash

        git clone https://github.com/rluis/BIORSL.git
        cd BIORSL
        python3 setup.py install


To **uninstall BIORSL modules**:

    - using *pip* (preferentially):

    .. code-block:: bash

        pip3 uninstall BIORSL

    - using *python setup.py*:

    .. code-block:: bash

        git clone https://github.com/rluis/BIORSL.git
        cd BIORSL
        python3 setup.py develop --uninstall


To **print current version**, after installation:

    - using *pip*:

    .. code-block:: bash

        pip3 freeze | grep BIORSL
