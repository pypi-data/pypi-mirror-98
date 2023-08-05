#!/usr/bin/python3
# -*- coding: utf-8 -*-

# This file is part of damedb.

#  Copyright (C) 2021 David Arroyo Menéndez

#  Author: David Arroyo Menéndez <davidam@gmail.com>
#  Maintainer: David Arroyo Menéndez <davidam@gmail.com>
#  This file is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 3, or (at your option)
#  any later version.
#
#  This file is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with damedb; see the file LICENSE.  If not, write to
#  the Free Software Foundation, Inc., 51 Franklin Street, Fifth Floor,
#  Boston, MA 02110-1301 USA,


import unittest
import redis
import datetime

class TddInPythonExample(unittest.TestCase):

    def test_basics(self):
        r = redis.Redis()
        r.mset({"Croatia": "Zagreb", "Bahamas": "Nassau"})        
        self.assertEqual("b'Nassau'", str(r.get("Bahamas")))

