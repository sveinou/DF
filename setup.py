# coding=utf-8
from distutils.core import setup

setup(
	name='DynamicNetworkFirewall',
	version='0.4.alpha',
	author='espengj && sveinou',
	author_email='@stud.hist.no',
	packages=['DNF','DNF.firewall','DNF.auth','DNF.stats','DNF.database',
              'dDNF','dDNF.statistics', 'dDNF.login'],
    #package_dir = {'dDNF':'/usr/local/share/dnf/'},
    package_data = {'dDNF':['templates/*.html', 'templates/media/*','locale/no/LC_MESSAGES/*']},
	scripts=['bin/dynfw'], # setup_firewall should be a command from dynfw
	url='http://github.com/sveinou/DF',
	license='LICENSE.txt',
	description='Combined firewall and captive portal, with dynamic bandwidth allocation',
	long_description=open('README.txt').read(),
	data_files=[('/etc/dnf/',['cfg/dnf.conf','cfg/apache.wsgi']),
				('/etc/init.d/',['cfg/dynfd.sh']),
				('/etc/sudoers.d/', ['cfg/dynfw.sudo']),
				('/etc/dhcp/',['cfg/dhcpd.dnf.conf']),
				('/etc/apache2/conf.d/',['cfg/djangoDNF.conf']),
                ],
	install_requires=[
		"pam >= 0.1.3",
		"MySQL-python >= 1.2.2",
		"Django >= 1.2.3",
	],
)
