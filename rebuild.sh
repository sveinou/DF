#!/bin/bash
pip uninstall DynamicNetworkFirewall
rm MANIFEST
rm dist/*
python setup.py sdist
pip install dist/DynamicNetworkFirewall-0.3.dev1.tar.gz
