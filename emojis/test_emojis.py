import unittest
import emojis
import random

class TestEmojis(unittest.TestCase):
    def test_emojis(self):
        self.assertEqual(emojis.buildkite, ":buildkite:")
        self.assertEqual(emojis.bazel, ":bazel:")
        self.assertEqual(emojis.python, ":python:")

if __name__ == "__main__":
    unittest.main()