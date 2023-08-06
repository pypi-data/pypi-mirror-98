from setuptools import setup
from os import path

# read the contents of readme.md
with open('readme.md', encoding='utf-8') as f:
    long_description = f.read()


description = "A simplified socket setup suitable for many/most lightweight client server programs. " + \
              "The Python standard library TCP/IP socket module has a relatively steep learning curve. " + \
              "This module is intended to help get most projects up and running quickly by wrapping " + \
              "the standard library socket module in an easy to use interface."

setup(
    name='socket_for_humans',
    version='0.0.2',
    packages=['socket_for_humans'],
    url='https://gitlab.com/koyaanisqatsi.naqoyqatsi1/socket_for_humans',
    license='MIT',
    author='koyaanisqatsi.naqoyqatsi@pm.me',
    author_email='koyaanisqatsi.naqoyqatsi@pm.me',
    description=description,
    long_description=long_description,
    long_description_content_type='text/markdown',
    keywords='networking, TCP/IP, simplified, client, server, socket',
    classifiers=[
        # How mature is this project? Common values are
        #   3 - Alpha
        #   4 - Beta
        #   5 - Production/Stable
        'Development Status :: 3 - Alpha',
        # Indicate who your project is intended for
        'Intended Audience :: Developers',
        'Topic :: System :: Networking',

        # Pick your license as you wish (should match "license" above)
        'License :: OSI Approved :: MIT License',

        # Specify the Python versions you support here. In particular, ensure
        # that you indicate whether you support Python 2, Python 3 or both.
        'Programming Language :: Python :: 3'
    ],
)
