import json, os
import copy
from inspect import signature # For detect count of def args
from . import __Orchestrator__
#ControlPanelDict
from desktopmagic.screengrab_win32 import (
	getDisplayRects, saveScreenToBmp, saveRectToBmp, getScreenAsImage,
	getRectAsImage, getDisplaysAsImages)
from http import cookies
import uuid # generate UUID4
import time # sleep functions
import datetime # datetime functions
import threading # Multi-threading
from .Web import Basic
from . import BackwardCompatibility # Support old up to 1.2.0 defs
from . import Processor
from . import SettingsTemplate
# # # # # # # # # # # #
# v 1.2.0 Functionallity
# # # # # # # # # # # #
# Generate JS when page init
def HiddenJSInitGenerate(inRequest, inGSettings):
    dUAC = inRequest.UACClientCheck # Alias.
    lUACCPTemplateKeyList=["pyOpenRPADict","CPKeyDict"]
    lL = inGSettings["Logger"] # Alias for logger
    lJSInitResultStr = ""
    lRenderFunctionsRobotDict = inGSettings["CPDict"]
    for lItemKeyStr in lRenderFunctionsRobotDict:
        lItemDict = lRenderFunctionsRobotDict[lItemKeyStr]
        lJSInitGeneratorDef = lItemDict.get("JSInitGeneratorDef",None)
        lUACBool = dUAC(inRoleKeyList=lUACCPTemplateKeyList+[lItemKeyStr]) # Check if render function is applicable User Access Rights (UAC)
        if lItemKeyStr=="VersionCheck": lUACBool=True # For backward compatibility for the old fron version which not reload page when new orch version is comming
        if lUACBool: # Run function if UAC is TRUE
            # JSONGeneratorDef
            if lJSInitGeneratorDef is not None: # Call def (inRequest, inGSettings) or def (inGSettings)
                lJSResult = None
                lDEFSignature = signature(lJSInitGeneratorDef) # Get signature of the def
                lDEFARGLen = len(lDEFSignature.parameters.keys()) # get count of the def args
                try:
                    if lDEFARGLen == 1: # def (inGSettings)
                        lJSResult = lJSInitGeneratorDef(inGSettings)
                    elif lDEFARGLen == 2: # def (inRequest, inGSettings)
                        lJSResult = lJSInitGeneratorDef(inRequest, inGSettings)
                    elif lDEFARGLen == 0: # def ()
                        lJSResult = lJSInitGeneratorDef()
                    if type(lJSResult) is str:
                        lJSInitResultStr += "; "+lJSResult # Add delimiter to some cases
                    else:
                        if lL: lL.warning(f"JSInitGenerator return bad type: {str(type(lJSResult))}, CP Key {lItemKeyStr}")
                except Exception as e:
                    if lL: lL.exception(f"Error in control panel JSInitGeneratorDef. CP Key {lItemKeyStr}. Exception are below")
    return lJSInitResultStr

