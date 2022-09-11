import siwen
import unittest


class MyTestCase(unittest.TestCase):

    def setUp(self) -> None:
        self.a = siwen.Base()

    def test_import(self):

        self.assertEqual(str(self.a), 'base')  # add assertion here


if __name__ == '__main__':
    unittest.main()
