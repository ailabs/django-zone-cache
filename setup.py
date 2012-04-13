import os
import sys

from setuptools import setup, find_packages, Command


install_requires = [
    'Django>=1.3',
]

readme = []
with open('README.rst', 'r') as fh:
    readme = fh.readlines()


setup(
    name='django-zone-cache',
    version='0.2',
    url='https://github.com/ailabs/django-zone-cache/',
    license='MIT',
    author='Michael van Tellingen',
    author_email='m.vantellingen@auto-interactive.nl',
    description='Small library to add support for cache zones to Django cache',
    long_description=''.join(readme),
    install_requires=install_requires,
    zip_safe=False,
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Software Development'
    ],
    test_suite='test.suite'
)
