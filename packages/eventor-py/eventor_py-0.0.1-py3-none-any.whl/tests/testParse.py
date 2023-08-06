import unittest
from eventor_py import Eventor
import os
from tabulate import tabulate
import json

class GetData(unittest.TestCase):

    def test_init(self):
        apikey = os.environ.get('eventorAPI')
        eventor = Eventor(apikey)

    def test_parse_events(self):
        apikey = os.environ.get('eventorAPI')
        eventor = Eventor(apikey)
        response = eventor.parse_events(filepath="D:\PROGRAMMERING\Python\EventorPy2\downloads\events.xml")



if __name__ == '__main__':
    unittest.main()