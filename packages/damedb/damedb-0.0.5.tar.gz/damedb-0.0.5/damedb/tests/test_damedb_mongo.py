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
import datetime
from mongoengine import *

class Post(Document):
     title = StringField(required=True, max_length=200)
     content = StringField(required=True)
     author = StringField(required=True, max_length=50)
     published = DateTimeField(default=datetime.datetime.now)
 
class TddInPythonExample(unittest.TestCase):

    def test_basics(self):
        connect('mongoengine_test', host='localhost', port=27017)
        post_1 = Post(
            title='Sample Post',
            content='Some engaging content',
            author='Scott'
        )
        post_1.save()
        self.assertEqual(post_1.title, 'Sample Post')
        
        post_1.title = 'A Better Post Title'
        post_1.save()
        self.assertEqual(post_1.title, 'A Better Post Title')
        post_2 = Post(title="Good title", content='Content goes here', author='David')
        post_2.save()
        self.assertEqual(post_2.author, 'David')
