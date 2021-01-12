#! /usr/bin/env python
"""Installation script."""

from setuptools import setup

setup(
    name='mcwb',
    use_scm_version=True,
    setup_requires=['setuptools_scm'],
    author='Richard Neumann',
    author_email='mail@richard-neumann.de',
    python_requires='>=3.8',
    packages=['mcwb'],
    install_requires=['mcipc'],
    url='https://github.com/conqp/mcwb',
    license='GPLv3',
    description='A Minecraft world builder library.',
    long_description=open('README.md').read(),
    long_description_content_type="text/markdown",
    keywords='minecraft world builder python rcon'
)
