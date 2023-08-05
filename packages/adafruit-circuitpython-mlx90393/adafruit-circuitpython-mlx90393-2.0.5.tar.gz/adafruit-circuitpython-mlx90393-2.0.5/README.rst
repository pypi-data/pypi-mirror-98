Introduction
============

.. image:: https://readthedocs.org/projects/adafruit-circuitpython-mlx90393/badge/?version=latest
    :target: https://circuitpython.readthedocs.io/projects/mlx90393/en/latest/
    :alt: Documentation Status

.. image:: https://img.shields.io/discord/327254708534116352.svg
    :target: https://adafru.it/discord
    :alt: Discord

.. image:: https://github.com/adafruit/Adafruit_CircuitPython_MLX90393/workflows/Build%20CI/badge.svg
    :target: https://github.com/adafruit/Adafruit_CircuitPython_MLX90393/actions/
    :alt: Build Status

Adafruit CircuitPython driver for the MLX90393 3-axis magnetometer.

Dependencies
=============
This driver depends on:

* `Adafruit CircuitPython <https://github.com/adafruit/circuitpython>`_
* `Bus Device <https://github.com/adafruit/Adafruit_CircuitPython_BusDevice>`_

Please ensure all dependencies are available on the CircuitPython filesystem.
This is easily achieved by downloading
`the Adafruit library and driver bundle <https://github.com/adafruit/Adafruit_CircuitPython_Bundle>`_.

Installing from PyPI
--------------------

On supported GNU/Linux systems like the Raspberry Pi, you can install the driver locally `from
PyPI <https://pypi.org/project/adafruit-circuitpython-mlx90939/>`_. To install for current user:

.. code-block:: shell

    pip3 install adafruit-circuitpython-mlx90939

To install system-wide (this may be required in some cases):

.. code-block:: shell

    sudo pip3 install adafruit-circuitpython-mlx90939

To install in a virtual environment in your current project:

.. code-block:: shell

    mkdir project-name && cd project-name
    python3 -m venv .env
    source .env/bin/activate
    pip3 install adafruit-circuitpython-mlx90939

Usage Example
=============

.. code-block:: python3

    import time
    import busio
    import board

    import adafruit_mlx90393

    I2C_BUS = busio.I2C(board.SCL, board.SDA)
    SENSOR = adafruit_mlx90393.MLX90393(I2C_BUS, gain=adafruit_mlx90393.GAIN_1X)

    while True:
        MX, MY, MZ = SENSOR.magnetic
        print("[{}]".format(time.monotonic()))
        print("X: {} uT".format(MX))
        print("Y: {} uT".format(MY))
        print("Z: {} uT".format(MZ))
        # Display the status field if an error occured, etc.
        if SENSOR.last_status > adafruit_mlx90393.STATUS_OK:
            SENSOR.display_status()
        time.sleep(1.0)

Contributing
============

Contributions are welcome! Please read our `Code of Conduct
<https://github.com/adafruit/Adafruit_CircuitPython_MLX90393/blob/master/CODE_OF_CONDUCT.md>`_
before contributing to help this project stay welcoming.

Documentation
=============

For information on building library documentation, please check out `this guide <https://learn.adafruit.com/creating-and-sharing-a-circuitpython-library/sharing-our-docs-on-readthedocs#sphinx-5-1>`_.
