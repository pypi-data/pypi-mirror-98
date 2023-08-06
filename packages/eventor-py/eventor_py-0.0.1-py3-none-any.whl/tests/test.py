import xml.etree.ElementTree as ET
from tabulate import tabulate

tree = ET.parse("get_events.xml")
root = tree.getroot()

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

print(tabulate(event_list, headers={'name': 'name', 'id': 'id'}))