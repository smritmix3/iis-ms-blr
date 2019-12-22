from typing import Dict, Text, Any, List, Union, Optional
from rasa_sdk import Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.forms import FormAction
from rasa_sdk import Action
from rasa_sdk.events import (SlotSet,AllSlotsReset)
import requests
from requests.auth import HTTPBasicAuth
import json
from datetime import datetime
from datetime import date
import re
import pytest
from datetime import time, date, timedelta, datetime
from dateutil import parser
from dateutil.tz import tzlocal
from duckling import DucklingWrapper, Dim
from rasa_sdk.events import Restarted
d = DucklingWrapper()


class DateForm(FormAction):
    def name(self):
        return "date_form"

    @staticmethod
    def required_slots(tracker: Tracker) -> List[Text]:
        return ["from", "to"]

    def slot_mappings(self) -> Dict[Text, Union[Dict, List[Dict]]]:
        return { "from":[self.from_text(not_intent=["stop"])],
                "to":[self.from_text(not_intent=["stop"])]}
    def validate_from(
        self,
        value: Text,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> Optional[Text]:
        #print("To initial Date: ", value)
     #text = '2nd aug 2020'
            try:
                print("value ****"+value)
                if value == 'stop':
                    intent= tracker.latest_message["intent"].get("name")
                    if intent == "stop":
                        return [self.deactivate(), FollowupAction('action_slot_cancel')]
                else:
                    date = d.parse_time(value)
                    #if type(date) == str:
                    print("----"+str(date[0]['value']['value']) )
                    # else:
                    #    print("----"+str(date[0]['value']['value']['from']))
        
                    print(d.parse_time(value))
                    date = d.parse_time(value)
                    # print("date: "+date[0]['value']['value'])
                    print("date================================"+ str(date))
                    # if type(date) == str:
                    print("----"+str(date[0]['value']['value']))
                    Ducklingvalue = date[0]['value']['value']
                    # else:
                    #     print("----"+str(date[0]['value']['value']['from']) )
                    #     Ducklingvalue = date[0]['value']['value']['from']
                    from_date = Ducklingvalue[0:4]
                    print("from_date: ",from_date)
                    current_text = 'today'
                    current_date = d.parse_time(current_text)
                    print("current_date: "+str(current_date))
                    Current_date_Ducklingvalue = current_date[0]['value']['value']
                    print("Current_date_Ducklingvalue: "+str(Current_date_Ducklingvalue))
                    current_year = Current_date_Ducklingvalue[0:4]
                    print("current_year: "+str(current_year))
                    ############################################################ Validation Code
                    today = str(current_year)
                    count = abs(int(from_date)-int(today))
                    final_date=''
                    if count > 0 or count < 0:
                        #print("if")
                        final_date = today+Ducklingvalue[4:10]
                    else:
                        #print("else")
                        final_date = Ducklingvalue[0:10]
                    print("From Date: "+ final_date )
            except Exception as e:
                # print(e.message)
                # print ("Error: IndexError")
                # print(e.message)
                dispatcher.utter_message("Provide input in proper format. e.g. 17th sept.")
            else:
                return {'from': final_date}
    def validate_to(
        self,
        value: Text,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> Optional[Text]:
        print(str(tracker.latest_message["intent"]))
        intent= tracker.latest_message["intent"].get("name")
        if intent == "stop":
            return [self.deactivate(), FollowupAction('action_slot_cancel')]
        else:
            try:
                print(d.parse_time(value))
                date = d.parse_time(value)
                print("date: "+str(date[0]['value']['value']) )
            except IndexError:
                print ("Error: IndexError")
                dispatcher.utter_message("Provide input in proper format")
            else:
                #print("To initial Date: ", value)
                print(d.parse_time(value))
                date = d.parse_time(value)
                #if type(date) == str:
                print("----"+str(date[0]['value']['value']) )
                Ducklingvalue = date[0]['value']['value']
                # else:
                #     print("----"+str(date[0]['value']['value']['from']) )
                #     Ducklingvalue = date[0]['value']['value']['from'] 

                #Ducklingvalue = date[0]['value']['value']
                to_date = Ducklingvalue[0:4]
                print("to_date: ",to_date)

                ############################################################# Current Date
                current_text = 'today'
                current_date = d.parse_time(current_text)
                print("current_date: ",current_date)
                Current_date_Ducklingvalue = current_date[0]['value']['value']
                print("Current_date_Ducklingvalue: ",Current_date_Ducklingvalue)
                current_year = Current_date_Ducklingvalue[0:4]
                print("current_year: ",current_year)

                ############################################################ Validation Code
                today = str(current_year)
                count = abs(int(to_date)-int(today))
                final_date=''
                if count > 0 or count < 0:
                    #print("if")
                    final_date = today+Ducklingvalue[4:10]
                else:
                    #print("else")
                    final_date = Ducklingvalue[0:10]
                print("to Date: "+ final_date )
                return {'to': final_date}
    def submit(self,dispatcher: CollectingDispatcher,tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict]:
        dispatcher.utter_template("utter_submit", tracker)
        return[] 
class SlotCancel(Action):  
    def name(self):         
        return 'action_slot_cancel'  
    def run(self, dispatcher, tracker, domain):
        dispatcher.utter_template('utter_logout',tracker)
        return [Restarted()]   
    
class SlotNextAction(Action):  
    def name(self):         
        return 'action_next_action'  
    def run(self, dispatcher, tracker, domain):
        dispatcher.utter_message("form is deactivated======")
        print("form is deactivated==================")
        #return [FollowupAction('action_validateEmail')]  


class QCfailedRecords(Action):
    """This class is for checking qcfailedrecords"""

    def name(self):
        return "action_esi_forge_qcfailedrecords"

    def run(self, dispatcher, tracker, domain):
        print("action_esi_forge_qcfailedrecords is running")
        try:
            url = "/"
            username= ""
            password = "9d611be6-d4ef-4db3-aa84-e065b498f721"
            from_date = str(tracker.get_slot('from'))+'T00:00:00.000Z'
            to_date = str(tracker.get_slot('to'))+'T00:00:00.000Z'
            auth_values = (username, password)
            value = {
                "FromDate":from_date,
                "ToDate":to_date,
                "QC_Status":"true"
            }
            value1 = {
                "FromDate":from_date,
                "ToDate":to_date,
                "QC_Status":"false"
            }
            result = requests.post(url, data=json.dumps(value), auth=HTTPBasicAuth(username, password))
            result1 = requests.post(url, data=json.dumps(value1), auth=HTTPBasicAuth(username, password))
            qcfailedrecordsResult=""
            str1=""
            str2=""
            if result.status_code != 200:
                print(result.status_code)
                dispatcher.utter_template('utter_technical_error_template',tracker)
            if value.get('QC_Status') == "true":
                json_data = result.json()
                print(json_data)
                for each in json_data:
                    str1=str1+str(each['QC_Verified'])
                    print(str1)
                    if str1 == "No Records found":
                        qcverifiedcount=0
                        print("QC verified Count:"+str(qcverifiedcount))
                        break
                    else:
                        qcverifiedcount = len(json_data)
                        print("QC verified Count:"+str(qcverifiedcount))
                        break

            if result1.status_code != 200:
                print(result1.status_code)
                dispatcher.utter_template('utter_technical_error_template',tracker)
            if value1.get('QC_Status') == "false":
                json_data = result1.json()
                print(json_data)
                for each in json_data:
                    str2=str2+str(each['QC_Verified'])
                    print(str2)
                    if str2 == "No Records found":
                        qcnonverifiedcount=0
                        print("QC non verified Count: "+str(qcnonverifiedcount))
                        break
                    else:
                        qcnonverifiedcount = len(json_data)
                        print("QC non verified Count: "+str(qcnonverifiedcount))
                        break
            dispatcher.utter_message("QC verified Count : "+ str(qcverifiedcount) +'</br>'+ "QC non verified Count :" + str(qcnonverifiedcount))
            return[SlotSet("from",None),SlotSet("to",None)]
            
        except Exception as e:
            dispatcher.utter_message("No data is available")
            print("Exception: ",e) 

class  CheckPhoneQCData(Action):
    """This class is for checking phone QCData"""

    def name(self):
        return "action_esi_forge_checkphoneqcdata"

    def run(self, dispatcher, tracker, domain):    
        # print("action_qc_checkphonedata is running")  
        try: 
            url = 
            user = "
            passwd = 

            #Phoneid= tracker.get_slot("Phone_ID")
            # print("Phone_ID from action",Phoneid)
            Phoneid = tracker.latest_message.get('text')
            print("=================Phoneid"+ str(Phoneid))
            #auth_values = (user, passwd)
            value= {"Phone_ID":Phoneid}

            response = requests.post(
                url, data=json.dumps(value), auth=HTTPBasicAuth(user, passwd)
            )  
            # response1=response.json()
            # print(response1)
            str1= " "
            if response.status_code != 200:
                print(response.status_code)
                dispatcher.utter_template('utter_technical_error_template',tracker)
            else:
                json_data = response.json()
                phoneqcdataVar = " "
                for each in json_data:
                    str1=str1+"Name: "+str(each['Name']) + "\n" + "Dimensions_Height: "+str(each['Dimentions_Height'])+"\n"+"Dimensions_Width: "+str(each['Dimentions_Width'])+"\n"+"Dimensions_Depth: "+str(each['Dimentions_Depth'])+"\n"+"Color_FrontSideName: "+str(each['Color_FrontSideName'])+"\n"+"Color_FrontSideCode: "+str(each['Color_FrontSideCode'])+"\n"+"Color_RearSideName: "+str(each['Color_RearSideName'])+"\n"+"Color_RearSideCode: "+str(each['Color_RearSideCode'])+"\n"+"Color_GlassName: "+str(each['Color_GlassName'])+"\n"+"Color_GlassCode: "+str(each['Color_GlassCode'])+"\n"+ "Thermal_StandardHeat:" +str(each['Thermal_StandardHeat'])+"\n"+"Thermal_MaxHeat: "+str(each['Thermal_MaxHeat'])
                print(str1)
            dispatcher.utter_message("The details of phoneQCdata are here </br>"+str1)
            return[SlotSet('Phone_ID', Phoneid)] 
        except Exception as e:
            dispatcher.utter_message("No PhoneQCdata is available for this ID")
            print("Exception: ",e)     

# =========================================================================== #
# ====================================================================================================================== #        



#========================

class innovMF(Action):
    """This class is for innov8 MF ===================="""

    def name(self):
        return "action_innovMF"

    def run(self, dispatcher, tracker, domain):
        print("action_innovMF is running inside class innovMF")
        innovsmmodelno = str(tracker.get_slot('qc_check_report_slot'))
        try:
            url = "http://127.0.0.1:5000/"
  
            value= {"Model_Name": innovsmmodelno}    
            response = requests.post(url, value)
            
            if response.status_code != 200:   
                print(response.status_code)
            else:
                json_data = response.json()
                print("Json data response for Innov8 json_data", json_data)
            #     for each in json_data:
            #         print("each data = ", each['QC_Completed'])
            #         if str(each['QC_Completed']) == 'NO':
            #             qcNotCompletedCount = qcNotCompletedCount+1
            #         if str(each['QC_Completed']) == 'yes':
            #             qcCompletedCount = qcCompletedCount+1
            #     # qcNotCompletedCountVar = qcNotCompletedCount
            #     # qcCompletedCountVar = qcCompletedCount
            # print("Not completed QC check count = ", qcNotCompletedCountVar)
            # print("Completed QC check count = ", qcCompletedCountVar)                      
            # dispatcher.utter_template(
            #     "utter_esi_forge_get_completed_and_notcompleted_qc_check_count_template", tracker, qcNotCompletedCountVar = qcNotCompletedCountVar+str(qcNotCompletedCount), qcCompletedCountVar = qcCompletedCountVar+str(qcCompletedCount)
            # )
            print(
                "class innovMF  is working successfully"
            )
        except Exception as e:
            dispatcher.utter_message("Sorry for the inconvenience")
            print("Exception: ",e) 

#=====================


            
def API_GetPhoneDataByID(dispatcher,modelNo):
    print("API Calling Method")
    try:
        url = 
        user = 
        passwd =   
        value= {"Product_Model_Name": modelNo}    
        response = requests.post(url, data=json.dumps(value), auth=HTTPBasicAuth(user, passwd))
        return response
    except Exception as e:
        dispatcher.utter_message("Technical Error While Calling API")
        print("Exception: ",e)

        # ============================= SmartMF



def API_GetPhoneDataByID(dispatcher,modelNo):
    print("API Calling Method")
    try:
        url = 
        user = 
        passwd =    
        value= {"Product_Model_Name": modelNo}    
        response = requests.post(url, data=json.dumps(value), auth=HTTPBasicAuth(user, passwd))
        return response
    except Exception as e:
        dispatcher.utter_message("Technical Error While Calling API")
        print("Exception: ",e)

class ModelNoForm(FormAction):
    """Example of a custom form action"""

    def name(self):
        """Unique identifier of the form"""
        return "modelno_form"

    @staticmethod
    def required_slots(tracker: Tracker) -> List[Text]:
        return ["modelNo"]

    def slot_mappings(self) -> Dict[Text, Union[Dict, List[Dict]]]:
        return {"modelNo":[self.from_entity(entity="ProductModelNo"),self.from_text(not_intent=["stop"])]}

    def validate_modelNo(
        self,
        value: Text,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> Optional[Text]:
            try:
                if value == 'stop':
                    intent= tracker.latest_message["intent"].get("name")
                    if intent == "stop":
                        return [self.deactivate(), FollowupAction('action_slot_cancel')]
                else:
                    update_value = value.upper()
                    print(update_value)
                    return {'modelNo': update_value}
            except Exception as e:
                # print(e.message)
                # print ("Error: IndexError")
                # print(e.message)
                dispatcher.utter_message("Provide input in proper format.")
    
    def submit(self,dispatcher: CollectingDispatcher,tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict]:
        return[]

class QC_Verify(Action):
    def name(self):
        return 'action_QC_Verify'
    def run(self, dispatcher, tracker, domain):
        print("QC Verification Class")
        model_no = (next(tracker.get_latest_entity_values("ProductModelNo"), None))
        model_no = str(model_no).upper()
        print("Product Model Number: ",model_no)        
        slot_value = tracker.get_slot("modelNo")
        print("Slot Value is: ", slot_value)
        if model_no is None and slot_value is None:
            dispatcher.utter_template("utter_ask_modelNo",tracker)
        else:
            try:
                if slot_value is None:
                    response = API_GetPhoneDataByID(dispatcher,model_no) #### Here i have to pass the model number
                else:
                    response = API_GetPhoneDataByID(dispatcher,slot_value)
                #print("response: ",response)
                if response.status_code != 200:
                    dispatcher.utter_message("API Status Not Equal to 200")
                else:
                    try:
                        json_data = response.json()
                        print("Json Data: ",json_data[0]["QC_Verified"])
                        result = json_data[0]["QC_Verified"]
                        if result == 'false':
                            dispatcher.utter_message("QC verification is not done for this product")
                        else:
                            dispatcher.utter_message("QC verification is completed for this product")
                    except Exception as e:
                        dispatcher.utter_message(json_data[0]["Producr_Model_Name"])
                        dispatcher.utter_message("Model Number Not Present or Data Not present")
                        print("Exception: ", e)
            except Exception as e:
                dispatcher.utter_message("provide valid product_name")
                print("Exception: ", e)
                dispatcher.utter_template("utter_ask_modelNo",tracker)
        return [SlotSet("modelNo",None)]


class QC_Check_Count(Action):
    def name(self):
        return 'action_QC_Check'
    def run(self, dispatcher, tracker, domain):
        print("QC Check Count Class")
        model_no = (next(tracker.get_latest_entity_values("ProductModelNo"), None))
        model_no = str(model_no).upper()
        print("Product Model Number: ",model_no)
        print("Slot Value is: ", tracker.get_slot("modelNo"))
        slot_value = tracker.get_slot("modelNo")
        if model_no is None and slot_value is None:
            dispatcher.utter_template("utter_ask_modelNo",tracker)
        else:
            if slot_value is None:
                response = API_GetPhoneDataByID(dispatcher,model_no) #### Here i have to pass the model number
            else:
                response = API_GetPhoneDataByID(dispatcher,slot_value)
            try:
                if response.status_code != 200:
                    dispatcher.utter_message("API Status Not Equal to 200")
                else:
                    try:
                        json_data = response.json()
                        result = json_data[0]["QC_Count"]
                        result_msg = "The QC check count is "+ str(result)[:-2]
                        dispatcher.utter_message(result_msg)
                    except Exception as e:
                        dispatcher.utter_message(json_data[0]["Product_Model_Name"])
                        print("Exception: ",e)
            except Exception as e:
                dispatcher.utter_message("provide valid product_name")
                print("Exception: ", e)
                dispatcher.utter_template("utter_ask_modelNo",tracker)
        return [SlotSet("modelNo",None)]

class QC_EmployeeDetails(Action):
    def name(self):
        return 'action_QC_EmployeeDetails'
    def run(self, dispatcher, tracker, domain):
        print("QC Employee Details Class")
        model_no = (next(tracker.get_latest_entity_values("ProductModelNo"), None))
        model_no = str(model_no).upper()
        print("Product Model Number: ",model_no)
        print("Slot Value is: ", tracker.get_slot("modelNo"))
        slot_value = tracker.get_slot("modelNo")
        if model_no is None and slot_value is None:
            dispatcher.utter_template("utter_ask_modelNo",tracker)
        else:
            if slot_value is None:
                response = API_GetPhoneDataByID(dispatcher,model_no) #### Here i have to pass the model number
            else:
                response = API_GetPhoneDataByID(dispatcher,slot_value)
            try:
                if response.status_code != 200:
                    dispatcher.utter_message("API Status Not Equal to 200")
                else:
                    try:
                        json_data = response.json()
                        result = "EmployeeID: "+str(json_data[0]["QC_EmployeeID"])+" EmployeeName: "+str(json_data[0]["QC_EmployeeName"])
                        dispatcher.utter_message(result)
                    except Exception as e:
                        dispatcher.utter_message(json_data[0]["Producr_Model_Name"])
                        print("Exception: ",e)
            except Exception as e:
                dispatcher.utter_message("provide valid product_name")
                print("Exception: ", e)
                dispatcher.utter_template("utter_ask_modelNo",tracker)
        return [SlotSet("modelNo",None)]

class QC_Date(Action):
    def name(self):
        return 'action_QC_Date'
    def run(self, dispatcher, tracker, domain):
        print("QC Date Class")
        model_no = (next(tracker.get_latest_entity_values("ProductModelNo"), None))
        print("Product Model Number: ",model_no)
        model_no = str(model_no).upper()
        print("Slot Value is: ", tracker.get_slot("modelNo"))
        slot_value = tracker.get_slot("modelNo")
        if model_no is None and slot_value is None:
            dispatcher.utter_template("utter_ask_modelNo",tracker)
        else:
            if slot_value is None:
                response = API_GetPhoneDataByID(dispatcher,model_no) #### Here i have to pass the model number
            else:
                response = API_GetPhoneDataByID(dispatcher,slot_value)
            try:
                if response.status_code != 200:
                    dispatcher.utter_message("API Status Not Equal to 200")
                else:
                    try:
                        json_data = response.json()
                        result = json_data[0]["CreatedDate"]
                        value = result[0:9]
                        dispatcher.utter_message("StartDate: "+value[6:8]+"-"+value[4:6]+"-"+value[0:4])
                    except Exception as e:
                        dispatcher.utter_message(json_data[0]["Product_Model_Name"])
                        print("Exception: ",e)
            except Exception as e:
                dispatcher.utter_message("provide valid product_name")
                print("Exception: ", e)
                dispatcher.utter_template("utter_ask_modelNo",tracker)
        return [SlotSet("modelNo",None)]

class ActionDefaultAskAffirmation(Action):
    """Asks for an affirmation of the intent if NLU threshold is not met."""

    def name(self) -> Text:
        return "action_default_ask_affirmation"

    def __init__(self) -> None:
        import csv

        self.intent_mappings = {}
        with open('data/intent_description_mapping.csv',
                  newline='',
                  encoding='utf-8') as file:
            csv_reader = csv.reader(file)
            for row in csv_reader:
                self.intent_mappings[row[0]] = row[1]

    def run(self,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]
            ) -> List['Event']:

        intent_ranking = tracker.latest_message.get('intent_ranking', [])
        if len(intent_ranking) > 1:
            diff_intent_confidence = (intent_ranking[0].get("confidence") -
                                      intent_ranking[1].get("confidence"))
            if diff_intent_confidence < 0.2:
                intent_ranking = intent_ranking[:2]
            else:
                intent_ranking = intent_ranking[:1]
        first_intent_names = [intent.get('name', '')
                              for intent in intent_ranking
                              if intent.get('name', '') != 'out_of_scope']

        message_title = "Sorry, I'm not sure I've understood " \
                        "you correctly 🤔 Do you mean..."

        mapped_intents = [(name, self.intent_mappings.get(name, name))
                          for name in first_intent_names]

        entities = tracker.latest_message.get("entities", [])
        entities_json, entities_text = get_formatted_entities(entities)

        buttons = []
        for intent in mapped_intents:
            buttons.append({'title': intent[1],
                            'payload': '/{}{}'.format(str(intent[0]),
                                                      str(entities_json))})
        print("Button: ",buttons)
        buttons.append({'title': 'Something else',
                        'payload': '/out_of_scope'})

        dispatcher.utter_button_message(message_title, buttons=buttons)

        return []

def get_formatted_entities(entities: List[Dict[str, Any]]) -> (Text, Text):
    key_value_entities = {}
    for e in entities:
        key_value_entities[e.get("entity")] = e.get("value")
    entities_json = ""
    entities_text = ""
    if len(entities) > 0:
        entities_json = json.dumps(key_value_entities)
        entities_text = ["'{}': '{}'".format(k, key_value_entities[k])
                         for k in key_value_entities]
        entities_text = ", ".join(entities_text)
        entities_text = " ({})".format(entities_text)

    return str(entities_json), str(entities_text)
