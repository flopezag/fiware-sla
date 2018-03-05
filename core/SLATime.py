#!/usr/bin/env python
# -*- encoding: utf-8 -*-
##
# Copyright 2017 FIWARE Foundation, e.V.
# All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.
##

from datetime import datetime
from datetime import timedelta

__author__ = 'fla'


class SLATime:
    def __init__(self):
        pass

    @staticmethod
    def adjust_time_delta(t, start, stop):

        start_hour = start.seconds//3600
        end_hour = stop.seconds//3600
        zero = timedelta(0)

        '''if t - t.replace(hour=start_hour, minute=0, second=0) < zero:
            t = t.replace(hour=start_hour, minute=0, second=0, microsecond=0)
        elif t - t.replace(hour=end_hour, minute=0, second=0) > zero:
            t = t.replace(hour=end_hour, minute=0, second=0, microsecond=0)
        '''
        weekday = t.weekday()

        if weekday == 6 or weekday == 5:
            t = t.replace(day=t.day+(7-weekday), hour=start_hour, minute=0, second=0)
        else:
            if t - t.replace(hour=start_hour, minute=0, second=0) < zero:
                t = t.replace(hour=start_hour, minute=0, second=0, microsecond=0)
            elif t - t.replace(hour=end_hour, minute=0, second=0) > zero:
                t = t.replace(hour=end_hour, minute=0, second=0, microsecond=0)

        return t

    @staticmethod
    def full_in_between_working_days(first_date, second_date):
        working = 0

        a_day = timedelta(days=1)
        a_day_total_seconds = a_day.total_seconds()

        # We discard the first and last day due to we calcutate the diff in the other methods.
        first_date_new = \
            first_date.replace(day=first_date.day, hour=0, minute=0, second=0, microsecond=0) + timedelta(days=1)

        second_date_new = \
            second_date.replace(day=second_date.day,
                                hour=23,
                                minute=59,
                                second=59,
                                microsecond=999999) - timedelta(days=1)

        precision = 0.000001

        if first_date_new.date() == second_date_new.date():
            # Both are in the same date, therefore there is no days between the a and b
            pass
        else:
            while (second_date_new - first_date_new).total_seconds() + precision >= a_day_total_seconds:
                if second_date_new.weekday() < 5:
                    working += 1

                second_date_new = second_date_new - timedelta(days=1)

        return working

    @staticmethod
    def office_time_between(a, b,
                            start=timedelta(hours=8, minutes=0, seconds=0, milliseconds=0),
                            stop=timedelta(hours=17, minutes=0, seconds=0, milliseconds=0)):
        """
        Return the total office time between `a` and `b` as a timedelta
        object. Office time consists of weekdays from `start` to `stop`
        (default: 08:00 to 17:00).
        """
        zero = timedelta(0)
        assert(zero <= start <= stop <= timedelta(1))

        # Adjust the date to the working date
        a_delta = SLATime.adjust_time_delta(t=a, start=start, stop=stop)
        b_delta = SLATime.adjust_time_delta(t=b, start=start, stop=stop)

        if a_delta.date() == b_delta.date():
            # It is in the same day, therefore just a difference of the two dates
            time_diff = b_delta - a_delta
        else:
            # There are some days between the two dates. Therefore we have to
            # calculate those days.

            # Get the number of complete days between a and b without weekend days
            office_day = stop - start
            complete_working_date = SLATime.full_in_between_working_days(a, b)

            # Calculate the work activity the first and last days
            stop_delta = a_delta
            stop_delta = stop_delta.replace(hour=17, minute=0, second=0, microsecond=0)

            start_delta = b_delta
            start_delta = start_delta.replace(hour=8, minute=0, second=0, microsecond=0)

            time_diff_a = stop_delta - a_delta
            time_diff_b = b_delta - start_delta

            # Add the difference work hours plus the complete working days times office hour day
            time_diff = time_diff_a + time_diff_b + complete_working_date * office_day

        return time_diff


if __name__ == "__main__":
    a = datetime(2018, 2, 16, 14, 35, 24, 43)
    b = datetime(2018, 2, 19, 7, 54, 34, 24)

    slatime = SLATime()

    print(slatime.office_time_between(a, b))
    print(slatime.office_time_between(a, b).total_seconds())
