Set Up hps-java
===============

This document explains how to setup an installation of hps-java for you to run accumulation with and for you to develop on.

General Broken Lines
--------------------
We use the `C++ General Broken Lines <https://gitlab.desy.de/claus.kleinwort/general-broken-lines>`_ library for speed.
V03-01-00 of this library introduced the necessary ``extern "C"`` functions to access it via Java Native Access (JNA) from java,
so that is the minimum version we support.::

    git clone --branch V03-01-00 https://gitlab.desy.de/claus.kleinwort/general-broken-lines.git
    cmake -B general-broken-lines/cpp/build -S general-broken-lines/cpp -DCMAKE_INSTALL_PREFIX=<install location>
    cmake --build general-broken-lines/cpp/build --target install

If you don't already have `Eigen <https://eigen.tuxfamily.org/index.php?title=Main_Page>`_ installed, you will need it to build.::

    wget -q -O - https://gitlab.com/libeigen/eigen/-/archive/3.4.0/eigen-3.4.0.tar.gz | tar -xz
    cmake -B eigen-3.4.0/build -S eigen-3.4.0 -DCMAKE_INSTALL_PREFIX=<install location>
    cmake --build eigen-3.4.0/build --target install

and then pass the Eigen install location to GBL with ``-DEIGEN3_DIR=<install location>``.

Specialized Configurations
^^^^^^^^^^^^^^^^^^^^^^^^^^
The C++ GBL library has a few compile-time configurations that may be helpful if memory issues are encountered when using it.

JNA_MEMORY_MONITOR
  set this to ``ON`` if you want a report of how many C++ GBL objects are left in memory when the program completes. 
  They should all be zero, but it is broken down by type so it may help point you in the directory of which ``delete`` call is missing.

JNA_DEBUG 
  set this to ``ON`` to enable debug printouts from the C++ GBL ``extern "C"`` wrapper functions. 
  These printouts are extremely verbose and should only be used in short runs.

hps-java
--------
Commit must be based on `hps-java:4f599a33 <https://github.com/JeffersonLab/hps-java/tree/4f599a3391cecf01d4e47b7b3cf02f8e3b90b599>`_
which, essentially, updates the JNA interaction with the GBL library to include the necessary functions and introduces the 
necessary ``delete`` calls to make sure everyting created on the GBL side is cleaned up.

In order for JNA to be able to read the GBL C++ library, it needs to be able to find it. If GBL is not installed to a system
location (like e.g. ``/usr/local`` which is the CMake default), then one must tell JNA what path to look in for requested
libraries. This is accomplished with a special command line parameter for ``java``::

    -Djna.library.path=/full/path/to/directory/with/GBL/lib

The full path provided must be the full path to the directory that contains the ``libGBL.so`` file.
If you want to use your custom built version, it will be the ``<install location>`` you provided with the ``lib`` subdirectory.

In the ``hps-mc`` framework you can provide this option in your config file.

Containerized Environment
-------------------------
Both GBL and Eigen are already installed to system paths in recent versions of 
`tomeichlersmith/hps-env <https://github.com/tomeichlersmith/hps-env>`_.
so this option is unnecessary unless you wish to use a specialized build (or are developing the C++-side functions).
