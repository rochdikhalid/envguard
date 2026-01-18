import unittest
from envguard.diff import diff_envs

class TestDiff(unittest.TestCase):

    def test_diff_added_removed_changed(self):
        env_a = {"A": "1", "B": "2"}
        env_b = {"B": "3", "C": "4"}

        result = diff_envs(env_a, env_b)
        self.assertIn("+ C", result)
        self.assertIn("- A", result)
        self.assertIn("~ B", result)

    def test_diff_identical(self):
        env_a = {"X": "1"}
        env_b = {"X": "1"}
        result = diff_envs(env_a, env_b)
        self.assertIn("✅ Environments are identical!", result)