# Generate CP HTML + JSON
# Return {"Key":{"",""}}
def HiddenCPDictGenerate(inRequest, inGSettings):
    dUAC = inRequest.UACClientCheck # Alias.
    lUACCPTemplateKeyList=["pyOpenRPADict","CPKeyDict"]
    lL = inGSettings["Logger"] # Alias for logger
    # Create result JSON
    lCPDict = {}
    lRenderFunctionsRobotDict = inGSettings["CPDict"]
    for lItemKeyStr in lRenderFunctionsRobotDict:
        lItemDict = lRenderFunctionsRobotDict[lItemKeyStr]
        lItemHTMLRenderDef = lItemDict.get("HTMLRenderDef",None)
        lItemJSONGeneratorDef = lItemDict.get("JSONGeneratorDef",None)
        lUACBool = dUAC(inRoleKeyList=lUACCPTemplateKeyList+[lItemKeyStr]) # Check if render function is applicable User Access Rights (UAC)
        if lItemKeyStr=="VersionCheck": lUACBool=True # For backward compatibility for the old fron version which not reload page when new orch version is comming
        if lUACBool: # Run function if UAC is TRUE
            lCPItemDict = {"HTMLStr": None, "JSONDict":None}
            # HTMLRenderDef
            if lItemHTMLRenderDef is not None: # Call def (inRequest, inGSettings) or def (inGSettings)
                lHTMLResult = None
                lDEFSignature = signature(lItemHTMLRenderDef) # Get signature of the def
                lDEFARGLen = len(lDEFSignature.parameters.keys()) # get count of the def args
                try:
                    if lDEFARGLen == 1: # def (inGSettings)
                        lHTMLResult = lItemHTMLRenderDef(inGSettings)
                    elif lDEFARGLen == 2: # def (inRequest, inGSettings)
                        lHTMLResult = lItemHTMLRenderDef(inRequest, inGSettings)
                    elif lDEFARGLen == 0: # def ()
                        lHTMLResult = lItemHTMLRenderDef()
                    # RunFunction
                    # Backward compatibility up to 1.2.0 - call HTML generator if result has no "HTMLStr"
                    if type(lHTMLResult) is str:
                        lCPItemDict["HTMLStr"] = lHTMLResult
                    elif "HTMLStr" in lHTMLResult or "JSONDict" in lHTMLResult:
                        lCPItemDict = lHTMLResult # new version
                    else:
                        # Call backward compatibility HTML generator
                        lCPItemDict["HTMLStr"] = Basic.HTMLControlPanelBC(inCPDict=lHTMLResult)
                except Exception as e:
                    if lL: lL.exception(f"Error in control panel HTMLRenderDef. CP Key {lItemKeyStr}. Exception are below")
            # JSONGeneratorDef
            if lItemJSONGeneratorDef is not None: # Call def (inRequest, inGSettings) or def (inGSettings)
                lJSONResult = None
                lDEFSignature = signature(lItemJSONGeneratorDef) # Get signature of the def
                lDEFARGLen = len(lDEFSignature.parameters.keys()) # get count of the def args
                try:
                    if lDEFARGLen == 1: # def (inGSettings)
                        lJSONResult = lItemJSONGeneratorDef(inGSettings)
                    elif lDEFARGLen == 2: # def (inRequest, inGSettings)
                        lJSONResult = lItemJSONGeneratorDef(inRequest, inGSettings)
                    elif lDEFARGLen == 0: # def ()
                        lJSONResult = lItemJSONGeneratorDef()
                    # RunFunction
                    # Backward compatibility up to 1.2.0 - call HTML generator if result has no "HTMLStr"
                    lType = type(lJSONResult)
                    if lType is str or lJSONResult is None or lType is int or lType is list or lType is dict or lType is bool or lType is float:
                        lCPItemDict["JSONDict"] = lJSONResult
                    else:
                        if lL: lL.warning(f"JSONGenerator return bad type: {str(type(lJSONResult))}, CP Key {lItemKeyStr}")
                except Exception as e:
                    if lL: lL.exception(f"Error in control panel JSONGeneratorDef. CP Key {lItemKeyStr}. Exception are below")
            # Insert CPItemDict in result CPDict
            lCPDict[lItemKeyStr]=lCPItemDict
    return lCPDict

