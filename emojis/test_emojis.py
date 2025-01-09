import unittest
import emojis

class TestEmojis(unittest.TestCase):
    def test_emojis(self):
        self.assertEqual(emojis.buildkite, ":buildkite:")

if __name__ == '__main__':
    unittest.main()