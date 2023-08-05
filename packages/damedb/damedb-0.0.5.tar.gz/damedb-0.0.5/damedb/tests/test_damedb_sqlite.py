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
import sqlite3

class TddInPythonExample(unittest.TestCase):

    def test_basics(self):
        persons = [
            ("David", "Boss"),
            ("Calvin", "Klein")
        ]
        con = sqlite3.connect(":memory:")
        # Create the table
        con.execute("create table person(firstname, lastname)")
        # Fill the table
        con.executemany("insert into person(firstname, lastname) values (?, ?)", persons)
        # Print the table contents
        for row in con.execute("select firstname, lastname from person"):
            print(row)
        string = "I just deleted " +  str(con.execute("delete from person").rowcount) + " rows"
        self.assertEqual("I just deleted 2 rows", string)
