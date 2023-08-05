# 1.2.0 - general processor - contains old orchestrator processor + RDPActive processor
import time, copy, threading
# Run processor synchronious
# inThreadControlDict = {"ThreadExecuteBool":True}
def ProcessorRunSync(inGSettings, inRobotRDPThreadControlDict):
    """
        "ProcessorDict": { # Has been changed. New general processor (one threaded) v.1.2.0
            "ActivityList": [ # List of the activities
                # {
                #    "Def":"DefAliasTest", # def link or def alias (look gSettings["Processor"]["AliasDefDict"])
                #    "ArgList":[1,2,3], # Args list
                #    "ArgDict":{"ttt":1,"222":2,"dsd":3}, # Args dictionary
                #    "ArgGSettings": None # Name of GSettings attribute: str (ArgDict) or index (for ArgList)
                #    "ArgLogger": None # Name of GSettings attribute: str (ArgDict) or index (for ArgList)
                # },
            ],
            "AliasDefDict": {}, # Storage for def with Str alias. To use it see pyOpenRPA.Orchestrator.ControlPanel
            "CheckIntervalSecFloat": 1.0 # Interval for check gSettings in ProcessorDict > ActivityList
            "ExecuteBool": True # Flag to execute thread processor
    """
    lL = inGSettings["Logger"]  # Logger alias
    inGSettings["ProcessorDict"]["ThreadIdInt"] = threading.get_ident() # fill Processor thread id
    while inGSettings["ProcessorDict"]["ExecuteBool"]:
        lActivityList = inGSettings["ProcessorDict"]["ActivityList"] # Alias
        if len(lActivityList)>0:
            if lL: lL.debug(f'Processor ActivityList len: {len(lActivityList)}')
            lActivityItem = inGSettings["ProcessorDict"]["ActivityList"].pop(0) # Extract the first item from processor queue
            inRobotRDPThreadControlDict["ThreadExecuteBool"]=False # Stop the RobotRDPActive monitoring
            ActivityListExecute(inGSettings = inGSettings, inActivityList = [lActivityItem]) # execute the activity item
            inRobotRDPThreadControlDict["ThreadExecuteBool"] = True  # Continue the RobotRDPActive monitoring
        else:
            time.sleep(inGSettings["ProcessorDict"]["CheckIntervalSecFloat"]) # Sleep when list is empty

# Execute ActivityItem list
# return the def result
def ActivityListExecute(inGSettings, inActivityList):
    lL = inGSettings["Logger"]  # Logger alias
    lResultList = [] # init the result list
    try:
        for lActivityItem in inActivityList:  # Iterate throught the activity list
            if lL: lL.info(f'pyOpenRPA Processor.ActivityListExecute:: Def:{str(lActivityItem["Def"])}. Parameters are not available to see.')
            lDef = None  # Def variable
            if callable(lActivityItem["Def"]):  # CHeck if def is callable
                lDef = lActivityItem["Def"]  # Get the def
            else:  # Is not callable - check alias
                lDef = inGSettings["ProcessorDict"]["AliasDefDict"].get(lActivityItem["Def"], None)  # get def if def key in Alias def storage
            #gSettings
            lGSettingsDictKey = lActivityItem.pop("ArgGSettings",None)
            # # Prepare arg dict - gSettings
            if type(lGSettingsDictKey) is str  and lGSettingsDictKey is not "": # check if gSetting key is in ArgDict 13.02.2021 - Fix when ArgGSettings is ""
                lActivityItem["ArgDict"][lGSettingsDictKey] = inGSettings # Set the gSettings in dict
            # # Prepare arg list
            elif type(lGSettingsDictKey) is int: # check if gSetting key is in ArgDict
                lActivityItem["ArgList"].insert(lGSettingsDictKey,inGSettings)# Set the gSettings in list by the index
            #Logger
            lLoggerDictKey = lActivityItem.pop("ArgLogger",None)
            # # Prepare arg dict - Logger
            if type(lLoggerDictKey) is str and lLoggerDictKey is not "": # check if gSetting key is in ArgDict 13.02.2021 - Fix when ArgLogger is ""
                lActivityItem["ArgDict"][lLoggerDictKey] = lL # Set the lLogger in dict
            # # Prepare arg list
            elif type(lLoggerDictKey) is int: # check if gSetting key is in ArgDict
                lActivityItem["ArgList"].insert(lLoggerDictKey,lL)# Set the lLogger in list by the index

            try:  # try to run function from Processor.py
                lActivityItemResult = lDef(*lActivityItem["ArgList"], **lActivityItem["ArgDict"])
                lResultList.append(lActivityItemResult) # return the result
            except Exception as e:
                if lL: lL.exception(f"pyOpenRPA Processor.ActivityListExecute: Exception in def execution - activity will be ignored.")  # Logging
                lResultList.append(e) # return the generated exception
    except Exception as e:
        if lL: lL.exception(f"pyOpenRPA Processor.ActivityListExecute: Exception when initialisation - All activity list will be ignored.")  # Logging
    return lResultList # return the result list

def __ActivityListVerify__(inActivityList):
    """
    Verify ActivityList variable - raise exception if input list is not list of dict with structure:
        #    "Def":"DefAliasTest", # def link or def alias (look gSettings["Processor"]["AliasDefDict"])
        #    "ArgList":[1,2,3], # Args list
        #    "ArgDict":{"ttt":1,"222":2,"dsd":3}, # Args dictionary
        #    "ArgGSettings": None # Name of GSettings attribute: str (ArgDict) or index (for ArgList)
        #    "ArgLogger": None # Name of GSettings attribute: str (ArgDict) or index (for ArgList)

    :param inActivityList:
    :return:
    """
    # CASE LIST
    if type(inActivityList) is list:
        for lItem in inActivityList:
            # CASE LIST item is LIST
            if type(lItem) is list:
                raise Exception(f"pyOpenRPA Processor.__ActivityListVerify__: inActivityList has wrong structure! Details: Your ActivityList item is list too. List of the list :(")
            # CASE Item is not dict
            if type(lItem) is not dict:
                raise Exception(f"pyOpenRPA Processor.__ActivityListVerify__: inActivityList has wrong structure! Details: Your ActivityList item is is not dict")
            # CASE HAS NO "Def"
            if "Def" not in lItem:
                raise Exception(f"pyOpenRPA Processor.__ActivityListVerify__: inActivityList has wrong structure! Details: Activity item has no attribute 'Def'")
    #CASE NOT LIST
    else:
        raise Exception(f"pyOpenRPA Processor.__ActivityListVerify__: inActivityList has wrong structure! Details: Your ActivityList is not a list.")