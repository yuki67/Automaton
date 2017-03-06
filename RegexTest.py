import unittest
from Regex import regex_to_eNFA


class RegexTest(unittest.TestCase):

    def runTest(self):
        alphabet = "ab"
        cases = [["a", [["a", True], ["b", False], ["aa", False], ["ab", False]]]]
        for regex, tests in cases:
            enfa = regex_to_eNFA(regex, alphabet)
            for test, expected in tests:
                self.assertEqual(enfa.run(test), expected)


if __name__ == "__main__":
    suite = unittest.TestSuite()
    suite.addTest(RegexTest())
    unittest.TextTestRunner().run(suite)
