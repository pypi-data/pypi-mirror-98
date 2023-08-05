#!/usr/bin/env python3

# Note!
# ' are required, do not use any '.

# setup.
from setuptools import setup, find_packages
setup(
	name='w3bsite',
	version='4.27.0',
	description='Some description.',
	url='http://github.com/vandenberghinc/w3bsite',
	author='Daan van den Bergh',
	author_email='vandenberghinc.contact@gmail.com',
	license='MIT',
	packages=find_packages(),
	zip_safe=False,
	include_package_data=True,
	install_requires=[
            'wheel',
            'asgiref',
            'certifi',
            'chardet',
            'idna',
            'sqlparse',
            'urllib3',
            'gunicorn',
            'whitenoise',
            'psutil',
            'uwsgi',
            'xmltodict',
            'stripe',
            'syst3m',
            'dev0s',
            'netw0rk',
            'ssht00ls',
        ])