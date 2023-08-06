from setuptools import setup
from os import path

# read the contents of readme.md
with open('readme.md', encoding='utf-8') as f:
    long_description = f.read()

# extract the first paragraph of readme for the short description
description = long_description.split('\n')
for d in reversed(description):
    d0 = d.strip()
    if d0.startswith('#'):
        description.remove(d)
    elif not d0:
        description.remove(d)
description = description[0]

setup(
    name='socket_for_humans',
    version='0.0.3',
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
