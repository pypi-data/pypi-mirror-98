"""Test cases for detection engine module."""
import unittest

from openmt import detect
from openmt.unittest.util import DetectTest


class TestTrain(DetectTest):
    """Test cases for openmt detection training."""

    def test_train(self) -> None:
        """Testcase for training."""
        if self.det2cfg is not None and self.cfg is not None:
            detect.train_func(self.det2cfg, self.cfg)
        else:
            self.assertEqual(True, False, msg="failed to initialize configs!")


if __name__ == "__main__":
    unittest.main()
