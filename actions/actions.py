# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


# This is a simple example for a custom action which utters "Hello World!"

# from typing import Any, Text, Dict, List
#
# from rasa_sdk import Action, Tracker
# from rasa_sdk.executor import CollectingDispatcher
#
#
# class ActionHelloWorld(Action):
#
#     def name(self) -> Text:
#         return "action_hello_world"
#
#     def run(self, dispatcher: CollectingDispatcher,
#             tracker: Tracker,
#             domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
#
#         dispatcher.utter_message(text="Hello World!")
#
#         return []

from typing import Any, Text, Dict, List

from rasa_sdk import Action, Tracker
from rasa_sdk.events import SlotSet, EventType
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.forms import FormAction
from rasa_sdk.events import FollowupAction

from datetime import datetime as dt , timedelta
import time
from dateutil.relativedelta import *
from dateutil.easter import *
from dateutil.rrule import *
from dateutil.parser import *
from datetime import *

def customParser(inp):
    # inp= input("Enter the string: ")
    user = inp.lower()
    td=None
    ku=None
    current_time = dt.now()
    # print(current_time)

    try:
        ku = parse(user, fuzzy=True)
        return ku
        print(ku.strftime("%I:%M %p"))
    except:
        td=timedelta(hours=1)

        if(user=="in half an hour" or user == "half an hour" or user == "half hour"):
            td=timedelta(minutes=30)
        elif(user=="in one hour" or user == "one hour" or user == "after one hour" or user == "after an hour"):
            td = timedelta(hours=1)
        elif(user=="in two hours" or user =="in two hour" or user =="two hour" or user == "after two hours" or user == "after two hour"):
            td= timedelta(hours=2)
        elif(user=="now" or user=="this moment"):
            td= timedelta(hours=0)
        elif(user=="in fifteen minutes" or user=="in fifteen minute"):
            td= timedelta(minutes=15)
        elif(user=="in ten minutes" or user=="in ten minute"):
            td= timedelta(minutes=10)
        elif(user=="in five minutes" or user=="in five minute"):
            td= timedelta(minutes=5)
        elif(user=="in twenty minutes" or user=="in twenty minute" or user=="in 20 minute" or user=="in 20 minutes"):
            td= timedelta(minutes=20)
        elif(user=="in thirty minutes" or user=="in thirty minute" or user=="in 30 minute" or user=="in 30 minutes"):
            td= timedelta(minutes=30)
            

        ku=current_time+td
        return ku
        print(ku.strftime("%I:%M %p"))

def roundOff(y):
    minute=y.strftime("%M")
    if(int(minute)>=30): minute=int(minute)-30
    # print(type(minute))
    to_cal=timedelta(minutes=int(minute))
    return y-to_cal

def isValid(x):
    dls=parse("7PM")
    dle=parse("10pm")
    return (x>dls and x<dle)

class timePar(Action):

    def name(self) -> Text:
        return "action_parse"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        var1 = tracker.get_slot("time")
        var2 = customParser(var1)

        # var3 = var2.strftime("%I:%M %p")
        # return [SlotSet("time", var3)]

        if(isValid(var2)):
            # var3 = var2.strftime("%I:%M %p")
            var3=roundOff(var2)
            var4= var3.strftime("%I:%M%p")
            return [SlotSet("time", var4)]
        else:
            dispatcher.utter_message(text=" We are not open at that time. We are only open from 7pm to 10pm")
            return [SlotSet("time", None),FollowupAction(name = "input_form")] 
            # SlotSet("time", None)
            # return [Form(input_form)]



# class InputForm(Action):
#     def name(self) -> Text:
#         return "input_form"

#     def run(
#         self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict
#     ) -> List[EventType]:
#         required_slots = ["seats", "section"]

#         for slot_name in required_slots:
#             if tracker.slots.get(slot_name) is None:
#                 # The slot is not filled yet. Request the user to fill this slot next.
#                 return [SlotSet("requested_slot", slot_name)]

#         # All slots are filled.
#         return [SlotSet("requested_slot", None)]

class ActionSubmit(Action):
    def name(self) -> Text:
        return "action_submit"

    def run(
        self,
        dispatcher,
        tracker: Tracker,
        domain: "DomainDict",
    ) -> List[Dict[Text, Any]]:
        dispatcher.utter_message(template="utter_submit",
                                 seats=tracker.get_slot("seats"),
                                 section=tracker.get_slot("section"))


class SetAC(Action):

    def name(self) -> Text:
        return "action_setAC"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        # dispatcher.utter_message(text="Hello World!")

        return [SlotSet("section", "AC")]

class SetNAC(Action):

    def name(self) -> Text:
        return "action_setNAC"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        # dispatcher.utter_message(text="Hello World!")

        return [SlotSet("section", "non-AC")]


