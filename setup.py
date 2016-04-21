"""
Python PayU Latam
-----------------

Simple SDK for the PayU Latam API
"""
from setuptools import setup


setup(
    name='Python PayU Latam',
    version='1.0',
    url='https://github.com/PolymathVentures/python-payu-latam',
    author='Victor Baumann',
    author_email='victor.baumann@vincuventas.com',
    description='Simple SDK for the PayU Latam API',
    long_description=__doc__,
    py_modules=['payu'],
    install_requires=[
        'requests'
    ],
    classifiers=[
      'Development Status :: 3 - Alpha',
      'Topic :: Utilities',
      'License :: OSI Approved :: BSD License',
    ]
)
