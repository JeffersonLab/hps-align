hps_align.plot package
======================

.. automodule:: hps_align.plot
   :members:
   :undoc-members:
   :show-inheritance:
   :private-members:

Plotters
--------
The `hps_align.plot` submodule is broken up
into veraious "plotters" so that users can choose
which plots to generate from the input files.

.. automodule:: hps_align.plot.vertex
   :members:
   :undoc-members:
   :show-inheritance:
   :private-members:

.. automodule:: hps_align.plot.derivatives
   :members:
   :undoc-members:
   :show-inheritance:
   :private-members:

.. automodule:: hps_align.plot.kinks
   :members:
   :undoc-members:
   :show-inheritance:
   :private-members:

.. automodule:: hps_align.plot.residual
   :members:
   :undoc-members:
   :show-inheritance:
   :private-members:

.. automodule:: hps_align.plot.tracks
   :members:
   :undoc-members:
   :show-inheritance:
   :private-members:

.. automodule:: hps_align.plot.tanL
   :members:
   :undoc-members:
   :show-inheritance:
   :private-members:

Advanced Usage
--------------
The main way we achieve this auto-registration of the
different plotters is by using a "decorator". This decorator
is a class member of the object that is passed to each plotting
function and is used to uniformly interact with the input
files.

.. automodule:: hps_align.plot._plotter
   :members:
   :undoc-members:
   :show-inheritance:
   :private-members:
