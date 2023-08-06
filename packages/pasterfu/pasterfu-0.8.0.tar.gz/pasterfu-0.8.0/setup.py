#! /usr/bin/env python3


from pasterfu import constants
import setuptools


with open('README.md', 'r') as fh:
    long_description = fh.read()


setuptools.setup(
    name='pasterfu',
    version=constants.__version__,
    author=constants.__author__,
    description='Open a link with a command read from a database.',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://gitlab.com/obtusescholar/pasterfu',
    entry_points={ 'console_scripts': ['pasterfu = pasterfu.cli:main'] },
    packages=setuptools.find_packages(
        include=['pasterfu', 'pasterfu.*'],
        exclude=['pasterfu/__pycache__']
    ),
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Console',
        'License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)',
        'Operating System :: OS Independent',
        'Intended Audience :: End Users/Desktop',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Topic :: Internet',
        'Topic :: Terminals',
        'Topic :: Utilities'
    ],
    license='GPLv3+',
    keywords='paste link url rss',
    python_requires='>=3.9',
    install_requires=['pyperclip']
)
