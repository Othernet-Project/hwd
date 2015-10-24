hwd
===

hwd wraps around `pyudev <https://pypi.python.org/pypi/pyudev>`_'s ``Device``
objects to provide functionality specific to different types of hardware.
Currently, hwd provides a base wrapper class that provides common information
such as bus, vendor, and model, and classes for wrapping storage and network
devices.

hwd is being developed at `Outernet <https://outernet.is/>`_ specifically for
integration of hardware management functionality into `Librarian
<https://github.com/Outernet-Project/librarian/>`_ that runs on Outernet
receives. As such, there are no plans for adding support for devices that are
common on personal computers.

API documentation
-----------------

.. toctree::
   :maxdepth: 2
    
   wrapper
   network
   storage
   udev

