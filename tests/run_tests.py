#!/usr/bin/env python3
import unittest
import os

def set_environment_variable(variable_name, value):
    os.environ[variable_name] = value

set_environment_variable("APP_SECRET_KEY", "test")
set_environment_variable("DBUSER", "root")

test_suite = unittest.defaultTestLoader.discover('.', pattern='*_test.py')
unittest.TextTestRunner().run(test_suite)
