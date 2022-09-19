import re
import unittest


class MyTestCase(unittest.TestCase):

    def setUp(self) -> None:
        pass

    def test_repl_h(self):

        print(re.match(r'#{1,6} (.*)', '# 123'))
        print(re.match(r'#{1,6} (.*)', '## 123'))
        print(re.match(r''))


if __name__ == '__main__':
    unittest.main()
