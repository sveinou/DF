=========================
Dynamic Network Firewall
=========================

Dynamic Network Firewall is a combinde captureportal and firewall which dynamicly allocates bandwidth to it's logged inn users.

You can issue commands to the dnf with the dynfw-command.

1. Prerequisites
================

The following (debian) linux-pacakages must be installed:
* iptables
* python 2.6
* mysql-server (??)
* isc-dhcp-server
* apache2 with mod_wsgi

The following python (PyPi)-packages are needed:
* PAM
* mySQLdb
* django

2. Installation
=====================
* [sudo] apt-get install python python-pip python-django mysql-server iptables isc-dhcp-server apache2 libapache2-mod-wsgi
* [sudo] pip install DynamicNetworkFirewall-v0.3.dev1.tar.gz

3. Setup
======================
Nothing yet... or: you probably have to run install.sh to setup your firewall...

4. Usage
======================
dynfw &lg;cmd&gt; &lt;arguments&gt;

