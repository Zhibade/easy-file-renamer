"""
Test runner
"""

import unittest

TEST_PATH = "test/"

if __name__ == "__main__":
    test_suite = unittest.defaultTestLoader.discover(TEST_PATH)
    test_runner = unittest.TextTestRunner(verbosity=2)
    test_runner.run(test_suite)
