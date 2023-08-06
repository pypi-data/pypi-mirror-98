# -*- coding: utf-8 -*-

from logilab.common.testlib import unittest_main, TestCase

from cubicweb_conference.utils import normalize_name


class UtilsTC(TestCase):
    def test_normalize_name(self):
        conference_name = u"une Conférence"
        self.assertEqual(normalize_name(conference_name), u"une_conference")


if __name__ == "__main__":
    unittest_main()
