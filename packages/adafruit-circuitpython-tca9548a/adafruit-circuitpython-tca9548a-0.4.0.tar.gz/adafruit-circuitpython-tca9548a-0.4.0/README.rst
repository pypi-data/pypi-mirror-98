Introduction
============

.. image:: https://readthedocs.org/projects/adafruit-circuitpython-tca9548a/badge/?version=latest
    :target: https://circuitpython.readthedocs.io/projects/tca9548a/en/latest/
    :alt: Documentation Status

.. image:: https://img.shields.io/discord/327254708534116352.svg
    :target: https://adafru.it/discord
    :alt: Discord

.. image:: https://github.com/adafruit/Adafruit_CircuitPython_TCA9548A/workflows/Build%20CI/badge.svg
    :target: https://github.com/adafruit/Adafruit_CircuitPython_TCA9548A/actions/
    :alt: Build Status

CircuitPython driver for the TCA9548A I2C Multiplexer.

Dependencies
=============
This driver depends on:

* `Adafruit CircuitPython <https://github.com/adafruit/circuitpython>`_
* `Bus Device <https://github.com/adafruit/Adafruit_CircuitPython_BusDevice>`_

Please ensure all dependencies are available on the CircuitPython filesystem.
This is easily achieved by downloading
`the Adafruit library and driver bundle <https://github.com/adafruit/Adafruit_CircuitPython_Bundle>`_.

Installing from PyPI
====================

On supported GNU/Linux systems like the Raspberry Pi, you can install the driver locally `from
PyPI <https://pypi.org/project/adafruit-circuitpython-tca9548a/>`_. To install for current user:

.. code-block:: shell

    pip3 install adafruit-circuitpython-tca9548a

To install system-wide (this may be required in some cases):

.. code-block:: shell

    sudo pip3 install adafruit-circuitpython-tca9548a

To install in a virtual environment in your current project:

.. code-block:: shell

    mkdir project-name && cd project-name
    python3 -m venv .env
    source .env/bin/activate
    pip3 install adafruit-circuitpython-tca9548a

Usage Example
=============

.. code-block :: python

    # This example shows using two TSL2491 light sensors attached to TCA9548A channels 0 and 1.
    # Use with other I2C sensors would be similar.
    import time
    import board
    import busio
    import adafruit_tsl2591
    import adafruit_tca9548a

    # Create I2C bus as normal
    i2c = busio.I2C(board.SCL, board.SDA)

    # Create the TCA9548A object and give it the I2C bus
    tca = adafruit_tca9548a.TCA9548A(i2c)

    # For each sensor, create it using the TCA9548A channel instead of the I2C object
    tsl1 = adafruit_tsl2591.TSL2591(tca[0])
    tsl2 = adafruit_tsl2591.TSL2591(tca[1])

    # Loop and profit!
    while True:
        print(tsl1.lux, tsl2.lux)
        time.sleep(0.1)


Contributing
============

Contributions are welcome! Please read our `Code of Conduct
<https://github.com/adafruit/Adafruit_CircuitPython_TCA9548A/blob/master/CODE_OF_CONDUCT.md>`_
before contributing to help this project stay welcoming.

Documentation
=============

For information on building library documentation, please check out `this guide <https://learn.adafruit.com/creating-and-sharing-a-circuitpython-library/sharing-our-docs-on-readthedocs#sphinx-5-1>`_.
