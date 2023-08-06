import unittest
from eventor_py import Eventor
import os
from tabulate import tabulate
import json

class GetData(unittest.TestCase):



    def test_parse_events(self):
        apikey = os.environ.get('eventorAPI')
        eventor = Eventor(apikey)
        response = eventor.parse_events(openfilepath="D:\PROGRAMMERING\Python\EventorPy2\downloads\events.xml")
        #print(tabulate(response))


    def test_parse_event(self):
        apikey = os.environ.get('eventorAPI')
        eventor = Eventor(apikey)
        response = eventor.parse_event(openfilepath="D:\PROGRAMMERING\Python\EventorPy2\downloads\event.xml")
        print(response["name"])


if __name__ == '__main__':
    unittest.main()