from django.test import TestCase

from brabbl.utils import math


class MathTest(TestCase):
    def test_iterative_mean(self):
        numbers = list(range(1, 20))
        mean = sum(numbers) / len(numbers)

        iterative_mean = 0
        for idx, num in enumerate(numbers):
            iterative_mean = math.iterative_mean(iterative_mean, idx, num)

        self.assertAlmostEqual(iterative_mean, mean)
