
from setuptools import setup

import cine as app

setup(
    name='cine',
    packages=['cine', 'tests'],
    version=app.__version__,
    author=app.__author__,
    author_email='python@lost.co.nz',
    url='http://lost.co.nz/',
    license='LICENSE.txt',


    description='Movie collection management utilities',
    long_description=open('README.txt').read(),
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Console',
        'License :: OSI Approved :: GNU General Public License (GPL)',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3.7'
        'Topic :: Utilities',
    ],
    python_requires='>=3.7',
)
