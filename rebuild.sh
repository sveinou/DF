#!/bin/bash
pip uninstall DynamicNetworkFirewall
rm MANIFEST
rm dist/*
python setup.py sdist
pip install dist/DynamicNetworkFirewall-0.4.alpha.tar.gz
service apache2 restart
