import unittest
from unittest import TestCase
from unittest.mock import patch, call

import timesheets   


class TestTimeSheets(TestCase):

    """mock input() and force it to return a value"""

    @patch('builtins.input', return_value='2')
    def test_get_hours_for_day(self, mock_input):
        hours = timesheets.get_hours_for_day('Monday')
        self.assertEqual(2,hours)

    @patch('builtins.input', side_effect=['ball',' ','fish','123','baa123','2'])
    def test_get_hours_for_day_non_numeric_rejected(self, mock_input):
        hours = timesheets.get_hours_for_day('Monday')
        self.assertEqual(2,hours)

    @patch('builtins.input', side_effect=['93','71','-1','123','80','2'])
    def test_get_hours_for_day_numbers_not_between_valid_range(self, mock_input):
        hours = timesheets.get_hours_for_day('Monday')
        self.assertEqual(2,hours)

    @patch('builtins.print')
    def test_display_total(self,mock_print):
        timesheets.display_total(123)
        mock_print.assert_called_once_with('Total hours worked: 123')

    @patch('timesheets.alert')
    def test_alert_meet_min_hours_doesnt_meet(self, mock_alert):
        timesheets.alert_not_meet_min_hours(13,30)
        mock_alert.assert_called_once()

    @patch('timesheets.alert')
    def test_alert_meet_min_hours_does_meet_min(self, mock_alert):
        timesheets.alert_not_meet_min_hours(40,30)
        mock_alert.assert_not_called()

    @patch('timesheets.get_hours_for_day')
    def test_get_hours(self, mock_get_hours):
        mock_hours = [5,6,7]
        mock_get_hours.side_effect = mock_hours
        days = ['m','t','w']
        # the dict zip funtions makes the first dictionary keys and the second one becomes values
        expected_hours = dict(zip(days,mock_hours))
        hours = timesheets.get_hours(days)
        self.assertEqual(expected_hours,hours)

    @patch('builtins.print')
    def test_display_hours(self, mock_print):

        #arranging everything
        example = {'M': 3, 'T': 12, 'W': 6}
        expected_table_calls = [
            call('Day            Hours Worked   '),
            call('M              3              '),
            call('T              12             '),
            call('W              6              ')
        ]

        timesheets.display_hours(example)
        mock_print.assert_has_calls(expected_table_calls)

    def test_total_hours(self):
        example = {'M': 3, 'T': 12, 'W': 6}
        total = timesheets.total_hours(example)
        expected_total = 3+12+6
        self.assertEqual(total,expected_total)
