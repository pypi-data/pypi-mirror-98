# source: https://python-packaging.readthedocs.io/en/latest/minimal.html
from setuptools import setup, find_packages
name='encrypti0n'
setup(
	name=name,
	version='3.22.0',
	description='Easily encrypt & decrypt files with python / through the CLI.',
	url=f'http://github.com/vandenberghinc/{name}',
	author='Daan van den Bergh',
	author_email='vandenberghinc.contact@gmail.com',
	license='MIT',
	packages=find_packages(),
	zip_safe=False,
      include_package_data=True,
	install_requires=[
            'certifi',
            'chardet',
            'idna',
            'pycryptodome',
            'urllib3',
            'dev0s',
            'netw0rk',
            'syst3m',
        ])