import os

from setuptools import setup

readme = open(os.path.join(os.path.dirname(__file__), 'README.md'), 'r').read()

setup(
    name='virtualenv-tools-enhanced',
    author='Fireteam Ltd.; Yelp, Inc.; Damien "psolyca" Gaignon',
    author_email='damien.gaignon@gmail.com',
    version='1.0.0',
    url='https://github.com/psolyca/virtualenv-tools',
    py_modules=['virtualenv_tools'],
    description='A set of tools to relocate virtualenv (and main installation on Windows)',
    long_description=readme,
    long_description_content_type='text/markdown',
    entry_points={
        'console_scripts': [
            'virtualenv-tools = virtualenv_tools:main'
        ]
    },
    zip_safe=False,
    classifiers=[
        'License :: OSI Approved :: BSD License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
    ]
)
