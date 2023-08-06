__all__ = ["PyModuleTestCase"]
import os
import sys
import unittest
import gada


class PyModuleTestCase(unittest.TestCase):
    def test_sum(self):
        """This node has an implicit configured module."""
        gada.main(["gada", "testnodes.pymodule_sum", "1", "2", "3"])

    def test_sum2(self):
        """This node has an explicit configured module."""
        gada.main(["gada", "testnodes.pymodule_sum2", "1", "2", "3"])

    def test_noentrypoint(self):
        """This node has no configured entrypoint."""
        with self.assertRaises(Exception):
            gada.main(["gada", "testnodes.pymodule_noentrypoint"])

    def test_invalidmodule(self):
        """This node has an invalid configured module."""
        with self.assertRaises(Exception):
            gada.main(["gada", "testnodes.pymodule_invalidmodule"])

    def test_invalidentrypoint(self):
        """This node has an invalid configured entrypoint."""
        with self.assertRaises(Exception):
            gada.main(["gada", "testnodes.pymodule_invalidentrypoint"])


if __name__ == "__main__":
    unittest.main()
