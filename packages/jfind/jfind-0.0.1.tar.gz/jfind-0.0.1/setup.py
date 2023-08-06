import os
from setuptools import setup, find_packages


def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()


setup(
    name='jfind',
    version='0.0.1',
    author='Erick Durán',
    author_email='me@erickduran.com',
    description=('A simple JSON search script.'),
    license='GPL-3',
    keywords='json search script',
    url='https://github.com/erickduran/jfind',
    packages=find_packages(),
    long_description=read('README.md'),
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Topic :: Utilities',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
    ],
    entry_points={
        'console_scripts': [
            'jfind=jfind.__main__:main'
        ]
    }
)
