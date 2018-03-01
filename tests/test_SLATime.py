# -*- encoding: utf-8 -*-
#
# Copyright 2014 Telefonica Investigación y Desarrollo, S.A.U
#
# This file is part of FI-WARE project.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
#
# You may obtain a copy of the License at:
#
#        http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#
# See the License for the specific language governing permissions and
# limitations under the License.
#
# For those usages not covered by the Apache version 2.0 License please
# contact with opensource@tid.es
#
__author__ = 'fla'

from unittest import TestCase
from core.SLATime import SLATime
from datetime import datetime, timedelta


class TestAjustHours(TestCase):
    pass

    def test_adjust_time_delta_inside_workday(self):
        """The adjust time inside working day is the same time"""
        a = datetime(2018, 2, 16, 14, 35, 24, 43)
        start = timedelta(hours=8)
        stop = timedelta(hours=17)

        time_delta = SLATime.adjust_time_delta(a, start, stop)
        expected_time_delta = datetime(year=2018, month=2, day=16, hour=14, minute=35, second=24, microsecond=43)

        self.assertEqual(expected_time_delta, time_delta)

    def test_adjust_time_delta_after_the_end_workday(self):
        """The adjust time inside working day is the same time"""
        a = datetime(2018, 2, 16, 18, 35, 24, 43)
        start = timedelta(hours=8)
        stop = timedelta(hours=17)

        time_delta = SLATime.adjust_time_delta(a, start, stop)
        expected_time_delta = datetime(year=2018, month=2, day=16, hour=17, minute=0, second=0, microsecond=0)

        self.assertEqual(expected_time_delta, time_delta)

    def test_adjust_time_delta_before_the_beginning_workday(self):
        """The adjust time inside working day is the same time"""
        a = datetime(2018, 2, 16, 7, 35, 24, 43)
        start = timedelta(hours=8)
        stop = timedelta(hours=17)

        time_delta = SLATime.adjust_time_delta(a, start, stop)
        expected_time_delta = datetime(year=2018, month=2, day=16, hour=8, minute=0, second=0, microsecond=0)

        self.assertEqual(expected_time_delta, time_delta)


class TestFullDaysBetweenDays(TestCase):
    pass

    def test_full_between_same_working_days(self):
        """The adjust time inside working day is the same time"""
        a = datetime(2018, 2, 16, 7, 35, 24, 43)
        b = datetime(2018, 2, 16, 7, 35, 24, 43)

        days = SLATime.full_in_between_working_days(a, b)
        expected_days = 0

        self.assertEqual(expected_days, days)

    def test_full_between_working_days_weekend(self):
        """The adjust time inside working day is the same time"""
        a = datetime(2018, 2, 16, 7, 35, 24, 43)
        b = datetime(2018, 2, 18, 8, 47, 43, 12)

        days = SLATime.full_in_between_working_days(a, b)
        expected_days = 0

        self.assertEqual(expected_days, days)

    def test_full_between_working_days_weekend_2(self):
        """The adjust time inside working day is the same time"""
        a = datetime(2018, 2, 16, 7, 35, 24, 43)
        b = datetime(2018, 2, 19, 8, 47, 43, 12)

        days = SLATime.full_in_between_working_days(a, b)
        expected_days = 0

        self.assertEqual(expected_days, days)

    def test_full_between_wrong_working_days(self):
        """The adjust time inside working day is the same time"""
        a = datetime(2018, 2, 16, 7, 35, 24, 43)
        b = datetime(2018, 2, 15, 7, 35, 24, 43)

        days = SLATime.full_in_between_working_days(a, b)
        expected_days = 0

        self.assertEqual(expected_days, days)

    def test_full_between_normal_working_days(self):
        """The adjust time inside working day is the same time"""
        a = datetime(2018, 2, 15, 7, 35, 24, 43)
        b = datetime(2018, 2, 16, 7, 35, 24, 43)

        days = SLATime.full_in_between_working_days(a, b)
        expected_days = 0

        self.assertEqual(expected_days, days)

    def test_full_between_normal_working_days_1(self):
        """The adjust time inside working day is the same time"""
        a = datetime(2018, 2, 15, 7, 35, 24, 43)
        b = datetime(2018, 2, 16, 7, 35, 24, 42)

        days = SLATime.full_in_between_working_days(a, b)
        expected_days = 0

        self.assertEqual(expected_days, days)

    def test_full_between_normal_working_days_2(self):
        """The adjust time inside working day is the same time"""
        a = datetime(2018, 2, 15, 7, 35, 24, 43)
        b = datetime(2018, 2, 16, 7, 35, 24, 44)

        days = SLATime.full_in_between_working_days(a, b)
        expected_days = 0

        self.assertEqual(expected_days, days)

    def test_full_between_casuistic_1(self):
        """The adjust time inside working day is the same time"""
        a = datetime(2018, 2, 18, 6, 36, 12)
        b = datetime(2018, 2, 19, 7, 35, 24)

        days = SLATime.full_in_between_working_days(a, b)
        expected_days = 0

        self.assertEqual(expected_days, days)

    def test_full_between_casuistic_2(self):
        """The adjust time inside working day is the same time"""
        a = datetime(2017, 12, 17, 14, 36, 12)
        b = datetime(2017, 12, 19, 7, 35, 24)

        days = SLATime.full_in_between_working_days(a, b)
        expected_days = 0

        self.assertEqual(expected_days, days)

    def test_full_between_casuistic_3(self):
        """The adjust time inside working day is the same time"""
        a = datetime(2018, 1, 31, 14, 36, 12)
        b = datetime(2018, 2, 2, 8, 35, 24)

        days = SLATime.full_in_between_working_days(a, b)
        expected_days = 0

        self.assertEqual(expected_days, days)

    def test_full_between_casuistic_4(self):
        """The adjust time inside working day is the same time"""
        a = datetime(2018, 1, 29, 14, 36, 12)
        b = datetime(2018, 2, 1, 8, 35, 24)

        days = SLATime.full_in_between_working_days(a, b)
        expected_days = 2

        self.assertEqual(expected_days, days)


