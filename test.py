#!/usr/bin/python


from storage import Database


import sys
sql = "select User from clients where IP4='%s'" % sys.argv[1]
print Database().get_row(sql)[0]
