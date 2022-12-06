import re

from django.test import TestCase
from django.conf import settings
from brabbl.utils import string


class StringTest(TestCase):
    def test_random_string(self):
        string_length = 32
        test_string = string.random_string(string_length)
        self.assertEqual(len(test_string), string_length)
        self.assertTrue(bool(re.match("^[A-Za-z0-9]*$", test_string)))

    def test_add_widget_hashtag(self):
        expected_url = "http://test.com/" + settings.WIDGET_HASHTAG
        self.assertEqual(string.add_widget_hashtag("http://test.com/"), expected_url)
        self.assertEqual(string.add_widget_hashtag("http://test.com/" + settings.WIDGET_HASHTAG), expected_url)
        self.assertEqual(string.add_widget_hashtag("http://test.com/#foo" + settings.WIDGET_HASHTAG), expected_url)
