# coding=utf-8
from distutils.core import setup

setup(
	name='DynamicNetworkFirewall',
	version='0.3.dev1',
	author='espengj && sveinou',
	author_email='@stud.hist.no',
	packages=['DNF','DNF.firewall','DNF.auth','DNF.stats','DNF.database'],
	scripts=['bin/dynfw'], # setup_firewall should be a command from dynfw
	url='http://github.com/sveinou/DF',
	license='LICENSE.txt',
	description='Combined firewall and captive portal, with dynamic bandwidth allocation',
	long_description=open('README.txt').read(),
	install_requires=[
		"pam >= 0.1.3",
		"MySQL-python >= 1.2.2",
	],
)
