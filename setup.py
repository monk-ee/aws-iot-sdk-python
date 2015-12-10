#! /usr/bin/env python

from setuptools import setup

exec(open("./aws_iot_sdk/_version.py").read())

setup(name="aws-iot-sdk",
      version=__version__,
      author="monkeemagic",
      author_email="lyndon.swan@cloudtrek.com.au",
      packages=['aws_iot_sdk'],
      install_requires = [
          'user-agents',
      ],
      license='GPLv3+',
      description="Provide a sensible interface to Paho MQTT and AWS IoT",
      test_suite='aws_iot_sdk.tests',
      classifiers=[
          'Development Status :: 5 - Production/Stable',
          'License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)',
          'Environment :: Console',
          'Intended Audience :: Developers',
          'Operating System :: OS Independent',
          'Programming Language :: Python',
          'Programming Language :: Python :: 2',
          'Programming Language :: Python :: 2.6',
          'Programming Language :: Python :: 2.7',
          'Programming Language :: Python :: 3',
          'Programming Language :: Python :: 3.3',
          'Programming Language :: Python :: 3.4',
      ]
      )