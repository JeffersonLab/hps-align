Detector Dump
=============

Dumping the sensor position and orientation for easier analysis.

.. automodule:: hps_align.detdump
   :members:
   :undoc-members:
   :show-inheritance:
   :private-members:

Global
------
.. automodule:: hps_align.detdump._global
   :members:
   :private-members:

Local
-----
.. automodule:: hps_align.detdump._local
   :members:
   :private-members:

Data Writing
------------
The backend module for writing this parsed data
into a more easily-parsed format (either CSV or JSON).

.. automodule:: hps_align.detdump._write
   :members:
   :private-members:

Plotting
--------
We can also summarize the dumped detector parameters through
plots showing the sensor location/orientation in absolute terms
or relative to a certain reference detector.

.. automodule:: hps_align.detdump.plot
   :members:
   :private-members:


Calculating Angles
^^^^^^^^^^^^^^^^^^

.. automodule:: hps_align.detdump.plot._angles
   :members:
   :private-members:

Loading Dumps
^^^^^^^^^^^^^
Loading the dumps gives us an opportunity to apply transformations
to the coordinate vectors and positions so that the values we look
at in the plots are more interpretable by the user. For example,
This is where we choose how to calculate angles from the coordinate
vectors u, v, and w.

.. automodule:: hps_align.detdump.plot._load
   :members:
   :private-members:

Table of Figures
^^^^^^^^^^^^^^^^
We've isolated the matplotlib nonsense for putting together
several figures into a "table" of subplots so that it is easier
to maintain. This is where stylistic choices are made.

.. automodule:: hps_align.detdump.plot._table_fig
   :members:
   :private-members:
