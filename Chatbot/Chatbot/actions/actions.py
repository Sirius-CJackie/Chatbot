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
import time
from typing import List, Text, Any, Dict

from rasa.shared.core.constants import ACTION_DEFAULT_FALLBACK_NAME
from rasa_sdk import Action, Tracker, FormValidationAction
from rasa_sdk.events import AllSlotsReset, UserUtteranceReverted
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.types import DomainDict
import sqlite3


music_name = []
album_name = []
singer_name =[]
obj_list = []

class ActionSubscriptionProvide(Action):

    def name(self) -> Text:
        return "action_subscription_provide"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        conn = sqlite3.connect('album.db')
        c = conn.cursor()
        c.execute('select music_name from album')

        res = c.fetchall()
        print(type(res))
        for r in res:
            print(type(r))
            msg = ' '.join(r) + "\n"
            dispatcher.utter_message(text=msg)
        conn.close()

        return []


class ValidateSimpleMusicForm(FormValidationAction):

    def name(self) -> Text:
        return "validate_simple_music_form"

    def validate_music(self, slot_value: Any, dispatcher: CollectingDispatcher, tracker: Tracker, domain: DomainDict) -> Dict[Text, Any]:

        dispatcher.utter_message(text=f"OK! You like the {slot_value}")

        return {"music": slot_value}

    def validate_email(self, slot_value: Any, dispatcher: CollectingDispatcher, tracker: Tracker, domain: DomainDict) -> Dict[Text, Any]:
        print(slot_value)
        dispatcher.utter_message(text=f"OK! Your email is {slot_value}")
        return {"email": slot_value}

    def validate_duration(self, slot_value: Any, dispatcher: CollectingDispatcher, tracker: Tracker, domain: DomainDict) -> Dict[Text, Any]:
        print(slot_value)
        dispatcher.utter_message(text=f"OK! Your duration is {slot_value} month")
        return {"duration": slot_value}


class ActionSubmitForm(Action):

    def name(self) -> Text:
        return "action_submit_form"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        music_name = tracker.get_slot("music")
        duration = tracker.get_slot("duration")
        email = tracker.get_slot("email")
        deadline = tracker.get_slot("deadline")
        print(email)
        deadline = time.strftime("%Y-%m-%d %H:%M:%S",time.localtime(time.time() + int(duration)*2592000))
        print(time)
        conn = sqlite3.connect('album.db')
        c = conn.cursor()
        c.execute('insert into subscription(music_name, email, deadline) values("'+music_name+'", "'+email+'", "' +str(deadline)+ '" )')
        conn.commit()
        conn.close()
        dispatcher.utter_message(text=f"I have completed the subscription for you.")
        return [AllSlotsReset()]

class QueryMusicInformByMusic(Action):

    def name(self) -> Text:
        return "action_query_music"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        music = next(tracker.get_latest_entity_values("music"), None)

        print(music)

        #print(email_number)
        #now_time = datetime.datetime.now()
        conn = sqlite3.connect('album.db')
        c = conn.cursor()
        c.execute('SELECT * FROM album WHERE music_name = "' + music + '"')
        res = c.fetchall()
        print(type(res))
        print(res)
        #print(res)
        conn.close()
        for r in res:
            print(r[1])
            print(type(r[1]))
            msg = '  '.join(r[1])
            dispatcher.utter_message(text='The album name is ' + ' '.join(r[0]) + ', the music name is ' + ' '.join(
                r[1]) + ', the singer is ' + ' '.join(r[2]) + ', the music type is ' + ' '.join(r[3]))
        return [AllSlotsReset()]

class QueryMusicInformBySinger(Action):

    def name(self) -> Text:
        return "action_query_singer"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        singer = next(tracker.get_latest_entity_values("singer"), None)

        print("+++++")

        conn = sqlite3.connect('album.db')
        c = conn.cursor()
        c.execute('SELECT * FROM album WHERE singer_name = "' + singer + '"')
        res = c.fetchall()
        print(type(res))
        print(res)
        # print(res)
        conn.close()
        for r in res:
            print(r[1])
            print(type(r[1]))
            msg = '  '.join(r[1])
            dispatcher.utter_message(text='The album name is ' + ' '.join(r[0]) + ', the music name is ' + ' '.join(
                r[1]) + ', the singer is ' + ' '.join(r[2]) + ', the music type is ' + ' '.join(r[3]))
        return [AllSlotsReset()]



class QueryMusicInformByAlbum(Action):

    def name(self) -> Text:
        return "action_query_album"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        album = next(tracker.get_latest_entity_values("album"), None)

        print("+++++")

        conn = sqlite3.connect('album.db')
        c = conn.cursor()
        c.execute('SELECT * FROM album WHERE album_name = "' + album + '"')
        res = c.fetchall()
        print(type(res))
        print(res)
        # print(res)
        conn.close()
        for r in res:
            print(r[1])
            print(type(r[1]))
            msg = '  '.join(r[1])
            dispatcher.utter_message(text='The album name is '+' '.join(r[0])+', the music name is '+' '.join(r[1])+', the singer is '+' '.join(r[2])+', the music type is '+' '.join(r[3]))
        return [AllSlotsReset()]


class QuerySubscriptionInform(Action):

    def name(self) -> Text:
        return "action_query_subscription"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        email = next(tracker.get_latest_entity_values("email"), None)

        print(email)

        conn = sqlite3.connect('album.db')
        c = conn.cursor()
        c.execute('SELECT * FROM subscription WHERE email = "' + email + '"')
        res = c.fetchall()
        print(type(res))
        print(res)
        # print(res)
        conn.close()
        for r in res:
            print(r[1])
            print(type(r[1]))
            dispatcher.utter_message(text='The music name is '+''.join(r[0])+', the The subscription deadline is '+''.join(r[2]))
        return [AllSlotsReset()]

class ValidateSimpleFeedbackForm(FormValidationAction):

    def name(self) -> Text:
        return "validate_simple_feedback_form"

    def validate_phone(self, slot_value: Any, dispatcher: CollectingDispatcher, tracker: Tracker, domain: DomainDict) -> Dict[Text, Any]:

        dispatcher.utter_message(text=f"OK! You like the {slot_value}")

        return {"phone": slot_value}

    def validate_email(self, slot_value: Any, dispatcher: CollectingDispatcher, tracker: Tracker, domain: DomainDict) -> Dict[Text, Any]:
        print(slot_value)
        dispatcher.utter_message(text=f"OK! Your email is {slot_value}")
        return {"email": slot_value}

    def validate_description(self, slot_value: Any, dispatcher: CollectingDispatcher, tracker: Tracker, domain: DomainDict) -> Dict[Text, Any]:
        print(slot_value)
        dispatcher.utter_message(text=f"OK! Your duration is {slot_value} month")
        return {"description": slot_value}

class ActionSubmitFeedback(Action):

    def name(self) -> Text:
        return "action_submit_feedback"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        phone = tracker.get_slot("phone")
        email = tracker.get_slot("email")
        description = tracker.get_slot("description")
        conn = sqlite3.connect('album.db')
        c = conn.cursor()
        c.execute('insert into feedback(phone, email, description) values("'+phone+'", "'+email+'", "' +description+ '" )')
        conn.commit()
        conn.close()
        dispatcher.utter_message(text=f"I have completed the subscription for you.")
        return [AllSlotsReset()]

