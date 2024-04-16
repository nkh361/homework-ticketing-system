import unittest

test_suite = unittest.defaultTestLoader.discover('.', pattern='*_test.py')
unittest.TextTestRunner().run(test_suite)
