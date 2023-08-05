# -*- Mode:Python; indent-tabs-mode:nil; tab-width:4; encoding:utf8 -*-
#
# Copyright 2002 Ben Escoto <ben@emerose.org>
# Copyright 2007 Kenneth Loafman <kenneth@loafman.com>
#
# This file is part of duplicity.
#
# Duplicity is free software; you can redistribute it and/or modify it
# under the terms of the GNU General Public License as published by the
# Free Software Foundation; either version 2 of the License, or (at your
# option) any later version.
#
# Duplicity is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with duplicity; if not, write to the Free Software Foundation,
# Inc., 59 Temple Place, Suite 330, Boston, MA 02111-1307 USA

from __future__ import print_function
from future import standard_library
standard_library.install_aliases()

import unittest

from testing import _runtest_dir
from . import FunctionalTestCase


class CleanupTest(FunctionalTestCase):
    u"""
    Test cleanup using duplicity binary
    """
    def test_cleanup_after_partial(self):
        u"""
        Regression test for https://bugs.launchpad.net/bugs/409593
        where duplicity deletes all the signatures during a cleanup
        after a failed backup.
        """
        self.make_largefiles()
        good_files = self.backup(u"full", u"{0}/testfiles/largefiles".format(_runtest_dir))
        good_files |= self.backup(u"inc", u"{0}/testfiles/largefiles".format(_runtest_dir))
        good_files |= self.backup(u"inc", u"{0}/testfiles/largefiles".format(_runtest_dir))
        self.backup(u"full", u"{0}/testfiles/largefiles".format(_runtest_dir), fail=1)
        bad_files = self.get_backend_files()
        bad_files -= good_files
        self.assertNotEqual(bad_files, set())
        # the cleanup should go OK
        self.run_duplicity(options=[u"cleanup", self.backend_url, u"--force"])
        leftovers = self.get_backend_files()
        self.assertEqual(good_files, leftovers)
        self.backup(u"inc", u"{0}/testfiles/largefiles".format(_runtest_dir))
        self.verify(u"{0}/testfiles/largefiles".format(_runtest_dir))

    def test_remove_all_but_n(self):
        u"""
        Test that remove-all-but-n works in the simple case.
        """
        full1_files = self.backup(u"full", u"{0}/testfiles/empty_dir".format(_runtest_dir))
        full2_files = self.backup(u"full", u"{0}/testfiles/empty_dir".format(_runtest_dir))
        self.run_duplicity(options=[u"remove-all-but-n", u"1", self.backend_url, u"--force"])
        leftovers = self.get_backend_files()
        self.assertEqual(full2_files, leftovers)

    def test_remove_all_inc_of_but_n(self):
        u"""
        Test that remove-all-inc-of-but-n-full works in the simple case.
        """
        full1_files = self.backup(u"full", u"{0}/testfiles/empty_dir".format(_runtest_dir))
        inc1_files = self.backup(u"inc", u"{0}/testfiles/empty_dir".format(_runtest_dir))
        full2_files = self.backup(u"full", u"{0}/testfiles/empty_dir".format(_runtest_dir))
        self.run_duplicity(options=[u"remove-all-inc-of-but-n-full", u"1", self.backend_url, u"--force"])
        leftovers = self.get_backend_files()
        self.assertEqual(full1_files | full2_files, leftovers)

if __name__ == u"__main__":
    unittest.main()
