import mock
from nose.tools import assert_equal

import datetime

import pinkbelt
from pinkbelt.handle_trello import infer_branch_name, get_next_sunday

datetime_patcher = mock.patch.object(
    pinkbelt.handle_trello.datetime, 'date',
    mock.Mock(wraps=datetime.datetime)
)


class TestInferringBranch(object):

    def test_simple_url(self):
        assert_equal('bb-t-next', infer_branch_name(
            'https://trello.com/c/7b4Z3V8o/1803-bb-t-next'
        ))


class TestNextSunday(object):

    def setUp(self):
        self.mocked_datetime = datetime_patcher.start()

    def tearDown(self):
        datetime_patcher.stop()

    def test_middle_week(self):
        self.mocked_datetime.today.return_value = datetime.datetime(2015, 4, 1) # April's Fools! In fact, Wednesday

        sun = get_next_sunday()
        assert_equal(sun, datetime.date(2015, 4, 5))

    def test_monday(self):
        self.mocked_datetime.today.return_value = datetime.datetime(2015, 4, 6)

        sun = get_next_sunday()
        assert_equal(sun, datetime.date(2015, 4, 12))

    def test_sunday_yields_next_sunday(self):
        self.mocked_datetime.today.return_value = datetime.datetime(2015, 4, 5)

        sun = get_next_sunday()
        assert_equal(sun, datetime.date(2015, 4, 12))
