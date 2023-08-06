__all__ = ["PythonTestCase"]
import os
import sys
import unittest
import gada


class PythonTestCase(unittest.TestCase):
    def test_sum(self):
        gada.main(["gada", "testnodes.python_sum", "1", "2", "3"])


if __name__ == "__main__":
    unittest.main()
