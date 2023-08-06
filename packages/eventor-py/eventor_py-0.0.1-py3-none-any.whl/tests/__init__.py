import unittest
from eventor_py import Eventor
import os
from tabulate import tabulate
import json

class GetData(unittest.TestCase):

    def test_init(self):
        apikey = os.environ.get('eventorAPI')
        eventor = Eventor(apikey)

    def test_get_event(self):
        apikey = os.environ.get('eventorAPI')
        eventor = Eventor(apikey)
        response = eventor.get_event(eventId="30549", filepath="D:\PROGRAMMERING\Python\EventorPy2\downloads\event.xml")

    def test_split(self):
        apikey = os.environ.get('eventorAPI')
        eventor = Eventor(apikey)
        events = eventor.get_events(fromDate="2015-03-15", toDate="2016-03-31", filepath="D:\PROGRAMMERING\Python\EventorPy2\downloads\events.xml")


if __name__ == '__main__':
    unittest.main()


