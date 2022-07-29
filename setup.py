#!/usr/bin/env python

from setuptools import setup, find_packages

setup(name='SocialApp',
      version='1.0',
      description='Sommercamp 2022 Social Media App',
      author='Isabella Graßl',
      author_email='isabella.grassl@uni-passau.de ',
      url='https://artemis.se2.fim.uni-passau.de/courses/10/exercises/60',
      packages=find_packages(),
      scripts=['manage.py']
      )
