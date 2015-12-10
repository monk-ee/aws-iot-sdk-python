# -*- coding: utf-8 -*-
"""
This is an SDK that allows you to connect to the AWS IoT Platform using python.
Copyright (c) 2015 Lyndon James Swan

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""
import unittest
import aws_iot_sdk

class AWSIotSDKTestCase(unittest.TestCase):
    maxDiff = None

    def test_simple(self):
        pass


if __name__ == '__main__':
    unittest.main()
