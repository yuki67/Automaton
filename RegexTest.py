import unittest
from Regex import regex_to_eNFA


class RegexTest(unittest.TestCase):

    def runTest(self):
        alphabet = {"a", "b"}
        cases = [["a",
                  [["a", True],
                   ["b", False],
                   ["aa", False],
                   ["ab", False]]],
                 ["aba",
                  [["aba", True],
                   ["aaa", False],
                   ["baa", False]]],
                 ["a*",
                  [["a", True],
                   ["aaaaaaaaa", True],
                   ["", True],
                   ["abba", False],
                   ["b", False]]],
                 ["ab*a",
                  [["aba", True],
                   ["abbbbba", True],
                   ["aa", True],
                   ["aabb", False],
                   ["aabaaabb", False]]]]
        for regex, tests in cases:
            enfa = regex_to_eNFA(regex, alphabet)
            for test, expected in tests:
                self.assertEqual(enfa.run(test), expected)


def run():
    suite = unittest.TestSuite()
    suite.addTest(RegexTest())
    unittest.TextTestRunner().run(suite)


if __name__ == "__main__":
    run()
