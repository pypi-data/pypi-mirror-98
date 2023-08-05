
import os
import sys

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

# Don't import analytics-python module here, since deps may not be installed
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'amplitude_tracker'))
from version import VERSION

long_description = '''
Amplitude Tracker
=================

Amplitude Tracker library lets you record analytics data from your
Python code to `Amplitude`_

Getting Started
---------------

Install ``amplitude-tracker`` using pip:

::

   pip install amplitude-tracker

Inside your app, you’ll want to *set your* ``write_key`` before making
any analytics calls:

.. code:: python

   import amplitude_tracker as amplitude

   amplitude.write_key = 'xxxxxxxxxxxxxxx'

*Note:* If you need to send data to multiple Segment sources, you can
initialize a new Client for each write_key.

Development Settings
--------------------

The default initialization settings are production-ready and queue
messages to be processed by a background thread.

In development you might want to enable some settings to make it easier
to spot problems. Enabling amplitude.debug will log debugging info to
the Python logger. You can also add an on_error handler to specifically
print out the response you’re seeing from the Amplitude’s API.

.. code:: python

   def on_error(error, items):
       print("An error occurred:", error)


   analytics.debug = True
   analytics.on_error = on_error

Track
-----

``track`` lets you record the actions your users perform. Every action
triggers what we call an “event”, which can also have associated
properties.

.. code:: python

   import amplitude_tracker as amplitude
   amplitude.write_key = 'xxxxxxxxxxxxxxx'

   amplitude.track(
       user_id="xxx",
       event_type="xxx",
       user_properties={"trait": "xxx"},
       event_properties={"attribute": "xxx"})

Batching
--------

This library is built to support high performance environments. That
means it is safe to use amplitude-tracker on a web server that’s serving
hundreds of requests per second.

Every call ``track`` method *does not* result in an HTTP request, but is
queued in memory instead. Messages are flushed in batch in the
background, which allows for much faster operation.

By default, this library will flush:

-  every ``100`` messages (control with ``upload_size``)
-  if ``0.5`` seconds has passed since the last flush (control with
   ``upload_interval``)

There is a maximum of ``500KB`` per batch request and ``32KB`` per call.

.. _Amplitude: https://amplitude.com
'''

install_requires = [
    "requests>=2.7,<3.0",
    "six>=1.5",
    "monotonic>=1.5",
    "backoff==1.10.0",
    "python-dateutil>2.1"
]

tests_require = [
    "mock==2.0.0",
    "pylint==1.9.3",
    "flake8==3.7.9",
    "coverage==4.5.4"
]

setup(
    name='amplitude-tracker',
    version=VERSION,
    url='https://github.com/RandomCoffee/amplitude',
    author='RandomCoffee',
    author_email='tech@random-coffee.com',
    maintainer='RandomCoffee',
    maintainer_email='tech@random-coffee.com',
    test_suite='amplitude_tracker.test.all',
    packages=['amplitude_tracker', 'amplitude_tracker.test'],
    license='MIT License',
    install_requires=install_requires,
    extras_require={
        'test': tests_require
    },
    description='The hassle-free way to integrate amplitude into any python application.',
    long_description=long_description,
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.2",
        "Programming Language :: Python :: 3.3",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
    ],
)
