# -*- Mode:Python; indent-tabs-mode:nil; tab-width:4; encoding:utf8 -*-
#
# Copyright 2002 Ben Escoto <ben@emerose.org>
# Copyright 2007 Kenneth Loafman <kenneth@loafman.com>
# Copyright 2011 Canonical Ltd
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
from . import CmdError, FunctionalTestCase


class BadUploadTest(FunctionalTestCase):
    u"""
    Test missing volume upload using duplicity binary
    """
    def test_missing_file(self):
        u"""
        Test basic lost file
        """
        try:
            self.backup(u"full", u"{0}/testfiles/dir1".format(_runtest_dir), options=[u"--skip-volume=1"])
            self.fail()
        except CmdError as e:
            self.assertEqual(e.exit_status, 44, str(e))
        else:
            self.fail(u'Expected CmdError not thrown')

if __name__ == u"__main__":
    unittest.main()