# Return {"Key":{"",""}}
def HiddenRDPDictGenerate(inRequest, inGSettings):
    dUAC = inRequest.UACClientCheck # Alias.
    lUACRDPTemplateKeyList=["pyOpenRPADict","RDPKeyDict"]
    lRDPDict = {"HandlebarsList":[]}
    # Iterate throught the RDP list
    for lRDPSessionKeyStrItem in inGSettings["RobotRDPActive"]["RDPList"]:
        # Check UAC
        if dUAC(inRoleKeyList=lUACRDPTemplateKeyList+[lRDPSessionKeyStrItem]):
            lRDPConfiguration = inGSettings["RobotRDPActive"]["RDPList"][
                lRDPSessionKeyStrItem]  # Get the configuration dict
            lDataItemDict = {"SessionKeyStr": "", "SessionHexStr": "", "IsFullScreenBool": False,
                             "IsIgnoredBool": False}  # Template
            lDataItemDict["SessionKeyStr"] = lRDPSessionKeyStrItem  # Session key str
            lDataItemDict["SessionHexStr"] = lRDPConfiguration["SessionHex"]  # Session Hex
            lDataItemDict["IsFullScreenBool"] = True if lRDPSessionKeyStrItem == inGSettings["RobotRDPActive"][
                "FullScreenRDPSessionKeyStr"] else False  # Check  the full screen for rdp window
            lDataItemDict["IsIgnoredBool"] = lRDPConfiguration["SessionIsIgnoredBool"]  # Is ignored
            lRDPDict[lDataItemDict["SessionKeyStr"]]=lDataItemDict
            lHandlebarsDataItemDict = copy.deepcopy(lDataItemDict)
            lHandlebarsDataItemDict["SessionKeyStr"]=lDataItemDict["SessionKeyStr"]
            lRDPDict["HandlebarsList"].append(lHandlebarsDataItemDict)
    return lRDPDict

# Return {"HostNameUpperStr;UserUpperStr":{"IsListenBool":True}, "HandlebarsList":[{"HostnameUpperStr":"","UserUpperStr":"","IsListenBool":True}]}
def HiddenAgentDictGenerate(inRequest, inGSettings):
    dUAC = inRequest.UACClientCheck # Alias.
    lUACAgentTemplateKeyList=["pyOpenRPADict","AgentKeyDict"]
    lAgentDict = {"HandlebarsList":[]}
    # Iterate throught the RDP list
    for lAgentItemKeyStrItem in inGSettings["AgentDict"]:
        # Check UAC
        lKeyStr = f"{lAgentItemKeyStrItem[0]};{lAgentItemKeyStrItem[1]}" # turple ("HostNameUpperStr","UserUpperStr") > Str "HostNameUpperStr;UserUpperStr"
        if dUAC(inRoleKeyList=lUACAgentTemplateKeyList+[lKeyStr]):
            lDataItemDict = inGSettings["AgentDict"][lAgentItemKeyStrItem]
            lAgentDict[lKeyStr]=lDataItemDict
            lHandlebarsDataItemDict = copy.deepcopy(lDataItemDict)
            lHandlebarsDataItemDict["HostnameUpperStr"]=lAgentItemKeyStrItem[0]
            lHandlebarsDataItemDict["UserUpperStr"]=lAgentItemKeyStrItem[1]
            lAgentDict["HandlebarsList"].append(lHandlebarsDataItemDict)
    return lAgentDict


#v1.2.0 Send data container to the client from the server
# /pyOpenRPA/ServerData return {"HashStr" , "ServerDataDict": {"CPKeyStr":{"HTMLStr":"", DataDict:{}}}}

# Client: mGlobal.pyOpenRPA.ServerDataHashStr
# Client: mGlobal.pyOpenRPA.ServerDataDict
def pyOpenRPA_ServerData(inRequest,inGSettings):

    # Extract the hash value from request
    lValueStr = None
    if inRequest.headers.get('Content-Length') is not None:
        lInputByteArrayLength = int(inRequest.headers.get('Content-Length'))
        lInputByteArray = inRequest.rfile.read(lInputByteArrayLength)
        # Превращение массива байт в объект
        lValueStr = (lInputByteArray.decode('utf8'))
    # Generate ServerDataDict
    lFlagDoGenerateBool = True
    while lFlagDoGenerateBool:
        lServerDataDict = {
            "CPDict": HiddenCPDictGenerate(inRequest=inRequest, inGSettings=inGSettings),
            "RDPDict": HiddenRDPDictGenerate(inRequest=inRequest, inGSettings=inGSettings),
            "AgentDict": HiddenAgentDictGenerate(inRequest=inRequest, inGSettings=inGSettings),
            "UserDict": {"UACClientDict": inRequest.OpenRPA["DefUserRoleHierarchyGet"](), "CWDPathStr": os.getcwd(), "VersionStr": inGSettings["VersionStr"]},
        }
        # Create JSON
        lServerDataDictJSONStr = json.dumps(lServerDataDict)
        # Generate hash
        lServerDataHashStr = str(hash(lServerDataDictJSONStr))
        if lValueStr!=lServerDataHashStr and lServerDataHashStr!= "" and lServerDataHashStr!= None: # Case if Hash is not equal
            lFlagDoGenerateBool = False
        else: # Case Hashes are equal
            time.sleep(inGSettings["Client"]["Session"]["ControlPanelRefreshIntervalSecFloat"])
    # Return the result if Hash is changed
    lResult = {"HashStr": lServerDataHashStr, "ServerDataDict": lServerDataDict}
    inResponseDict = inRequest.OpenRPAResponseDict
    # Send message back to client
    message = json.dumps(lResult)
    # Write content as utf-8 data
    inResponseDict["Body"] = bytes(message, "utf8")
    return lResult

# GET
# /pyOpenRPA/ServerJSInit return JavaScript to init on page
def pyOpenRPA_ServerJSInit(inRequest,inGSettings):
    lResultStr = HiddenJSInitGenerate(inRequest=inRequest, inGSettings=inGSettings)
    inResponseDict = inRequest.OpenRPAResponseDict
    # Write content as utf-8 data
    inResponseDict["Body"] = bytes(lResultStr, "utf8")

#v1.2.0 Send data container to the client from the server
# /pyOpenRPA/ServerLog return {"HashStr" , "ServerLogList": ["row 1", "row 2"]}
# Client: mGlobal.pyOpenRPA.ServerLogListHashStr
# Client: mGlobal.pyOpenRPA.ServerLogList
def pyOpenRPA_ServerLog(inRequest,inGSDict):
    # Extract the hash value from request
    lValueStr = None
    if inRequest.headers.get('Content-Length') is not None:
        lInputByteArrayLength = int(inRequest.headers.get('Content-Length'))
        lInputByteArray = inRequest.rfile.read(lInputByteArrayLength)
        # Превращение массива байт в объект
        lValueStr = (lInputByteArray.decode('utf8'))
    # Generate ServerDataDict
    lFlagDoGenerateBool = True
    while lFlagDoGenerateBool:
        lServerLogList = inGSDict["Client"]["DumpLogList"]
        # Get hash
        lServerLogListHashStr = inGSDict["Client"]["DumpLogListHashStr"]
        if lValueStr!=lServerLogListHashStr and lServerLogListHashStr!= "" and lServerLogListHashStr!= None: # Case if Hash is not equal Fix because None can be obtained without JSON decode
            lFlagDoGenerateBool = False
        else: # Case Hashes are equal
            time.sleep(inGSDict["Client"]["DumpLogListRefreshIntervalSecFloat"])
    # Return the result if Hash is changed
    lResult = {"HashStr": lServerLogListHashStr, "ServerLogList": lServerLogList}
    inResponseDict = inRequest.OpenRPAResponseDict
    # Send message back to client
    message = json.dumps(lResult)
    # Write content as utf-8 data
    inResponseDict["Body"] = bytes(message, "utf8")
    return lResult

def pyOpenRPA_Screenshot(inRequest,inGlobalDict):
    # Get Screenshot
    def SaveScreenshot(inFilePath):
        # grab fullscreen
        # Save the entire virtual screen as a PNG
        lScreenshot = getScreenAsImage()
        lScreenshot.save('screenshot.png', format='png')
        # lScreenshot = ScreenshotSecondScreen.grab_screen()
        # save image file
        # lScreenshot.save('screenshot.png')
    # Сохранить файл на диск
    SaveScreenshot("Screenshot.png")
    lFileObject = open("Screenshot.png", "rb")
    # Write content as utf-8 data
    inRequest.OpenRPAResponseDict["Body"] = lFileObject.read()
    # Закрыть файловый объект
    lFileObject.close()
# Add activity item or activity list to the processor queue
# Body is Activity item or Activity List
def pyOpenRPA_Processor(inRequest, inGSettings):
    lL = inGSettings["Logger"]
    # Recieve the data
    lValueStr = None
    if inRequest.headers.get('Content-Length') is not None:
        lInputByteArrayLength = int(inRequest.headers.get('Content-Length'))
        lInputByteArray = inRequest.rfile.read(lInputByteArrayLength)
        # Превращение массива байт в объект
        lInput = json.loads(lInputByteArray.decode('utf8'))
    # If list - operator plus
    if type(lInput) is list:
        # Logging info about processor activity if not SuperToken ()
        if not __Orchestrator__.WebUserIsSuperToken(inRequest=inRequest, inGSettings=inGSettings):
            lActivityTypeListStr = ""
            try:
                for lActivityItem in lInput:
                    lActivityTypeListStr += f"{lActivityItem['Def']}; "
            except Exception as e:
                lActivityTypeListStr = "Has some error with Activity Type read"
            if lL: lL.info(f"ServerSettings.pyOpenRPA_Processor. User activity from web. Domain: {inRequest.OpenRPA['Domain']}, Username: {inRequest.OpenRPA['User']}, ActivityType: {lActivityTypeListStr}")
        # Append in list
        inGSettings["ProcessorDict"]["ActivityList"]+=lInput
    else:
        # Logging info about processor activity if not SuperToken ()
        if not __Orchestrator__.WebUserIsSuperToken(inRequest=inRequest, inGSettings=inGSettings):
            lActivityTypeListStr = ""
            try:
                lActivityTypeListStr = lInput['Def']
            except Exception as e:
                lActivityTypeListStr = "Has some error with Activity Type read"
            if lL: lL.info(f"ServerSettings.pyOpenRPA_Processor. User activity from web. Domain: {inRequest.OpenRPA['Domain']}, Username: {inRequest.OpenRPA['User']}, ActivityType: {lActivityTypeListStr}")
        # Append in list
        inGSettings["ProcessorDict"]["ActivityList"].append(lInput)
# Execute activity list
def pyOpenRPA_ActivityListExecute(inRequest, inGSettings):
    # Recieve the data
    lL = inGSettings["Logger"]
    lValueStr = None
    if inRequest.headers.get('Content-Length') is not None:
        lInputByteArrayLength = int(inRequest.headers.get('Content-Length'))
        lInputByteArray = inRequest.rfile.read(lInputByteArrayLength)
        # Превращение массива байт в объект
        lInput = json.loads(lInputByteArray.decode('utf8'))
    # If list - operator plus
    if type(lInput) is list:
        # Logging info about processor activity if not SuperToken ()
        if not __Orchestrator__.WebUserIsSuperToken(inRequest=inRequest, inGSettings=inGSettings):
            lActivityTypeListStr = ""
            try:
                for lActivityItem in lInput:
                    lActivityTypeListStr += f"{lActivityItem['Def']}; "
            except Exception as e:
                lActivityTypeListStr = "Has some error with Activity Type read"
            if lL: lL.info(f"ServerSettings.pyOpenRPA_ActivityListExecute. User activity from web. Domain: {inRequest.OpenRPA['Domain']}, Username: {inRequest.OpenRPA['User']}, ActivityType: {lActivityTypeListStr}")
        # Execution
        lResultList = Processor.ActivityListExecute(inGSettings = inGSettings, inActivityList = lInput)
        inRequest.OpenRPAResponseDict["Body"] = bytes(json.dumps(lResultList), "utf8")
    else:
        # Logging info about processor activity if not SuperToken ()
        if not __Orchestrator__.WebUserIsSuperToken(inRequest=inRequest, inGSettings=inGSettings):
            lActivityTypeListStr = ""
            try:
                lActivityTypeListStr = lInput['Def']
            except Exception as e:
                lActivityTypeListStr = "Has some error with Activity Type read"
            if lL: lL.info(f"ServerSettings.pyOpenRPA_ActivityListExecute. User activity from web. Domain: {inRequest.OpenRPA['Domain']}, Username: {inRequest.OpenRPA['User']}, ActivityType: {lActivityTypeListStr}")
        # Execution
        lResultList = Processor.ActivityListExecute(inGSettings = inGSettings, inActivityList = [lInput])
        inRequest.OpenRPAResponseDict["Body"] = bytes(json.dumps(lResultList[0]), "utf8")

# See docs in Agent (pyOpenRPA.Agent.O2A)
def pyOpenRPA_Agent_O2A(inRequest, inGSettings):
    lL = inGSettings["Logger"] # Alias
    lConnectionLifetimeSecFloat = 3600.0 # 60 min * 60 sec 3600.0
    lTimeStartFloat = time.time()
    # Recieve the data
    lValueStr = None
    if inRequest.headers.get('Content-Length') is not None:
        lInputByteArrayLength = int(inRequest.headers.get('Content-Length'))
        lInputByteArray = inRequest.rfile.read(lInputByteArrayLength)
        # Превращение массива байт в объект
        lInput = json.loads(lInputByteArray.decode('utf8'))
    # Check if item is created
    lAgentDictItemKeyTurple = (lInput["HostNameUpperStr"],lInput["UserUpperStr"])
    if lAgentDictItemKeyTurple not in inGSettings["AgentDict"]:
        inGSettings["AgentDict"][lAgentDictItemKeyTurple] = SettingsTemplate.__AgentDictItemCreate__()
    lThisAgentDict = inGSettings["AgentDict"][lAgentDictItemKeyTurple]
    lThisAgentDict["IsListenBool"]=True # Set is online
    lThisAgentDict["ConnectionCountInt"] += 1  # increment connection count
    # Test solution
    lDoLoopBool = True
    while lDoLoopBool:
        # Check if lifetime is over
        if time.time() - lTimeStartFloat > lConnectionLifetimeSecFloat: # Lifetime is over
            lThisAgentDict["IsListenBool"] = False  # Set is offline
            lDoLoopBool = False
        else: # Lifetime is good - do alg
            lThisAgentDict["IsListenBool"] = True  # Set is online
            lQueueList = lThisAgentDict["ActivityList"]
            if len(lQueueList)>0:# Do some operations if has queue items
                if lL: lL.debug(f'O2A BEFORE: ConnectionCountInt: {lThisAgentDict["ConnectionCountInt"]};ConnectionFirstQueueItemCountInt {lThisAgentDict["ConnectionFirstQueueItemCountInt"]}')
                if lThisAgentDict["ConnectionCountInt"] == lThisAgentDict["ConnectionFirstQueueItemCountInt"] + 1:
                    # POP QUEUE ITEM CONDITION ConnectionCountInt == ConnectionFirstQueueItemCountInt + 1
                    lActivityItem = lThisAgentDict["ActivityList"].pop(0)
                    lThisAgentDict["ConnectionFirstQueueItemCountInt"] = 0
                    if lL: lL.debug(f"Activity was deleted from the list: {lThisAgentDict['ActivityList']}")
                else:
                    lActivityItem = lThisAgentDict["ActivityList"][0]
                    lThisAgentDict["ConnectionFirstQueueItemCountInt"] += 1
                    if lL: lL.debug(f"Activity was !not! deleted from the list: {lThisAgentDict['ActivityList']}")
                if lL: lL.debug(f'O2A AFTER: ConnectionCountInt: {lThisAgentDict["ConnectionCountInt"]};ConnectionFirstQueueItemCountInt {lThisAgentDict["ConnectionFirstQueueItemCountInt"]}')
                # Send QUEUE ITEM
                if lL: lL.info(f"Activity item to agent Hostname {lInput['HostNameUpperStr']}, User {lInput['UserUpperStr']}. Activity item: {lActivityItem}")
                inRequest.OpenRPAResponseDict["Body"] = bytes(json.dumps(lActivityItem), "utf8")
                lDoLoopBool = False # CLose the connection
            else: # no queue item - sleep for the next iteration
                time.sleep(1)
    lThisAgentDict["ConnectionCountInt"] -= 1  # Connection go to be closed - decrement the connection count
# See docs in Agent (pyOpenRPA.Agent.A2O)
def pyOpenRPA_Agent_A2O(inRequest, inGSettings):
    # Recieve the data
    lValueStr = None
    if inRequest.headers.get('Content-Length') is not None:
        lInputByteArrayLength = int(inRequest.headers.get('Content-Length'))
        lInputByteArray = inRequest.rfile.read(lInputByteArrayLength)
        # Превращение массива байт в объект
        lInput = json.loads(lInputByteArray.decode('utf8'))
    if "LogList" in lInput:
        for lLogItemStr in lInput["LogList"]:
            inGSettings["Logger"].info(lLogItemStr)

def SettingsUpdate(inGlobalConfiguration):
    import os
    import pyOpenRPA.Orchestrator
    lOrchestratorFolder = "\\".join(pyOpenRPA.Orchestrator.__file__.split("\\")[:-1])
    lURLList = \
        [ #List of available URLs with the orchestrator server
            #{
            #    "Method":"GET|POST",
            #    "URL": "/index", #URL of the request
            #    "MatchType": "", #"BeginWith|Contains|Equal|EqualCase",
            #    "ResponseFilePath": "", #Absolute or relative path
            #    "ResponseFolderPath": "", #Absolute or relative path
            #    "ResponseContentType": "", #HTTP Content-type
            #    "ResponseDefRequestGlobal": None #Function with str result
            #}
            #Orchestrator basic dependencies
            {"Method":"GET", "URL": "/", "MatchType": "EqualCase", "ResponseFilePath": os.path.join(lOrchestratorFolder, "Web\\Index.xhtml"), "ResponseContentType": "text/html"},
            {"Method":"GET", "URL": "/Index.js", "MatchType": "EqualCase", "ResponseFilePath": os.path.join(lOrchestratorFolder, "Web\\Index.js"), "ResponseContentType": "text/javascript"},
            {"Method":"GET", "URL": "/3rdParty/Semantic-UI-CSS-master/semantic.min.css", "MatchType": "EqualCase", "ResponseFilePath": os.path.join(lOrchestratorFolder, "..\\Resources\\Web\\Semantic-UI-CSS-master\\semantic.min.css"), "ResponseContentType": "text/css"},
            {"Method":"GET", "URL": "/3rdParty/Semantic-UI-CSS-master/semantic.min.js", "MatchType": "EqualCase", "ResponseFilePath": os.path.join(lOrchestratorFolder, "..\\Resources\\Web\\Semantic-UI-CSS-master\\semantic.min.js"), "ResponseContentType": "application/javascript"},
            {"Method":"GET", "URL": "/3rdParty/jQuery/jquery-3.1.1.min.js", "MatchType": "EqualCase", "ResponseFilePath": os.path.join(lOrchestratorFolder, "..\\Resources\\Web\\jQuery\\jquery-3.1.1.min.js"), "ResponseContentType": "application/javascript"},
            {"Method":"GET", "URL": "/3rdParty/Google/LatoItalic.css", "MatchType": "EqualCase", "ResponseFilePath": os.path.join(lOrchestratorFolder, "..\\Resources\\Web\\Google\\LatoItalic.css"), "ResponseContentType": "font/css"},
            {"Method":"GET", "URL": "/3rdParty/Semantic-UI-CSS-master/themes/default/assets/fonts/icons.woff2", "MatchType": "EqualCase", "ResponseFilePath": os.path.join(lOrchestratorFolder, "..\\Resources\\Web\\Semantic-UI-CSS-master\\themes\\default\\assets\\fonts\\icons.woff2"), "ResponseContentType": "font/woff2"},
            {"Method":"GET", "URL": "/favicon.ico", "MatchType": "EqualCase", "ResponseFilePath": os.path.join(lOrchestratorFolder, "Web\\favicon.ico"), "ResponseContentType": "image/x-icon"},
            {"Method":"GET", "URL": "/3rdParty/Handlebars/handlebars-v4.1.2.js", "MatchType": "EqualCase", "ResponseFilePath": os.path.join(lOrchestratorFolder, "..\\Resources\\Web\\Handlebars\\handlebars-v4.1.2.js"), "ResponseContentType": "application/javascript"},
            {"Method": "GET", "URL": "/Monitor/ControlPanelDictGet", "MatchType": "Equal", "ResponseDefRequestGlobal": BackwardCompatibility.v1_2_0_Monitor_ControlPanelDictGet_SessionCheckInit, "ResponseContentType": "application/json"},
            {"Method": "GET", "URL": "/GetScreenshot", "MatchType": "BeginWith", "ResponseDefRequestGlobal": pyOpenRPA_Screenshot, "ResponseContentType": "image/png"},
            {"Method": "GET", "URL": "/pyOpenRPA_logo.png", "MatchType": "Equal", "ResponseFilePath": os.path.join(lOrchestratorFolder, "..\\Resources\\Web\\pyOpenRPA_logo.png"), "ResponseContentType": "image/png"},
            {"Method": "POST", "URL": "/Orchestrator/UserRoleHierarchyGet", "MatchType": "Equal","ResponseDefRequestGlobal": BackwardCompatibility.v1_2_0_UserRoleHierarchyGet, "ResponseContentType": "application/json"},
            # New way of the v.1.2.0 functionallity (all defs by the URL from /pyOpenRPA/...)
            {"Method": "POST", "URL": "/pyOpenRPA/ServerData", "MatchType": "Equal","ResponseDefRequestGlobal": pyOpenRPA_ServerData, "ResponseContentType": "application/json"},
            {"Method": "GET", "URL": "/pyOpenRPA/ServerJSInit", "MatchType": "Equal","ResponseDefRequestGlobal": pyOpenRPA_ServerJSInit, "ResponseContentType": "application/javascript"},
            {"Method": "POST", "URL": "/pyOpenRPA/ServerLog", "MatchType": "Equal","ResponseDefRequestGlobal": pyOpenRPA_ServerLog, "ResponseContentType": "application/json"},
            {"Method": "GET", "URL": "/pyOpenRPA/Screenshot", "MatchType": "BeginWith", "ResponseDefRequestGlobal": pyOpenRPA_Screenshot, "ResponseContentType": "image/png"},
            {"Method": "POST", "URL": "/pyOpenRPA/ProcessorQueueAdd", "MatchType": "Equal","ResponseDefRequestGlobal": pyOpenRPA_Processor, "ResponseContentType": "application/json"},
            {"Method": "POST", "URL": "/pyOpenRPA/ActivityListExecute", "MatchType": "Equal","ResponseDefRequestGlobal": pyOpenRPA_ActivityListExecute, "ResponseContentType": "application/json"},
            {"Method": "POST", "URL": "/pyOpenRPA/Agent/O2A", "MatchType": "Equal","ResponseDefRequestGlobal": pyOpenRPA_Agent_O2A, "ResponseContentType": "application/json"},
            {"Method": "POST", "URL": "/pyOpenRPA/Agent/A2O", "MatchType": "Equal","ResponseDefRequestGlobal": pyOpenRPA_Agent_A2O, "ResponseContentType": "application/json"},
    ]
    inGlobalConfiguration["ServerDict"]["URLList"]=inGlobalConfiguration["ServerDict"]["URLList"]+lURLList
    return inGlobalConfiguration