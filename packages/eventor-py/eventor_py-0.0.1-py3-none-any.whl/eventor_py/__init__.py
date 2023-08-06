'''
Python 3 API wrapper for https://eventor.orientering.se/.
Version: 2021.03.14
Author: William Grunder
'''

import os
import json
import logging
import requests
import inspect
import xml.etree.ElementTree as ET

BASE_URL = 'https://eventor.orientering.se/api'

# Config log
logging.basicConfig(filename='app.log', filemode='w', format='%(asctime)s - %(message)s')
logging.getLogger().setLevel(logging.INFO)

class Eventor():


    def __init__(self, apikey):

        self.e_template = 'An exception of type {0} occurred. Arguments:\n{1!r}'
        self.headers = {'ApiKey': apikey}
        self.save_xml = False
        self.save_json = False
        self.filepath = ""
        self.open_file = ""
        self.openfilepath = ""

        self.url_events = BASE_URL + '/events'
        self.url_documents = BASE_URL + '/events/documents'
        self.url_event = BASE_URL + '/event/'
        self.url_event_classes = BASE_URL + '/eventclasses'
        self.url_entry_fees = BASE_URL + '/entryfees/events/'
        self.url_org_apikey = BASE_URL + '/organisation/apiKey'
        self.url_organisations = BASE_URL + '/organisations'
        self.url_organisation = BASE_URL + '/organisation/'
        self.url_persons = BASE_URL + '/persons/organisations/'
        self.url_competitiors = BASE_URL + '/competitors'
        self.url_entries = BASE_URL + '/entries'
        self.url_competitior_count = BASE_URL + '/competitorcount'
        self.url_starts = BASE_URL + '/starts/event'
        self.url_startsIofXml = BASE_URL + '/starts/event/iofxml'
        self.url_starts_person = BASE_URL + '/starts/person'
        self.url_startsOrg = BASE_URL + '/starts/organisation'
        self.url_results = BASE_URL + '/results/event'
        self.url_resultsIofXml = BASE_URL + '/results/event/iofxml'
        self.url_resultsPerson = BASE_URL + '/results/person'
        self.url_resultsOrg = BASE_URL + '/results/organisation'
        self.url_activities = BASE_URL + '/activities'
        self.url_competitior = BASE_URL + '/competitor/'


    def saveXML(self, fileName, content):
        try:
            with open(fileName, 'wb') as file:
                file.write(content)
        except Exception as e:
            logging.error('Error while saving file')
            message = self.e_template.format(type(e).__name__, e.args)
            logging.error(message)


    def url_builder(self, apiurl, querys):
        if str(apiurl)[-1] == str('/'):
            try:
                eventId = querys['eventId']
                url = apiurl + str(eventId)
            except Exception:
                url = "None"
        else:
            try:
                url = apiurl + '?'
                for key, value in querys.items(): #Add Query-parameters
                    if url[-1] != '?':
                        url = url + '&'
                    url = url + (str(key) + '=' + str(value))
            except Exception as e:
                logging.error('Error while building url')
                message = self.e_template.format(type(e).__name__, e.args)
                logging.error(message)
        return url


    def fetch_data(self, url, querys):
        logging.info(url)
        logging.info(querys)

        url = self.url_builder(url, querys)
        logging.info(url)
        response = ''

        try:
            response = requests.get(url, headers=self.headers)
            logging.info(f'statuscode: {response.status_code}')
        except Exception as e:
            logging.error('Error sending request')
            message = self.e_template.format(type(e).__name__, e.args)
            logging.error(message)
        
        if self.save_xml == True:
            self.saveXML(self.filepath, response.content)

        return response


    def get_events(self, **kwargs):
        self.save_xml = False
        try:
            if ".xml" in kwargs["filepath"]:
                self.save_xml = True
                self.filepath = kwargs["filepath"]
            
        except Exception:
            pass

        response = self.fetch_data(self.url_events, kwargs)
        
        return response


    def parse_events(self, **kwargs):
        self.save_json = False
        try:
            if ".json" in kwargs["savefilepath"]:
                self.save_json = True
                self.filepath = kwargs["savefilepath"]
        except Exception:
            pass

        try:
            if ".xml" in kwargs["openfilepath"]:
                self.open_file = True
                self.openfilepath = kwargs["openfilepath"]
        except Exception:
            pass
        
        response = ""
        try:
            if kwargs["data"] != None:
                response = kwargs["data"]
        except Exception:
            pass

        if self.open_file:
            tree = ET.parse(self.openfilepath)
            root = tree.getroot()
        else:
            try:
                root = ET.fromstring(response.content)
            except Exception:
                pass

        events = root.findall("Event")

        event_list = []
        for event in events:
            event_name = event.find("Name").text
            event_id = event.find("EventId").text
            event_classification = event.find("EventClassificationId").text
            event_status = event.find("EventStatusId").text
            event_discipline = event.find("DisciplineId").text
            event_organiser = event.find("Organiser").findall("OrganisationId")
            event_organiser = [x.text for x in event_organiser]
            event_light_cond = event.find("EventRace").attrib["raceLightCondition"]
            event_distance = event.find("EventRace").attrib["raceDistance"]
            event_race_date = event.find("RaceDate")
            if event_race_date != None:
                event_date = event_race_date.find("Date").text
            else:
                event_date = event.find("StartDate").find("Date").text
            
            try:
                event_pos = event.find("EventCenterPosition").attrib
            except Exception:
                event_pos = ""


            event_list.append({"name": event_name, "id": event_id, "classification": event_classification,
                            "status": event_status, "discipline": event_discipline, "organiser": event_organiser,
                            "distance": event_distance, "light_cond": event_light_cond, "date": event_date,
                            "position": event_pos})

        if self.save_json:
            with open(self.filepath, 'w') as fp:
                json.dump(event_list, fp)
            
        return event_list

    def get_documents(self, **kwargs):
        return self.fetch_data(self.url_documents, kwargs)

    
    def get_event(self, **kwargs):
        self.save_xml = False
        try:
            if ".xml" in kwargs["filepath"]:
                self.save_xml = True
                self.filepath = kwargs["filepath"]
        except Exception:
            pass

        event = self.fetch_data(self.url_events, kwargs)

        return self.fetch_data(self.url_event, kwargs)
    

    def parse_event(self, **kwargs):
        self.save_json = False
        try:
            if ".json" in kwargs["savefilepath"]:
                self.save_json = True
                self.filepath = kwargs["savefilepath"]
        except Exception:
            pass

        try:
            if ".xml" in kwargs["openfilepath"]:
                self.open_file = True
                self.openfilepath = kwargs["openfilepath"]
        except Exception:
            pass
        
        response = ""
        try:
            if kwargs["data"] != None:
                response = kwargs["data"]
        except Exception:
            pass

        if self.open_file:
            tree = ET.parse(self.openfilepath)
            root = tree.getroot()
        else:
            try:
                root = ET.fromstring(response.content)
            except Exception:
                pass

        event_name = root.find("Name").text
        event_id = root.find("EventId").text
        event_classification = root.find("EventClassificationId").text
        event_status = root.find("EventStatusId").text
        event_discipline = root.find("DisciplineId").text
        event_organiser = root.find("Organiser").findall("OrganisationId")
        event_organiser = [x.text for x in event_organiser]
        event_light_cond = root.find("EventRace").attrib["raceLightCondition"]
        event_distance = root.find("EventRace").attrib["raceDistance"]
        event_race_date = root.find("RaceDate")
        if event_race_date != None:
            event_date = event_race_date.find("Date").text
        else:
            event_date = root.find("StartDate").find("Date").text
        
        try:
            event_pos = root.find("EventCenterPosition").attrib
        except Exception:
            event_pos = ""

        return  {"name": event_name, "id": event_id, "classification": event_classification,
                 "status": event_status, "discipline": event_discipline, "organiser": event_organiser,
                 "distance": event_distance, "light_cond": event_light_cond, "date": event_date,
                 "position": event_pos}


    def get_event_classes(self, **kwargs):
        return self.fetch_data(self.url_event_classes, kwargs)
    

    def get_entryfees(self, **kwargs):
        return self.fetch_data(self.url_entry_fees, kwargs)

    
    def get_organisations(self, **kwargs):
        return self.fetch_data(self.url_organisations, kwargs)


    def get_organisation_api(self, **kwargs):
        return self.fetch_data(self.url_org_apikey, kwargs)

    
    def get_organisation(self, **kwargs):
        return self.fetch_data(self.url_organisation, kwargs)

    
    def get_persons_org(self, **kwargs):
        return self.fetch_data(self.url_persons, kwargs)

    
    def get_competitiors(self, **kwargs):
        return self.fetch_data(self.url_competitiors, kwargs)
    

    def get_competitior_count(self, **kwargs):
        return self.fetch_data(self.url_competitior_count, kwargs)

    
    def get_entries(self, **kwargs):
        return self.fetch_data(self.url_entries, kwargs)

    
    def get_starts(self, **kwargs):
        return self.fetch_data(self.url_starts, kwargs)


    def get_starts_xml(self, **kwargs):
        return self.fetch_data(self.url_startsIofXml, kwargs)

    
    def get_starts_person(self, **kwargs):
        return self.fetch_data(self.url_starts_person, kwargs)

    
    def get_results(self, **kwargs):
        return self.fetch_data(self.url_results, kwargs)


    def get_results_xml(self, **kwargs):
        return self.fetch_data(self.url_resultsIofXml, kwargs)

    
    def get_results_person(self, **kwargs):
        return self.fetch_data(self.url_resultsPerson, kwargs)

    
    def get_results_org(self, **kwargs):
        return self.fetch_data(self.url_resultsOrg, kwargs)

    
    def get_activities(self, **kwargs):
        return self.fetch_data(self.url_activities, kwargs)


    def get_person(self, **kwargs):
        return self.fetch_data(self.url_competitior, kwargs)