class TestDifferenceOfficeTime(TestCase):
    pass

    def test_office_time_between_two_dates_in_the_same_day_1(self):
        a = datetime(2018, 2, 16, 8, 35, 24, 35)
        b = datetime(2018, 2, 16, 12, 24, 53, 12)

        official_time = SLATime.office_time_between(a, b)
        expected_diff = timedelta(hours=3, minutes=49, seconds=28, microseconds=999977)

        self.assertEqual(expected_diff, official_time)

    def test_office_time_between_two_dates_in_the_same_day_2(self):
        a = datetime(2018, 2, 16, 7, 35, 24, 12)
        b = datetime(2018, 2, 16, 12, 24, 53, 12)

        official_time = SLATime.office_time_between(a, b)
        expected_diff = timedelta(hours=4, minutes=24, seconds=53, microseconds=12)

        self.assertEqual(expected_diff, official_time)

    def test_office_time_between_two_dates_in_the_same_day_3(self):
        a = datetime(2018, 2, 16, 8, 35, 24, 35)
        b = datetime(2018, 2, 16, 18, 23, 51, 12)

        official_time = SLATime.office_time_between(a, b)
        expected_diff = timedelta(hours=8, minutes=24, seconds=35, microseconds=999965)

        self.assertEqual(expected_diff, official_time)

    def test_office_time_between_two_dates_in_the_same_day_4(self):
        a = datetime(2018, 2, 16, 7, 35, 24, 12)
        b = datetime(2018, 2, 16, 18, 23, 51, 7)

        official_time = SLATime.office_time_between(a, b)
        expected_diff = timedelta(hours=9)

        self.assertEqual(expected_diff, official_time)

    def test_office_time_between_two_friday_and_monday(self):
        a = datetime(2018, 2, 16, 9, 17, 59, 990071)
        b = datetime(2018, 2, 19, 14, 23, 37, 874513)

        official_time = SLATime.office_time_between(a, b)
        expected_diff = timedelta(hours=14, minutes=5, seconds=37, microseconds=884442)

        self.assertEqual(expected_diff, official_time)

    def test_office_time_between_two_friday_and_wednesday(self):
        a = datetime(2018, 2, 16, 9, 17, 59, 990071)
        b = datetime(2018, 2, 21, 14, 23, 37, 874513)

        official_time = SLATime.office_time_between(a, b)
        expected_diff = timedelta(hours=32, minutes=5, seconds=37, microseconds=884442)

        self.assertEqual(expected_diff, official_time)

    def test_office_time_between_two_monday_and_friday(self):
        a = datetime(2018, 2, 12, 9, 17, 59, 990071)
        b = datetime(2018, 2, 16, 14, 23, 37, 874513)

        official_time = SLATime.office_time_between(a, b)
        expected_diff = timedelta(hours=41, minutes=5, seconds=37, microseconds=884442)

        self.assertEqual(expected_diff, official_time)

    def test_office_time_between_two_friday_and_monday_1(self):
        a = datetime(2018, 2, 16, 7, 13, 21, 990071)
        b = datetime(2018, 2, 19, 21, 23, 37, 874513)

        official_time = SLATime.office_time_between(a, b)
        expected_diff = timedelta(hours=18)

        self.assertEqual(expected_diff, official_time)

    def test_office_time_between_weekend_and_monday(self):
        a = datetime(2018, 1, 7, 20, 0, 15)
        b = datetime(2018, 1, 8, 12, 53, 10, 275)

        official_time = SLATime.office_time_between(a, b)
        expected_diff = timedelta(hours=4, minutes=53, seconds=10, microseconds=275)

        self.assertEqual(expected_diff, official_time)

    def test_strange_casuistic_1(self):
        a = datetime(2017, 12, 17, 14, 40, 16)
        b = datetime(2017, 12, 18, 7, 50, 14, 495000)

        expected_diff = timedelta(hours=0)
        official_time = SLATime.office_time_between(a, b)

        self.assertEqual(expected_diff, official_time)

    def test_strange_casuistic_2(self):
        a = datetime(2017, 12, 17, 14, 40, 16)
        b = datetime(2017, 12, 19, 07, 34, 25)

        expected_diff = timedelta(hours=9)
        official_time = SLATime.office_time_between(a, b)

        self.assertEqual(expected_diff, official_time)

    def test_strange_casuistic_3(self):
        a = datetime(2017, 11, 20, 03, 41, 16)
        b = datetime(2017, 11, 20, 05, 03, 2, 809000)

        expected_diff = timedelta(hours=0)
        official_time = SLATime.office_time_between(a, b)

        self.assertEqual(expected_diff, official_time)

    def test_strange_casuistic_4(self):
        a = datetime(2017, 11, 20, 03, 41, 16)
        b = datetime(2017, 11, 20, 05, 03, 11)

        expected_diff = timedelta(hours=0)
        official_time = SLATime.office_time_between(a, b)

        self.assertEqual(expected_diff, official_time)

    def test_strange_casuistic_5(self):
        a = datetime(2017, 11, 13, 04, 12, 15)
        b = datetime(2017, 11, 13, 05, 02, 30, 883000)

        expected_diff = timedelta(hours=0)
        official_time = SLATime.office_time_between(a, b)

        self.assertEqual(expected_diff, official_time)

    def test_strange_casuistic_6(self):
        a = datetime(2017, 11, 13, 4, 12, 15)
        b = datetime(2017, 12, 04, 8, 24, 26)

        expected_diff = timedelta(days=5, hours=15, minutes=24, seconds=26)
        official_time = SLATime.office_time_between(a, b)

        self.assertEqual(expected_diff, official_time)

    def test_strange_casuistic_7(self):
        a = datetime(2017, 11, 06, 06, 36, 14)
        b = datetime(2017, 11, 06, 06, 39, 23, 320000)

        expected_diff = timedelta(hours=0)
        official_time = SLATime.office_time_between(a, b)

        self.assertEqual(expected_diff, official_time)

    def test_strange_casuistic_8(self):
        a = datetime(2017, 11, 06, 06, 36, 14)
        b = datetime(2017, 11, 06, 06, 39, 47)

        expected_diff = timedelta(hours=0)
        official_time = SLATime.office_time_between(a, b)

        self.assertEqual(expected_diff, official_time)

    def test_strange_casuistic_9(self):
        a = datetime(2017, 11, 06, 06, 36, 14)
        b = datetime(2017, 11, 06, 06, 36, 14)

        expected_diff = timedelta(hours=0)
        official_time = SLATime.office_time_between(a, b)

        self.assertEqual(expected_diff, official_time)

    def test_strange_casuistic_10(self):
        a = datetime(2018, 2, 18, 06, 36, 14)
        b = datetime(2018, 2, 19, 06, 36, 14)

        expected_diff = timedelta(hours=0)
        official_time = SLATime.office_time_between(a, b)

        self.assertEqual(expected_diff, official_time)
