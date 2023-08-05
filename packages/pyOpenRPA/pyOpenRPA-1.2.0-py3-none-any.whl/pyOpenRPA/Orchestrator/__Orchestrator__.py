import subprocess, json, psutil, time, os, win32security, sys, base64, logging, ctypes #Get input argument
from . import Server
from . import Timer
from . import Processor
from . import BackwardCompatibility # Backward compatibility from v1.1.13
from . import Core
from .Utils import LoggerHandlerDumpLogList

# ATTENTION! HERE IS NO Relative import because it will be imported dynamically
# All function check the flag SessionIsWindowResponsibleBool == True else no cammand is processed
# All functions can return None, Bool or Dict { "IsSuccessful": True }
from .RobotRDPActive import CMDStr # Create CMD Strings
from .RobotRDPActive import Connector # RDP API

#from .Settings import Settings
import importlib
from importlib import util
import threading # Multi-threading for RobotRDPActive
from .RobotRDPActive import RobotRDPActive #Start robot rdp active
from .RobotScreenActive import Monitor #Start robot screen active
from . import SettingsTemplate # Settings template
import uuid # Generate uuid
import datetime # datetime

#Единый глобальный словарь (За основу взять из Settings.py)
global gSettingsDict

# AGENT DEFS

def AgentActivityItemAdd(inGSettings, inHostNameStr, inUserStr, inActivityItemDict):
    """
    Add activity in AgentDict. Check if item is created

    :param inGSettings: Global settings dict (singleton)
    :param inHostNameStr: Agent host name
    :param inUserStr: User login, where agent is based
    :param inActivityItemDict: ActivityItem
    :return: None
    """
    lAgentDictItemKeyTurple = (inHostNameStr.upper(),inUserStr.upper())
    if lAgentDictItemKeyTurple not in inGSettings["AgentDict"]:
        inGSettings["AgentDict"][lAgentDictItemKeyTurple] = SettingsTemplate.__AgentDictItemCreate__()
    lThisAgentDict = inGSettings["AgentDict"][lAgentDictItemKeyTurple]
    lThisAgentDict["ActivityList"].append(inActivityItemDict)


def AgentOSCMD(inGSettings, inHostNameStr, inUserStr, inCMDStr, inRunAsyncBool=True):
    """
    Send CMD to OS thought the pyOpenRPA.Agent daemon. Result return to log + Orchestrator by the A2O connection

    :param inGSettings: Global settings dict (singleton)
    :param inHostNameStr:
    :param inUserStr:
    :param inCMDStr:
    :param inRunAsyncBool:
    """
    lActivityItemDict = {
        "Def":"OSCMD", # def alias (look pyOpeRPA.Agent gSettings["ProcessorDict"]["AliasDefDict"])
        "ArgList":[], # Args list
        "ArgDict":{"inCMDStr":inCMDStr,"inRunAsyncBool":inRunAsyncBool}, # Args dictionary
        "ArgGSettings": "inGSettings", # Name of GSettings attribute: str (ArgDict) or index (for ArgList)
        "ArgLogger": None # Name of GSettings attribute: str (ArgDict) or index (for ArgList)
    }
    #Send item in AgentDict for the futher data transmition
    AgentActivityItemAdd(inGSettings=inGSettings, inHostNameStr=inHostNameStr, inUserStr=inUserStr, inActivityItemDict=lActivityItemDict)

def AgentOSFileBinaryDataBytesCreate(inGSettings, inHostNameStr, inUserStr, inFilePathStr, inFileDataBytes):
    """
    Create binary file by the base64 string by the pyOpenRPA.Agent daemon process (safe for JSON transmition)

    :param inGSettings: Global settings dict (singleton)
    :param inHostNameStr:
    :param inUserStr:
    :param inFilePathStr:
    :param inFileDataBytes:
    """

    lFileDataBase64Str = base64.b64encode(inFileDataBytes).decode("utf-8")
    lActivityItemDict = {
        "Def":"OSFileBinaryDataBase64StrCreate", # def alias (look pyOpeRPA.Agent gSettings["ProcessorDict"]["AliasDefDict"])
        "ArgList":[], # Args list
        "ArgDict":{"inFilePathStr":inFilePathStr,"inFileDataBase64Str":lFileDataBase64Str}, # Args dictionary
        "ArgGSettings": "inGSettings", # Name of GSettings attribute: str (ArgDict) or index (for ArgList)
        "ArgLogger": None # Name of GSettings attribute: str (ArgDict) or index (for ArgList)
    }
    #Send item in AgentDict for the futher data transmition
    AgentActivityItemAdd(inGSettings=inGSettings, inHostNameStr=inHostNameStr, inUserStr=inUserStr, inActivityItemDict=lActivityItemDict)


def AgentOSFileBinaryDataBase64StrCreate(inGSettings, inHostNameStr, inUserStr, inFilePathStr, inFileDataBase64Str):
    """
    Create binary file by the base64 string by the pyOpenRPA.Agent daemon process (safe for JSON transmission)

    :param inGSettings: Global settings dict (singleton)
    :param inHostNameStr:
    :param inUserStr:
    :param inFilePathStr:
    :param inFileDataBase64Str:
    """

    lActivityItemDict = {
        "Def":"OSFileBinaryDataBase64StrCreate", # def alias (look pyOpeRPA.Agent gSettings["ProcessorDict"]["AliasDefDict"])
        "ArgList":[], # Args list
        "ArgDict":{"inFilePathStr":inFilePathStr,"inFileDataBase64Str":inFileDataBase64Str}, # Args dictionary
        "ArgGSettings": "inGSettings", # Name of GSettings attribute: str (ArgDict) or index (for ArgList)
        "ArgLogger": None # Name of GSettings attribute: str (ArgDict) or index (for ArgList)
    }
    #Send item in AgentDict for the futher data transmition
    AgentActivityItemAdd(inGSettings=inGSettings, inHostNameStr=inHostNameStr, inUserStr=inUserStr, inActivityItemDict=lActivityItemDict)

# Send text file to Agent (string)
def AgentOSFileTextDataStrCreate(inGSettings, inHostNameStr, inUserStr, inFilePathStr, inFileDataStr, inEncodingStr = "utf-8"):
    """
    Create text file by the string by the pyOpenRPA.Agent daemon process

    :param inGSettings: Global settings dict (singleton)
    :param inHostNameStr:
    :param inUserStr:
    :param inFilePathStr:
    :param inFileDataStr:
    :param inEncodingStr:
    """

    lActivityItemDict = {
        "Def":"OSFileTextDataStrCreate", # def alias (look pyOpeRPA.Agent gSettings["ProcessorDict"]["AliasDefDict"])
        "ArgList":[], # Args list
        "ArgDict":{"inFilePathStr":inFilePathStr,"inFileDataStr":inFileDataStr, "inEncodingStr": inEncodingStr}, # Args dictionary
        "ArgGSettings": "inGSettings", # Name of GSettings attribute: str (ArgDict) or index (for ArgList)
        "ArgLogger": None # Name of GSettings attribute: str (ArgDict) or index (for ArgList)
    }
    #Send item in AgentDict for the futher data transmition
    AgentActivityItemAdd(inGSettings=inGSettings, inHostNameStr=inHostNameStr, inUserStr=inUserStr, inActivityItemDict=lActivityItemDict)

# OS DEFS
def OSCredentialsVerify(inUserStr, inPasswordStr, inDomainStr=""): ##
    """
    Verify user credentials in windows. Return bool

    :param inUserStr:
    :param inPasswordStr:
    :param inDomainStr:
    :return: True - Credentials are actual; False - Credentials are not actual
    """
    try:
        hUser = win32security.LogonUser(
            inUserStr,inDomainStr, inPasswordStr,
            win32security.LOGON32_LOGON_NETWORK, win32security.LOGON32_PROVIDER_DEFAULT
        )
    except win32security.error:
        return False
    else:
        return True

def OSCMD(inCMDStr, inRunAsyncBool=True, inLogger = None):
    """
    OS send command in shell locally

    :param inCMDStr:
    :param inRunAsyncBool:
    :param inLogger:
    :return: CMD result string
    """
    lResultStr = ""
    # Subdef to listen OS result
    def _CMDRunAndListenLogs(inCMDStr, inLogger):
        lResultStr = ""
        lOSCMDKeyStr = str(uuid.uuid4())[0:4].upper()
        lCMDProcess = subprocess.Popen(f'cmd /c {inCMDStr}', stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        if inLogger:
            lListenBool = True
            inLogger.info(f"{lOSCMDKeyStr}: # # # # CMD Process has been STARTED # # # # ")
            inLogger.info(f"{lOSCMDKeyStr}: {inCMDStr}")
            while lListenBool:
                lOutputLineBytes = lCMDProcess.stdout.readline()
                if lOutputLineBytes == b"":
                    lListenBool = False
                lStr = lOutputLineBytes.decode('cp866')
                if lStr.endswith("\n"): lStr = lStr[:-1]
                inLogger.info(f"{lOSCMDKeyStr}: {lStr}")
                lResultStr+=lStr
            inLogger.info(f"{lOSCMDKeyStr}: # # # # CMD Process has been FINISHED # # # # ")
        return lResultStr
    # New call
    if inRunAsyncBool:
        lThread = threading.Thread(target=_CMDRunAndListenLogs, kwargs={"inCMDStr":inCMDStr, "inLogger":inLogger})
        lThread.start()
        lResultStr="ActivityList has been started in async mode - no output is available here."
    else:
        lResultStr = _CMDRunAndListenLogs(inCMDStr=inCMDStr, inLogger=inLogger)
    #lCMDCode = "cmd /c " + inCMDStr
    #subprocess.Popen(lCMDCode)
    #lResultCMDRun = 1  # os.system(lCMDCode)
    return lResultStr

def OrchestratorRestart(inGSettings=None):
    """
    Orchestrator restart

    :param inGSettings: Global settings dict (singleton)
    """
    OrchestratorSessionSave(inGSettings=inGSettings) # Dump RDP List in file json
    if inGSettings is not None:
        lL = inGSettings["Logger"]
        if lL: lL.info(f"Do restart")
    # Restart session
    os.execl(sys.executable, os.path.abspath(__file__), *sys.argv)
    sys.exit(0)

def OrchestratorSessionSave(inGSettings=None):
    """
    Orchestrator session save in file _SessionLast_RDPList.json (encoding = "utf-8")

    :param inGSettings: Global settings dict (singleton)
    :return: True every time
    """
    # Dump RDP List in file json
    lFile = open("_SessionLast_RDPList.json", "w", encoding="utf-8")
    lFile.write(json.dumps(inGSettings["RobotRDPActive"]["RDPList"]))  # dump json to file
    lFile.close()  # Close the file
    if inGSettings is not None:
        lL = inGSettings["Logger"]
        if lL: lL.info(
            f"Orchestrator has dump the RDP list before the restart.")
    return True

def UACKeyListCheck(inRequest, inRoleKeyList) -> bool:
    """
    Check is client is has access for the key list

    :param inRequest:
    :param inRoleKeyList:
    :return: bool
    """
    return inRequest.UACClientCheck(inRoleKeyList=inRoleKeyList)

def UACUpdate(inGSettings, inADLoginStr, inADStr="", inADIsDefaultBool=True, inURLList=None, inRoleHierarchyAllowedDict=None):
    """
    Update user access (UAC)

    :param inGSettings: Global settings dict (singleton)
    :param inADLoginStr:
    :param inADStr:
    :param inADIsDefaultBool:
    :param inURLList:
    :param inRoleHierarchyAllowedDict:
    """
    lUserTurple = (inADStr.upper(),inADLoginStr.upper()) # Create turple key for inGSettings["ServerDict"]["AccessUsers"]["RuleDomainUserDict"]
    if inURLList is None: inURLList = [] # Check if None
    if inRoleHierarchyAllowedDict is None: inRoleHierarchyAllowedDict = {} # Check if None
    # Get the old URLList
    try:
        inURLList += inGSettings["ServerDict"]["AccessUsers"]["RuleDomainUserDict"][lUserTurple]["MethodMatchURLBeforeList"]
    except:
        pass
    # Check RoleHierarchyAllowedDict in gSettings for the old role hierarchy - include in result.
    if lUserTurple in inGSettings["ServerDict"]["AccessUsers"]["RuleDomainUserDict"] and "RoleHierarchyAllowedDict" in inGSettings["ServerDict"]["AccessUsers"]["RuleDomainUserDict"][lUserTurple]:
        lRoleHierarchyAllowedOLDDict = inGSettings["ServerDict"]["AccessUsers"]["RuleDomainUserDict"][lUserTurple]["RoleHierarchyAllowedDict"]
        Server.__ComplexDictMerge2to1__(in1Dict=inRoleHierarchyAllowedDict, in2Dict=lRoleHierarchyAllowedOLDDict) # Merge dict 2 into dict 1

    # Create Access item
    lRuleDomainUserDict = {
        "MethodMatchURLBeforeList": inURLList,
        "RoleHierarchyAllowedDict": inRoleHierarchyAllowedDict
    }
    # Case add domain + user
    inGSettings["ServerDict"]["AccessUsers"]["RuleDomainUserDict"].update({(inADStr.upper(),inADLoginStr.upper()):lRuleDomainUserDict})
    if inADIsDefaultBool:
        # Case add default domain + user
        inGSettings["ServerDict"]["AccessUsers"]["RuleDomainUserDict"].update({("",inADLoginStr.upper()):lRuleDomainUserDict})

def UACSuperTokenUpdate(inGSettings, inSuperTokenStr):
    """
    Add supertoken for the all access (it is need for the robot communication without human)

    :param inGSettings: Global settings dict (singleton)
    :param inSuperTokenStr:
    """
    lLoginStr = "SUPERTOKEN"
    UACUpdate(inGSettings=inGSettings, inADLoginStr=lLoginStr)
    inGSettings["ServerDict"]["AccessUsers"]["AuthTokensDict"].update(
        {inSuperTokenStr:{"User":lLoginStr, "Domain":"", "TokenDatetime":  datetime.datetime.now(), "FlagDoNotExpire":True}}
    )

# # # # # # # # # # # # # # # # # # # # # # #
# OrchestratorWeb defs
# # # # # # # # # # # # # # # # # # # # # # #


def WebURLConnectDef(inGSettings, inMethodStr, inURLStr, inMatchTypeStr, inDef, inContentTypeStr="application/octet-stream"):
    """
     Connect URL to DEF
        "inMethodStr":"GET|POST",
        "inURLStr": "/index", #URL of the request
        "inMatchTypeStr": "", #"BeginWith|Contains|Equal|EqualCase",
        "inContentTypeStr": "", #HTTP Content-type
        "inDef": None #Function with str result

    :param inGSettings: Global settings dict (singleton)
    :param inMethodStr:
    :param inURLStr:
    :param inMatchTypeStr:
    :param inDef:
    :param inContentTypeStr:
    """
    lURLItemDict = {
        "Method": inMethodStr.upper(),
        "URL": inURLStr,  # URL of the request
        "MatchType": inMatchTypeStr,  # "BeginWith|Contains|Equal|EqualCase",
        # "ResponseFilePath": "", #Absolute or relative path
        #"ResponseFolderPath": "C:\Abs\Archive\scopeSrcUL\OpenRPA\Orchestrator\Settings",
        # Absolute or relative path
        "ResponseContentType": inContentTypeStr, #HTTP Content-type
        "ResponseDefRequestGlobal": inDef #Function with str result
    }
    inGSettings["ServerDict"]["URLList"].append(lURLItemDict)


def WebURLConnectFolder(inGSettings, inMethodStr, inURLStr, inMatchTypeStr, inFolderPathStr):
    """
    Connect URL to Folder
        "inMethodStr":"GET|POST",
        "inURLStr": "/Folder/", #URL of the request
        "inMatchTypeStr": "", #"BeginWith|Contains|Equal|EqualCase",
        "inFolderPathStr": "", #Absolute or relative path

    :param inGSettings: Global settings dict (singleton)
    :param inMethodStr:
    :param inURLStr:
    :param inMatchTypeStr:
    :param inFolderPathStr:
    """
    # Check if last symbol is "/" - append if not exist
    lFolderPathStr = os.path.abspath(inFolderPathStr)
    if lFolderPathStr[-1]!="/":lFolderPathStr+="/"
    # Prepare URLItem
    lURLItemDict = {
        "Method": inMethodStr.upper(),
        "URL": inURLStr,  # URL of the request
        "MatchType": inMatchTypeStr,  # "BeginWith|Contains|Equal|EqualCase",
        # "ResponseFilePath": "", #Absolute or relative path
        "ResponseFolderPath": lFolderPathStr, # Absolute or relative path
        "ResponseContentType": "application/octet-stream", #HTTP Content-type
        #"ResponseDefRequestGlobal": inDef #Function with str result
    }
    inGSettings["ServerDict"]["URLList"].append(lURLItemDict)


def WebURLConnectFile(inGSettings, inMethodStr, inURLStr, inMatchTypeStr, inFilePathStr, inContentTypeStr="application/octet-stream"):
    """
    Connect URL to File
        "inMethodStr":"GET|POST",
        "inURLStr": "/index", #URL of the request
        "inMatchTypeStr": "", #"BeginWith|Contains|Equal|EqualCase",
        "inFolderPathStr": "", #Absolute or relative path

    :param inGSettings: Global settings dict (singleton)
    :param inMethodStr:
    :param inURLStr:
    :param inMatchTypeStr:
    :param inFilePathStr:
    :param inContentTypeStr:
    """
    lURLItemDict = {
        "Method": inMethodStr.upper(),
        "URL": inURLStr,  # URL of the request
        "MatchType": inMatchTypeStr,  # "BeginWith|Contains|Equal|EqualCase",
        "ResponseFilePath": os.path.abspath(inFilePathStr), #Absolute or relative path
        #"ResponseFolderPath": os.path.abspath(inFilePathStr), # Absolute or relative path
        "ResponseContentType": inContentTypeStr, #HTTP Content-type
        #"ResponseDefRequestGlobal": inDef #Function with str result
    }
    inGSettings["ServerDict"]["URLList"].append(lURLItemDict)

def WebCPUpdate(inGSettings, inCPKeyStr, inHTMLRenderDef=None, inJSONGeneratorDef=None, inJSInitGeneratorDef=None):
    """
    Add control panel HTML, JSON generator or JS when page init

    :param inGSettings: Global settings dict (singleton)
    :param inCPKeyStr:
    :param inHTMLRenderDef:
    :param inJSONGeneratorDef:
    :param inJSInitGeneratorDef:
    """
    # Create Struct if the re is current key
    if inCPKeyStr not in inGSettings["CPDict"]:
        inGSettings["CPDict"][inCPKeyStr] = {"HTMLRenderDef": None,"JSONGeneratorDef": None, "JSInitGeneratorDef": None}
    # CASE HTMLRender
    if inHTMLRenderDef is not None:
        inGSettings["CPDict"][inCPKeyStr]["HTMLRenderDef"]=inHTMLRenderDef
    # CASE JSONGenerator
    if inJSONGeneratorDef is not None:
        inGSettings["CPDict"][inCPKeyStr]["JSONGeneratorDef"] = inJSONGeneratorDef
    # CASE JSInitGeneratorDef
    if inJSInitGeneratorDef is not None:
        inGSettings["CPDict"][inCPKeyStr]["JSInitGeneratorDef"] = inJSInitGeneratorDef

def WebUserInfoGet(inRequest):
    """
    Return User info about request

    :param inRequest:
    :return: {"DomainUpperStr": "", "UserNameUpperStr": ""}
    """
    lDomainUpperStr = inRequest.OpenRPA["Domain"].upper()
    lUserUpperStr = inRequest.OpenRPA["User"].upper()
    return {"DomainUpperStr": lDomainUpperStr, "UserNameUpperStr": lUserUpperStr}

def WebUserIsSuperToken(inRequest, inGSettings):
    """
    Return bool if request is authentificated with supetoken (token which is never expires)

    :param inRequest:
    :param inGSettings: Global settings dict (singleton)
    :return: bool True - is supertoken; False - is not supertoken
    """
    lIsSuperTokenBool = False
    # Get Flag is supertoken (True|False)
    lIsSuperTokenBool = inGSettings.get("ServerDict", {}).get("AccessUsers", {}).get("AuthTokensDict", {}).get(inRequest.OpenRPA["AuthToken"], {}).get("FlagDoNotExpire", False)
    return lIsSuperTokenBool

def WebUserUACHierarchyGet(inRequest):
    """
    Return User UAC Hierarchy DICT Return {...}

    :param inRequest:
    :return: UAC Dict {}
    """
    return inRequest.UserRoleHierarchyGet()

## GSettings defs
def GSettingsKeyListValueSet(inGSettings, inValue, inKeyList=None):
    """
    Set value in GSettings by the key list

    :param inGSettings: Global settings dict (singleton)
    :param inValue:
    :param inKeyList:
    :return: bool
    """
    if inKeyList is None: inKeyList = []
    lDict = inGSettings
    for lItem2 in inKeyList[:-1]:
        #Check if key - value exists
        if lItem2 in lDict:
            pass
        else:
            lDict[lItem2]={}
        lDict=lDict[lItem2]
    lDict[inKeyList[-1]] = inValue #Set value
    return True

def GSettingsKeyListValueGet(inGSettings, inKeyList=None):
    """
    Get the value from the GSettings by the key list

    :param inGSettings: Global settings dict (singleton)
    :param inKeyList:
    :return: value any type
    """
    if inKeyList is None: inKeyList = []
    lDict = inGSettings
    for lItem2 in inKeyList[:-1]:
        #Check if key - value exists
        if lItem2 in lDict:
            pass
        else:
            lDict[lItem2]={}
        lDict=lDict[lItem2]
    return lDict.get(inKeyList[-1],None)

def GSettingsKeyListValueAppend(inGSettings, inValue, inKeyList=None):
    """
    Append value in GSettings by the key list

    .. code-block:: python

        # USAGE
        from pyOpenRPA import Orchestrator

        Orchestrator.GSettingsKeyListValueAppend(
            inGSettings = gSettings,
            inValue = "NewValue",
            inKeyList=["NewKeyDict","NewKeyList"]):
        # result inGSettings: {
        #    ... another keys in gSettings ...,
        #    "NewKeyDict":{
        #        "NewKeyList":[
        #            "NewValue"
        #        ]
        #    }
        #}

    :param inGSettings: Global settings dict (singleton)
    :param inValue: Any value to be appended in gSettings Dict by the key list
    :param inKeyList: List of the nested keys (see example)
    :return: True every time
    """
    if inKeyList is None: inKeyList = []
    lDict = inGSettings
    for lItem2 in inKeyList[:-1]:
        #Check if key - value exists
        if lItem2 in lDict:
            pass
        else:
            lDict[lItem2]={}
        lDict=lDict[lItem2]
    lDict[inKeyList[-1]].append(inValue) #Set value
    return True

def GSettingsKeyListValueOperatorPlus(inGSettings, inValue, inKeyList=None):
    """
    Execute plus operation between 2 lists (1:inValue and 2:gSettings by the inKeyList)

    .. code-block:: python

        # USAGE
        from pyOpenRPA import Orchestrator

        Orchestrator.GSettingsKeyListValueOperatorPlus(
            inGSettings = gSettings,
            inValue = [1,2,3],
            inKeyList=["NewKeyDict","NewKeyList"]):
        # result inGSettings: {
        #    ... another keys in gSettings ...,
        #    "NewKeyDict":{
        #        "NewKeyList":[
        #            "NewValue",
        #            1,
        #            2,
        #            3
        #        ]
        #    }
        #}

    :param inGSettings: Global settings dict (singleton)
    :param inValue: List with values to be merged with list in gSettings
    :param inKeyList: List of the nested keys (see example)
    :return: True every time
    """
    if inKeyList is None: inKeyList = []
    lDict = inGSettings
    for lItem2 in inKeyList[:-1]:
        #Check if key - value exists
        if lItem2 in lDict:
            pass
        else:
            lDict[lItem2]={}
        lDict=lDict[lItem2]
    lDict[inKeyList[-1]] += inValue #Set value
    return True

def ProcessorAliasDefCreate(inGSettings, inDef, inAliasStr=None):
    """
    Create alias for def (can be used in ActivityItem in field Def)
    !WHEN DEF ALIAS IS REQUIRED! - Def alias is required when you try to call Python def from the Orchestrator WEB side (because you can't transmit Python def object out of the Python environment)

    .. code-block:: python

        # USAGE
        from pyOpenRPA import Orchestrator

        def TestDef():
            pass
        lAliasStr = Orchestrator.ProcessorAliasDefCreate(
            inGSettings = gSettings,
            inDef = TestDef,
            inAliasStr="TestDefAlias")
        # Now you can call TestDef by the alias from var lAliasStr with help of ActivityItem (key Def = lAliasStr)

    :param inGSettings: Global settings dict (singleton)
    :param inDef: Def
    :param inAliasStr: String alias for associated def
    :return: str Alias string (Alias can be regenerated if previous alias was occupied)
    """
    #TODO Pay attention - New alias can be used too - need to create more complex algorythm to create new alias!
    lL = inGSettings["Logger"]
    if inAliasStr is None: inAliasStr = str(inDef)
    # Check if key is not exists
    if inAliasStr in inGSettings["ProcessorDict"]["AliasDefDict"]:
        inAliasStr = str(inDef)
        if lL: lL.warning(f"Orchestrator.ProcessorAliasDefCreate: Alias {inAliasStr} already exists in alias dictionary. Another alias will be generated and returned")
    inGSettings["ProcessorDict"]["AliasDefDict"][inAliasStr] = inDef
    return inAliasStr

def ProcessorAliasDefUpdate(inGSettings, inDef, inAliasStr):
    """
    Update alias for def (can be used in ActivityItem in field Def).
    !WHEN DEF ALIAS IS REQUIRED! - Def alias is required when you try to call Python def from the Orchestrator WEB side (because you can't transmit Python def object out of the Python environment)

    .. code-block:: python

        # USAGE
        from pyOpenRPA import Orchestrator

        def TestDef():
            pass
        Orchestrator.ProcessorAliasDefUpdate(
            inGSettings = gSettings,
            inDef = TestDef,
            inAliasStr="TestDefAlias")
        # Now you can call TestDef by the alias "TestDefAlias" with help of ActivityItem (key Def = "TestDefAlias")

    :param inGSettings: Global settings dict (singleton)
    :param inDef: Def
    :param inAliasStr: String alias for associated def
    :return: str Alias string
    """
    if callable(inDef): inGSettings["ProcessorDict"]["AliasDefDict"][inAliasStr] = inDef
    else: raise Exception(f"pyOpenRPA Exception: You can't use Orchestrator.ProcessorAliasDefUpdate with arg 'inDef' string value. inDef is '{inDef}', inAliasStr is '{inAliasStr}'")
    return inAliasStr

def ProcessorActivityItemCreate(inDef, inArgList=None, inArgDict=None, inArgGSettingsStr=None, inArgLoggerStr=None):
    """
    Create activity item. Activity item can be used as list item in ProcessorActivityItemAppend or in Processor.ActivityListExecute.

    .. code-block:: python

        # USAGE
        from pyOpenRPA import Orchestrator

        # EXAMPLE 1
        def TestDef(inArg1Str, inGSettings, inLogger):
            pass
        lActivityItem = Orchestrator.ProcessorActivityItemCreate(
            inDef = TestDef,
            inArgList=[],
            inArgDict={"inArg1Str": "ArgValueStr"},
            inArgGSettingsStr = "inGSettings",
            inArgLoggerStr = "inLogger")
        # lActivityItem:
        #   {
        #       "Def":TestDef,
        #       "ArgList":inArgList,
        #       "ArgDict":inArgDict,
        #       "ArgGSettings": "inArgGSettings",
        #       "ArgLogger": "inLogger"
        #   }

        # EXAMPLE 2
        def TestDef(inArg1Str):
            pass
        Orchestrator.ProcessorAliasDefUpdate(
            inGSettings = gSettings,
            inDef = TestDef,
            inAliasStr="TestDefAlias")
        lActivityItem = Orchestrator.ProcessorActivityItemCreate(
            inDef = "TestDefAlias",
            inArgList=[],
            inArgDict={"inArg1Str": "ArgValueStr"},
            inArgGSettingsStr = None,
            inArgLoggerStr = None)
        # lActivityItem:
        #   {
        #       "Def":"TestDefAlias",
        #       "ArgList":inArgList,
        #       "ArgDict":inArgDict,
        #       "ArgGSettings": None,
        #       "ArgLogger": None
        #   }

    :param inDef: def link or def alias (look gSettings["Processor"]["AliasDefDict"])
    :param inArgList: Args list for the Def
    :param inArgDict: Args dict for the def
    :param inArgGSettingsStr: Name of def argument of the GSettings dict
    :param inArgLoggerStr: Name of def argument of the logging object
    :return: {}
    """
    if inArgList is None: inArgList=[]
    if inArgDict is None: inArgDict={}
    lActivityItemDict= {
            "Def":inDef, # def link or def alias (look gSettings["Processor"]["AliasDefDict"])
            "ArgList":inArgList, # Args list
            "ArgDict":inArgDict, # Args dictionary
            "ArgGSettings": inArgGSettingsStr, # Name of GSettings attribute: str (ArgDict) or index (for ArgList)
            "ArgLogger": inArgLoggerStr # Name of GSettings attribute: str (ArgDict) or index (for ArgList)
        }
    return lActivityItemDict

def ProcessorActivityItemAppend(inGSettings, inDef=None, inArgList=None, inArgDict=None, inArgGSettingsStr=None, inArgLoggerStr=None, inActivityItemDict=None):
    """
    Create and add activity item in processor queue.

    .. code-block:: python

        # USAGE
        from pyOpenRPA import Orchestrator

        # EXAMPLE 1
        def TestDef(inArg1Str, inGSettings, inLogger):
            pass
        lActivityItem = Orchestrator.ProcessorActivityItemAppend(
            inGSettings = gSettingsDict,
            inDef = TestDef,
            inArgList=[],
            inArgDict={"inArg1Str": "ArgValueStr"},
            inArgGSettingsStr = "inGSettings",
            inArgLoggerStr = "inLogger")
        # Activity have been already append in the processor queue

        # EXAMPLE 2
        def TestDef(inArg1Str):
            pass
        Orchestrator.ProcessorAliasDefUpdate(
            inGSettings = gSettings,
            inDef = TestDef,
            inAliasStr="TestDefAlias")
        lActivityItem = Orchestrator.ProcessorActivityItemCreate(
            inDef = "TestDefAlias",
            inArgList=[],
            inArgDict={"inArg1Str": "ArgValueStr"},
            inArgGSettingsStr = None,
            inArgLoggerStr = None)
        Orchestrator.ProcessorActivityItemAppend(
            inGSettings = gSettingsDict,
            inActivityItemDict = lActivityItem)
        # Activity have been already append in the processor queue

    :param inGSettings: Global settings dict (singleton)
    :param inDef: def link or def alias (look gSettings["Processor"]["AliasDefDict"])
    :param inArgList: Args list for the Def
    :param inArgDict: Args dict for the Def
    :param inArgGSettingsStr: Name of def argument of the GSettings dict
    :param inArgLoggerStr: Name of def argument of the logging object
    :param inActivityItemDict: Fill if you already have ActivityItemDict (don't fill inDef, inArgList, inArgDict, inArgGSettingsStr, inArgLoggerStr)
    """
    if inActivityItemDict is None:
        if inArgList is None: inArgList=[]
        if inArgDict is None: inArgDict={}
        if inDef is None: raise Exception(f"pyOpenRPA Exception: ProcessorActivityItemAppend need inDef arg if you dont use inActivityItemDict")
        lActivityList=[
            {
                "Def":inDef, # def link or def alias (look gSettings["Processor"]["AliasDefDict"])
                "ArgList":inArgList, # Args list
                "ArgDict":inArgDict, # Args dictionary
                "ArgGSettings": inArgGSettingsStr, # Name of GSettings attribute: str (ArgDict) or index (for ArgList)
                "ArgLogger": inArgLoggerStr # Name of GSettings attribute: str (ArgDict) or index (for ArgList)
            }
        ]
    else:
        lActivityList = [inActivityItemDict]
    inGSettings["ProcessorDict"]["ActivityList"]+=lActivityList

## Process defs
def ProcessIsStarted(inProcessNameWOExeStr): # Check if process is started
    """
    Check if there is any running process that contains the given name processName.

    .. code-block:: python

        # USAGE
        from pyOpenRPA import Orchestrator

        lProcessIsStartedBool = Orchestrator.ProcessIsStarted(inProcessNameWOExeStr = "notepad")
        # lProcessIsStartedBool is True - notepad.exe is running on the Orchestrator machine

    :param inProcessNameWOExeStr: Process name WithOut (WO) '.exe' postfix. Example: "notepad" (not "notepad.exe")
    :return: True - process is running on the orchestrator machine; False - process is not running on the orchestrator machine
    """
    #Iterate over the all the running process
    for proc in psutil.process_iter():
        try:
            # Check if process name contains the given name string.
            if inProcessNameWOExeStr.lower() in proc.name().lower():
                return True
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass
    return False

def ProcessStart(inPathStr, inArgList, inStopProcessNameWOExeStr=None):
    """
    Start process locally. Extra feature: Use inStopProcessNameWOExeStr to stop the execution if current process is running.

    .. code-block:: python

        # USAGE
        from pyOpenRPA import Orchestrator

        Orchestrator.ProcessStart(
            inPathStr = "notepad"
            inArgList = []
            inStopProcessNameWOExeStr = "notepad")
        # notepad.exe will be started if no notepad.exe is active on the machine

    :param inPathStr: Command to send in CMD
    :param inArgList: List of the arguments for the CMD command. Example: ["test.txt"]
    :param inStopProcessNameWOExeStr: Trigger: stop execution if process is running. Process name WithOut (WO) '.exe' postfix. Example: "notepad" (not "notepad.exe")
    :return: None - nothing is returned. If process will not start -exception will be raised
    """
    lStartProcessBool = True
    if inStopProcessNameWOExeStr is not None: #Check if process running
        lCheckTaskName = inStopProcessNameWOExeStr
        if len(lCheckTaskName)>4:
            if lCheckTaskName[-4:].upper() != ".EXE":
                lCheckTaskName = lCheckTaskName+".exe"
        else:
            lCheckTaskName = lCheckTaskName+".exe"
        #Check if process exist
        if not ProcessIsStarted(inProcessNameWOExeStr=lCheckTaskName): lStartProcessBool=True

    if lStartProcessBool == True: # Start if flag is true
        lItemArgs=[inPathStr]
        if inArgList is None: inArgList = [] # 2021 02 22 Minor fix default value
        lItemArgs.extend(inArgList)
        subprocess.Popen(lItemArgs,shell=True)

def ProcessStop(inProcessNameWOExeStr, inCloseForceBool, inUserNameStr = "%username%"):
    """
    Stop process on the orchestrator machine. You can set user session on the machine and set flag about to force close process.

    .. code-block:: python

        # USAGE
        from pyOpenRPA import Orchestrator

        Orchestrator.ProcessStop(
            inProcessNameWOExeStr = "notepad"
            inCloseForceBool = True
            inUserNameStr = "USER_99")
        # Will close process "notepad.exe" on the user session "USER_99" (!ATTENTION! if process not exists no exceptions will be raised)

    :param inProcessNameWOExeStr: Process name WithOut (WO) '.exe' postfix. Example: "notepad" (not "notepad.exe")
    :param inCloseForceBool: True - do force close. False - send signal to safe close (!ATTENTION! - Safe close works only in orchestrator session. Win OS doens't allow to send safe close signal between GUI sessions)
    :param inUserNameStr: User name which is has current process to close. Default value is close process on the Orchestrator session
    :return: None
    """
    # Support input arg if with .exe
    lProcessNameWExeStr = inProcessNameWOExeStr
    if len(lProcessNameWExeStr) > 4:
        if lProcessNameWExeStr[-4:].upper() != ".EXE":
            lProcessNameWExeStr = lProcessNameWExeStr + ".exe"
    else:
        lProcessNameWExeStr = lProcessNameWExeStr + ".exe"
    # Flag Force
    lActivityCloseCommand = 'taskkill /im ' + lProcessNameWExeStr
    if inCloseForceBool == True:
        lActivityCloseCommand += " /F"
    # None - all users, %username% - current user, another str - another user
    if inUserNameStr is not None:
        lActivityCloseCommand += f' /fi "username eq {inUserNameStr}"'
    # Kill process
    os.system(lActivityCloseCommand)

def ProcessListGet(inProcessNameWOExeList=None):
    """
    Return process list on the orchestrator machine sorted by Memory Usage. You can determine the list of the processes you are interested - def will return the list about it.

    .. code-block:: python

        # USAGE
        from pyOpenRPA import Orchestrator

        lProcessList = Orchestrator.ProcessListGet()
        # Return the list of the process on the machine.
        # !ATTENTION! RUn orchestrator as administrator to get all process list on the machine.

    :param inProcessNameWOExeList:
    :return: {
    "ProcessWOExeList": ["notepad","..."],
    "ProcessWOExeUpperList": ["NOTEPAD","..."],
    "ProcessDetailList": [
        {
            'pid': 412,
            'username': "DESKTOP\\USER",
            'name': 'notepad.exe',
            'vms': 13.77767775,
            'NameWOExeUpperStr': 'NOTEPAD',
            'NameWOExeStr': "'notepad'"},
        {...}]

    """
    if inProcessNameWOExeList is None: inProcessNameWOExeList = []
    lMapUPPERInput = {} # Mapping for processes WO exe
    lResult = {"ProcessWOExeList":[], "ProcessWOExeUpperList":[],"ProcessDetailList":[]}
    # Create updated list for quick check
    lProcessNameWOExeList = []
    for lItem in inProcessNameWOExeList:
        if lItem is not None:
            lProcessNameWOExeList.append(f"{lItem.upper()}.EXE")
            lMapUPPERInput[f"{lItem.upper()}.EXE"]= lItem
    # Iterate over the list
    for proc in psutil.process_iter():
        try:
            # Fetch process details as dict
            pinfo = proc.as_dict(attrs=['pid', 'name', 'username'])
            pinfo['vms'] = proc.memory_info().vms / (1024 * 1024)
            pinfo['NameWOExeUpperStr'] = pinfo['name'][:-4].upper()
            # Add if empty inProcessNameWOExeList or if process in inProcessNameWOExeList
            if len(lProcessNameWOExeList)==0 or pinfo['name'].upper() in lProcessNameWOExeList:
                try: # 2021 02 22 Minor fix if not admin rights
                    pinfo['NameWOExeStr'] = lMapUPPERInput[pinfo['name'].upper()]
                except Exception as e:
                    pinfo['NameWOExeStr'] = pinfo['name'][:-4]
                lResult["ProcessDetailList"].append(pinfo) # Append dict to list
                lResult["ProcessWOExeList"].append(pinfo['NameWOExeStr'])
                lResult["ProcessWOExeUpperList"].append(pinfo['NameWOExeUpperStr'])
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
           pass
    return lResult

# Python def - start module function
def PythonStart(inModulePathStr, inDefNameStr, inArgList=None, inArgDict=None, inLogger = None):
    """
    Import module and run def in the Orchestrator process.

    .. note::

        Import module will be each time when PythonStart def will be called.

    .. code-block:: python

        # USAGE
        from pyOpenRPA import Orchestrator

        Orchestrator.PythonStart(
            inModulePathStr="ModuleToCall.py", # inModulePathStr: Working Directory\\ModuleToCall.py
            inDefNameStr="TestDef")
        # Import module in Orchestrator process and call def "TestDef" from module "ModuleToCall.py"

    :param inModulePathStr: Absolute or relative (working directory of the orchestrator process) path to the importing module .py
    :param inDefNameStr: Def name in module
    :param inArgList: List of the arguments for callable def
    :param inArgDict: Dict of the named arguments for callable def
    :param inLogger: Logger instance to log some information when PythonStart def is running
    :return: None
    """
    if inArgList is None: inArgList=[]
    if inArgDict is None: inArgDict={}
    try:
        lModule=importlib.import_module(inModulePathStr) #Подключить модуль для вызова
        lFunction=getattr(lModule,inDefNameStr) #Найти функцию
        return lFunction(*inArgList,**inArgDict)
    except Exception as e:
        if inLogger: inLogger.exception("Loop activity error: module/function not founded")

# # # # # # # # # # # # # # # # # # # # # # #
# Scheduler
# # # # # # # # # # # # # # # # # # # # # # #

def SchedulerActivityTimeAddWeekly(inGSettings, inTimeHHMMStr="23:55:", inWeekdayList=None, inActivityList=None):
    """
    Add activity item list in scheduler. You can set weekday list and set time when launch. Activity list will be executed at planned time/day.

    .. code-block:: python

        # USAGE
        from pyOpenRPA import Orchestrator

        # EXAMPLE 1
        def TestDef(inArg1Str):
            pass
        lActivityItem = Orchestrator.ProcessorActivityItemCreate(
            inDef = TestDef,
            inArgList=[],
            inArgDict={"inArg1Str": "ArgValueStr"},
            inArgGSettingsStr = None,
            inArgLoggerStr = None)
        Orchestrator.SchedulerActivityTimeAddWeekly(
            inGSettings = gSettingsDict,
            inTimeHHMMStr = "04:34",
            inWeekdayList=[2,3,4],
            inActivityList = [lActivityItem])
        # Activity will be executed at 04:34 Wednesday (2), thursday (3), friday (4)

    :param inGSettings: Global settings dict (singleton)
    :param inTimeHHMMStr: Activation time from "00:00" to "23:59". Example: "05:29"
    :param inWeekdayList: Week day list to initiate activity list. Use int from 0 (monday) to 6 (sunday) as list items. Example: [0,1,2,3,4]. Default value is everyday ([0,1,2,3,4,5,6])
    :param inActivityList: Activity list structure
    :return: None
    """
    if inWeekdayList is None: inWeekdayList=[0,1,2,3,4,5,6]
    if inActivityList is None: inActivityList=[]
    Processor.__ActivityListVerify__(inActivityList=inActivityList) # DO VERIFICATION FOR THE inActivityList
    lActivityTimeItemDict = {
        "TimeHH:MMStr": inTimeHHMMStr,  # Time [HH:MM] to trigger activity
        "WeekdayList": inWeekdayList, # List of the weekday index when activity is applicable, Default [1,2,3,4,5,6,7]
        "ActivityList": inActivityList,
        "GUID": None  #    # Will be filled in Orchestrator automatically - is needed for detect activity completion
    }
    inGSettings["SchedulerDict"]["ActivityTimeList"].append(lActivityTimeItemDict)

# # # # # # # # # # # # # # # # # # # # # # #
# RDPSession
# # # # # # # # # # # # # # # # # # # # # # #

def RDPTemplateCreate(inLoginStr, inPasswordStr, inHostStr="127.0.0.1", inPortInt = 3389, inWidthPXInt = 1680,  inHeightPXInt = 1050,
                      inUseBothMonitorBool = False, inDepthBitInt = 32, inSharedDriveList=None):
    """
    Create RDP connect dict item/ Use it connect/reconnect (Orchestrator.RDPSessionConnect)

    .. code-block:: python

        # USAGE
        from pyOpenRPA import Orchestrator

        lRDPItemDict = Orchestrator.RDPTemplateCreate(
            inLoginStr = "USER_99",
            inPasswordStr = "USER_PASS_HERE",
            inHostStr="127.0.0.1",
            inPortInt = 3389,
            inWidthPXInt = 1680,
            inHeightPXInt = 1050,
            inUseBothMonitorBool = False,
            inDepthBitInt = 32,
            inSharedDriveList=None)
        #     lRDPTemplateDict= {  # Init the configuration item
        #         "Host": "127.0.0.1", "Port": "3389", "Login": "USER_99", "Password": "USER_PASS_HERE",
        #         "Screen": { "Width": 1680, "Height": 1050, "FlagUseAllMonitors": False, "DepthBit": "32" },
        #         "SharedDriveList": ["c"],
        #         ###### Will updated in program ############
        #         "SessionHex": "77777sdfsdf77777dsfdfsf77777777",  # Hex is created when robot runs, example ""
        #         "SessionIsWindowExistBool": False, "SessionIsWindowResponsibleBool": False, "SessionIsIgnoredBool": False
        #     }

    :param inLoginStr: User/Robot Login, example "USER_99"
    :param inPasswordStr: Password, example "USER_PASS_HERE"
    :param inHostStr: Host address, example "77.77.22.22"
    :param inPortInt: RDP Port, example "3389" (default)
    :param inWidthPXInt: Width of the remote desktop in pixels, example 1680
    :param inHeightPXInt: Height of the remote desktop in pixels, example 1050
    :param inUseBothMonitorBool: True - connect to the RDP with both monitors. False - else case
    :param inDepthBitInt: Remote desktop bitness. Available: 32 or 24 or 16 or 15, example 32
    :param inSharedDriveList: Host local disc to connect to the RDP session. Example: ["c", "d"]
    :return:
        {
            "Host": inHostStr,  # Host address, example "77.77.22.22"
            "Port": str(inPortInt),  # RDP Port, example "3389"
            "Login": inLoginStr,  # Login, example "test"
            "Password": inPasswordStr,  # Password, example "test"
            "Screen": {
                "Width": inWidthPXInt,  # Width of the remote desktop in pixels, example 1680
                "Height": inHeightPXInt,  # Height of the remote desktop in pixels, example 1050
                # "640x480" or "1680x1050" or "FullScreen". If Resolution not exists set full screen, example
                "FlagUseAllMonitors": inUseBothMonitorBool,  # True or False, example False
                "DepthBit": str(inDepthBitInt)  # "32" or "24" or "16" or "15", example "32"
            },
            "SharedDriveList": inSharedDriveList,  # List of the Root sesion hard drives, example ["c"]
            ###### Will updated in program ############
            "SessionHex": "77777sdfsdf77777dsfdfsf77777777",  # Hex is created when robot runs, example ""
            "SessionIsWindowExistBool": False,
            # Flag if the RDP window is exist, old name "FlagSessionIsActive". Check every n seconds , example False
            "SessionIsWindowResponsibleBool": False,
            # Flag if RDP window is responsible (recieve commands). Check every nn seconds. If window is Responsible - window is Exist too , example False
            "SessionIsIgnoredBool": False  # Flag to ignore RDP window False - dont ignore, True - ignore, example False
        }

    """
    if inSharedDriveList is None: inSharedDriveList = ["c"]
    lRDPTemplateDict= {  # Init the configuration item
        "Host": inHostStr,  # Host address, example "77.77.22.22"
        "Port": str(inPortInt),  # RDP Port, example "3389"
        "Login": inLoginStr,  # Login, example "test"
        "Password": inPasswordStr,  # Password, example "test"
        "Screen": {
            "Width": inWidthPXInt,  # Width of the remote desktop in pixels, example 1680
            "Height": inHeightPXInt,  # Height of the remote desktop in pixels, example 1050
            # "640x480" or "1680x1050" or "FullScreen". If Resolution not exists set full screen, example
            "FlagUseAllMonitors": inUseBothMonitorBool,  # True or False, example False
            "DepthBit": str(inDepthBitInt)  # "32" or "24" or "16" or "15", example "32"
        },
        "SharedDriveList": inSharedDriveList,  # List of the Root sesion hard drives, example ["c"]
        ###### Will updated in program ############
        "SessionHex": "77777sdfsdf77777dsfdfsf77777777",  # Hex is created when robot runs, example ""
        "SessionIsWindowExistBool": False,
        # Flag if the RDP window is exist, old name "FlagSessionIsActive". Check every n seconds , example False
        "SessionIsWindowResponsibleBool": False,
        # Flag if RDP window is responsible (recieve commands). Check every nn seconds. If window is Responsible - window is Exist too , example False
        "SessionIsIgnoredBool": False  # Flag to ignore RDP window False - dont ignore, True - ignore, example False
    }
    return lRDPTemplateDict

# TODO Search dublicates in GSettings RDPlist !
# Return list if dublicates
def RDPSessionDublicatesResolve(inGSettings):
    """
    DEVELOPING Search duplicates in GSettings RDPlist
    !def is developing!

    :param inGSettings: Global settings dict (singleton)
    :return:
    """
    pass
    #for lItemKeyStr in inGSettings["RobotRDPActive"]["RDPList"]:
    #   lItemDict = inGSettings["RobotRDPActive"]["RDPList"][lItemKeyStr]

def RDPSessionConnect(inGSettings, inRDPSessionKeyStr, inRDPTemplateDict=None, inHostStr=None, inPortStr=None, inLoginStr=None, inPasswordStr=None):
    """
    Create new RDPSession in RobotRDPActive. Attention - activity will be ignored if RDP key is already exists
     2 way of the use
    Var 1 (Main stream): inGSettings, inRDPSessionKeyStr, inRDPTemplateDict
    Var 2 (Backward compatibility): inGSettings, inRDPSessionKeyStr, inHostStr, inPortStr, inLoginStr, inPasswordStr

    .. code-block:: python

        # USAGE
        from pyOpenRPA import Orchestrator

        lRDPItemDict = Orchestrator.RDPTemplateCreate(
            inLoginStr = "USER_99",
            inPasswordStr = "USER_PASS_HERE", inHostStr="127.0.0.1", inPortInt = 3389, inWidthPXInt = 1680,
            inHeightPXInt = 1050, inUseBothMonitorBool = False, inDepthBitInt = 32, inSharedDriveList=None)
        Orchestrator.RDPSessionConnect(
            inGSettings = gSettings,
            inRDPSessionKeyStr = "RDPKey",
            inRDPTemplateDict = lRDPItemDict)
        # Orchestrator will create RDP session by the lRDPItemDict configuration

    :param inGSettings: Global settings dict (singleton)
    :param inRDPSessionKeyStr: RDP Session string key - need for the further identification
    :param inRDPTemplateDict: RDP configuration dict with settings (see def Orchestrator.RDPTemplateCreate)
    :param inHostStr: Backward compatibility from Orchestrator v 1.1.20. Use inRDPTemplateDict
    :param inPortStr: Backward compatibility from Orchestrator v 1.1.20. Use inRDPTemplateDict
    :param inLoginStr: Backward compatibility from Orchestrator v 1.1.20. Use inRDPTemplateDict
    :param inPasswordStr: Backward compatibility from Orchestrator v 1.1.20. Use inRDPTemplateDict
    :return: True every time :)
    """
    # Check thread
    if not Core.IsProcessorThread(inGSettings=inGSettings):
        if inGSettings["Logger"]: inGSettings["Logger"].warning(f"RDP def was called not from processor queue - activity will be append in the processor queue.")
        lResult = {
            "Def": RDPSessionConnect, # def link or def alias (look gSettings["Processor"]["AliasDefDict"])
            "ArgList": [],  # Args list
            "ArgDict": {"inRDPSessionKeyStr": inRDPSessionKeyStr, "inRDPTemplateDict":inRDPTemplateDict, "inHostStr": inHostStr, "inPortStr": inPortStr,
                    "inLoginStr": inLoginStr, "inPasswordStr": inPasswordStr},  # Args dictionary
            "ArgGSettings": "inGSettings",  # Name of GSettings attribute: str (ArgDict) or index (for ArgList)
            "ArgLogger": None  # Name of GSettings attribute: str (ArgDict) or index (for ArgList)
        }
        inGSettings["ProcessorDict"]["ActivityList"].append(lResult)
    else: # In processor - do execution
        # Var 1 - if RDPTemplateDict is input
        lRDPConfigurationItem=inRDPTemplateDict
        # Var 2 - backward compatibility
        if lRDPConfigurationItem is None:
            lRDPConfigurationItem = RDPTemplateCreate(inLoginStr=inLoginStr, inPasswordStr=inPasswordStr,
                  inHostStr=inHostStr, inPortInt = int(inPortStr))            # ATTENTION - dont connect if RDP session is exist
        # Start the connect
        if inRDPSessionKeyStr not in inGSettings["RobotRDPActive"]["RDPList"]:
            inGSettings["RobotRDPActive"]["RDPList"][inRDPSessionKeyStr] = lRDPConfigurationItem # Add item in RDPList
            Connector.Session(lRDPConfigurationItem) # Create the RDP session
            Connector.SystemRDPWarningClickOk()  # Click all warning messages
        else:
            if inGSettings["Logger"]: inGSettings["Logger"].warning(f"RDP session was not created because it is alredy exists in the RDPList. Use RDPSessionReconnect if you want to update RDP configuration.")
    return True

def RDPSessionDisconnect(inGSettings, inRDPSessionKeyStr, inBreakTriggerProcessWOExeList = None):
    """
    Disconnect the RDP session and stop monitoring it.

    .. code-block:: python

        # USAGE
        from pyOpenRPA import Orchestrator

        Orchestrator.RDPSessionDisconnect(
            inGSettings = gSettings,
            inRDPSessionKeyStr = "RDPKey")
        # Orchestrator will disconnect RDP session and will stop to monitoring current RDP

    :param inGSettings: Global settings dict (singleton)
    :param inRDPSessionKeyStr: RDP Session string key - need for the further identification
    :param inBreakTriggerProcessWOExeList: List of the processes, which will stop the execution. Example ["notepad"]

        .. note::

        Orchestrator look processes on the current machine
    :return: True every time
    """
    if inBreakTriggerProcessWOExeList is None: inBreakTriggerProcessWOExeList = []
    # Check thread
    if not Core.IsProcessorThread(inGSettings=inGSettings):
        if inGSettings["Logger"]: inGSettings["Logger"].warning(f"RDP def was called not from processor queue - activity will be append in the processor queue.")
        lResult = {
            "Def": RDPSessionDisconnect, # def link or def alias (look gSettings["Processor"]["AliasDefDict"])
            "ArgList": [],  # Args list
            "ArgDict": {"inRDPSessionKeyStr": inRDPSessionKeyStr, "inBreakTriggerProcessWOExeList": inBreakTriggerProcessWOExeList },  # Args dictionary
            "ArgGSettings": "inGSettings",  # Name of GSettings attribute: str (ArgDict) or index (for ArgList)
            "ArgLogger": None  # Name of GSettings attribute: str (ArgDict) or index (for ArgList)
        }
        inGSettings["ProcessorDict"]["ActivityList"].append(lResult)
    else: # In processor - do execution
        lSessionHex = inGSettings["RobotRDPActive"]["RDPList"].get(inRDPSessionKeyStr,{}).get("SessionHex", None)
        if lSessionHex:
            lProcessListResult = {"ProcessWOExeList":[],"ProcessDetailList":[]}
            if len(inBreakTriggerProcessWOExeList) > 0:
                lProcessListResult = ProcessListGet(inProcessNameWOExeList=inBreakTriggerProcessWOExeList)  # Run the task manager monitor
            if len(lProcessListResult["ProcessWOExeList"]) == 0: # Start disconnect if no process exist
                inGSettings["RobotRDPActive"]["RDPList"].pop(inRDPSessionKeyStr,None)
                Connector.SessionClose(inSessionHexStr=lSessionHex)
                Connector.SystemRDPWarningClickOk()  # Click all warning messages
    return True

def RDPSessionReconnect(inGSettings, inRDPSessionKeyStr, inRDPTemplateDict=None):
    """
    Reconnect the RDP session

    .. code-block:: python

        # USAGE
        from pyOpenRPA import Orchestrator

        lRDPItemDict = Orchestrator.RDPTemplateCreate(
            inLoginStr = "USER_99",
            inPasswordStr = "USER_PASS_HERE", inHostStr="127.0.0.1", inPortInt = 3389, inWidthPXInt = 1680,
            inHeightPXInt = 1050, inUseBothMonitorBool = False, inDepthBitInt = 32, inSharedDriveList=None)
        Orchestrator.RDPSessionReconnect(
            inGSettings = gSettings,
            inRDPSessionKeyStr = "RDPKey",
            inRDPTemplateDict = inRDPTemplateDict)
        # Orchestrator will reconnect RDP session and will continue to monitoring current RDP

    :param inGSettings: Global settings dict (singleton)
    :param inRDPSessionKeyStr: RDP Session string key - need for the further identification
    :param inRDPTemplateDict: RDP configuration dict with settings (see def Orchestrator.RDPTemplateCreate)
    :return:
    """
    # Check thread
    if not Core.IsProcessorThread(inGSettings=inGSettings):
        if inGSettings["Logger"]: inGSettings["Logger"].warning(f"RDP def was called not from processor queue - activity will be append in the processor queue.")
        lResult = {
            "Def": RDPSessionReconnect, # def link or def alias (look gSettings["Processor"]["AliasDefDict"])
            "ArgList": [],  # Args list
            "ArgDict": {"inRDPSessionKeyStr": inRDPSessionKeyStr, "inRDPTemplateDict":inRDPTemplateDict },  # Args dictionary
            "ArgGSettings": "inGSettings",  # Name of GSettings attribute: str (ArgDict) or index (for ArgList)
            "ArgLogger": None  # Name of GSettings attribute: str (ArgDict) or index (for ArgList)
        }
        inGSettings["ProcessorDict"]["ActivityList"].append(lResult)
    else:
        lRDPConfigurationItem = inGSettings["RobotRDPActive"]["RDPList"][inRDPSessionKeyStr]
        RDPSessionDisconnect(inGSettings = inGSettings, inRDPSessionKeyStr=inRDPSessionKeyStr) # Disconnect the RDP 2021 02 22 minor fix by Ivan Maslov
        # Replace Configuration item if inRDPTemplateDict exists
        if inRDPTemplateDict is not None: lRDPConfigurationItem=inRDPTemplateDict
        # Add item in RDPList
        inGSettings["RobotRDPActive"]["RDPList"][inRDPSessionKeyStr] = lRDPConfigurationItem
        # Create the RDP session
        Connector.Session(lRDPConfigurationItem)
    return True

def RDPSessionMonitorStop(inGSettings, inRDPSessionKeyStr):
    """
    Stop monitoring the RDP session by the Orchestrator process. Current def don't kill RDP session - only stop to track it (it can give )

    .. code-block:: python

        # USAGE
        from pyOpenRPA import Orchestrator

        Orchestrator.RDPSessionMonitorStop(
            inGSettings = gSettings,
            inRDPSessionKeyStr = "RDPKey")
        # Orchestrator will stop the RDP monitoring

    :param inGSettings: Global settings dict (singleton)
    :param inRDPSessionKeyStr: RDP Session string key - need for the further identification
    :return: True every time :>
    """
    lResult = True
    inGSettings["RobotRDPActive"]["RDPList"].pop(inRDPSessionKeyStr,None) # Remove item from RDPList
    return lResult

def RDPSessionLogoff(inGSettings, inRDPSessionKeyStr, inBreakTriggerProcessWOExeList = None):
    """
    Logoff the RDP session from the Orchestrator process (close all apps in session when logoff)

    .. code-block:: python

        # USAGE
        from pyOpenRPA import Orchestrator

        Orchestrator.RDPSessionLogoff(
            inGSettings = gSettings,
            inRDPSessionKeyStr = "RDPKey",
            inBreakTriggerProcessWOExeList = ['Notepad'])
        # Orchestrator will logoff the RDP session

    :param inGSettings: Global settings dict (singleton)
    :param inRDPSessionKeyStr: RDP Session string key - need for the further identification
    :param inBreakTriggerProcessWOExeList: List of the processes, which will stop the execution. Example ["notepad"]
    :return: True - logoff is successful
    """
    if inBreakTriggerProcessWOExeList is None: inBreakTriggerProcessWOExeList = []
    lResult = True
    # Check thread
    if not Core.IsProcessorThread(inGSettings=inGSettings):
        if inGSettings["Logger"]: inGSettings["Logger"].warning(f"RDP def was called not from processor queue - activity will be append in the processor queue.")
        lResult = {
            "Def": RDPSessionLogoff, # def link or def alias (look gSettings["Processor"]["AliasDefDict"])
            "ArgList": [],  # Args list
            "ArgDict": {"inRDPSessionKeyStr": inRDPSessionKeyStr, "inBreakTriggerProcessWOExeList": inBreakTriggerProcessWOExeList },  # Args dictionary
            "ArgGSettings": "inGSettings",  # Name of GSettings attribute: str (ArgDict) or index (for ArgList)
            "ArgLogger": None  # Name of GSettings attribute: str (ArgDict) or index (for ArgList)
        }
        inGSettings["ProcessorDict"]["ActivityList"].append(lResult)
    else:
        lCMDStr = "shutdown -L" # CMD logoff command
        # Calculate the session Hex
        lSessionHex = inGSettings["RobotRDPActive"]["RDPList"].get(inRDPSessionKeyStr,{}).get("SessionHex", None)
        if lSessionHex:
            lProcessListResult = {"ProcessWOExeList":[],"ProcessDetailList":[]}
            if len(inBreakTriggerProcessWOExeList) > 0:
                lProcessListResult = ProcessListGet(inProcessNameWOExeList=inBreakTriggerProcessWOExeList)  # Run the task manager monitor
            if len(lProcessListResult["ProcessWOExeList"]) == 0: # Start logoff if no process exist
                # Run CMD - dont crosscheck because CMD dont return value to the clipboard when logoff
                Connector.SessionCMDRun(inSessionHex=lSessionHex, inCMDCommandStr=lCMDStr, inModeStr="RUN", inLogger=inGSettings["Logger"], inRDPConfigurationItem=inGSettings["RobotRDPActive"]["RDPList"][inRDPSessionKeyStr])
                inGSettings["RobotRDPActive"]["RDPList"].pop(inRDPSessionKeyStr,None) # Remove item from RDPList
    return lResult

def RDPSessionResponsibilityCheck(inGSettings, inRDPSessionKeyStr):
    """
    DEVELOPING, MAYBE NOT USEFUL Check RDP Session responsibility TODO NEED DEV + TEST

    :param inGSettings: Global settings dict (singleton)
    :param inRDPSessionKeyStr: RDP Session string key - need for the further identification
    :return: True every time
    """
    # Check thread
    if not Core.IsProcessorThread(inGSettings=inGSettings):
        if inGSettings["Logger"]: inGSettings["Logger"].warning(f"RDP def was called not from processor queue - activity will be append in the processor queue.")
        lResult = {
            "Def": RDPSessionResponsibilityCheck, # def link or def alias (look gSettings["Processor"]["AliasDefDict"])
            "ArgList": [],  # Args list
            "ArgDict": {"inRDPSessionKeyStr": inRDPSessionKeyStr },  # Args dictionary
            "ArgGSettings": "inGSettings",  # Name of GSettings attribute: str (ArgDict) or index (for ArgList)
            "ArgLogger": None  # Name of GSettings attribute: str (ArgDict) or index (for ArgList)
        }
        inGSettings["ProcessorDict"]["ActivityList"].append(lResult)
    else:
        lRDPConfigurationItem = inGSettings["RobotRDPActive"]["RDPList"][inRDPSessionKeyStr] # Get the alias
        # set the fullscreen
        # ATTENTION!!! Session hex can be updated!!!
        Connector.SessionScreenFull(inSessionHex=lRDPConfigurationItem["SessionHex"], inLogger=inGSettings["Logger"], inRDPConfigurationItem=inGSettings["RobotRDPActive"]["RDPList"][inRDPSessionKeyStr])
        time.sleep(1)
        # Check RDP responsibility
        lDoCheckResponsibilityBool = True
        lDoCheckResponsibilityCountMax = 20
        lDoCheckResponsibilityCountCurrent = 0
        while lDoCheckResponsibilityBool:
            # Check if counter is exceed - raise exception
            if lDoCheckResponsibilityCountCurrent >= lDoCheckResponsibilityCountMax:
                pass
                #raise ConnectorExceptions.SessionWindowNotResponsibleError("Error when initialize the RDP session - RDP window is not responding!")
            # Check responding
            lDoCheckResponsibilityBool = not Connector.SystemRDPIsResponsible(inSessionHexStr = lRDPConfigurationItem["SessionHex"])
            # Wait if is not responding
            if lDoCheckResponsibilityBool:
                time.sleep(3)
            # increase the couter
            lDoCheckResponsibilityCountCurrent+=1
    return True

def RDPSessionProcessStartIfNotRunning(inGSettings, inRDPSessionKeyStr, inProcessNameWEXEStr, inFilePathStr, inFlagGetAbsPathBool=True):
    """
    Start process in RDP if it is not running (check by the arg inProcessNameWEXEStr)

    .. code-block:: python

        # USAGE
        from pyOpenRPA import Orchestrator

        Orchestrator.RDPSessionProcessStartIfNotRunning(
            inGSettings = gSettings,
            inRDPSessionKeyStr = "RDPKey",
            inProcessNameWEXEStr = 'Notepad.exe',
            inFilePathStr = "path\\to\the\\executable\\file.exe"
            inFlagGetAbsPathBool = True)
        # Orchestrator will start the process in RDP session

    :param inGSettings: Global settings dict (singleton)
    :param inRDPSessionKeyStr: RDP Session string key - need for the further identification
    :param inProcessNameWEXEStr: Process name with extension (.exe). This arg allow to check the process is running. Example: "Notepad.exe"
    :param inFilePathStr: Path to run process if it is not running.
    :param inFlagGetAbsPathBool: True - get abs path from the relative path in inFilePathStr. False - else case
    :return: True every time :)
    """
    # Check thread
    lResult = True
    if not Core.IsProcessorThread(inGSettings=inGSettings):
        if inGSettings["Logger"]: inGSettings["Logger"].warning(f"RDP def was called not from processor queue - activity will be append in the processor queue.")
        lActivityItem = {
            "Def": RDPSessionProcessStartIfNotRunning, # def link or def alias (look gSettings["Processor"]["AliasDefDict"])
            "ArgList": [],  # Args list
            "ArgDict": {"inRDPSessionKeyStr": inRDPSessionKeyStr,  "inProcessNameWEXEStr": inProcessNameWEXEStr, "inFilePathStr": inFilePathStr, "inFlagGetAbsPathBool": inFlagGetAbsPathBool },  # Args dictionary
            "ArgGSettings": "inGSettings",  # Name of GSettings attribute: str (ArgDict) or index (for ArgList)
            "ArgLogger": None  # Name of GSettings attribute: str (ArgDict) or index (for ArgList)
        }
        inGSettings["ProcessorDict"]["ActivityList"].append(lActivityItem)
    else:
        lCMDStr = CMDStr.ProcessStartIfNotRunning(inProcessNameWEXEStr, inFilePathStr, inFlagGetAbsPath= inFlagGetAbsPathBool)
        # Calculate the session Hex
        lSessionHex = inGSettings["RobotRDPActive"]["RDPList"].get(inRDPSessionKeyStr,{}).get("SessionHex", None)
        # Run CMD
        if lSessionHex:
            Connector.SessionCMDRun(inSessionHex=lSessionHex, inCMDCommandStr=lCMDStr, inModeStr="CROSSCHECK", inLogger=inGSettings["Logger"],
                                    inRDPConfigurationItem=inGSettings["RobotRDPActive"]["RDPList"][inRDPSessionKeyStr])
    return lResult

def RDPSessionCMDRun(inGSettings, inRDPSessionKeyStr, inCMDStr, inModeStr="CROSSCHECK"):
    """
    Send CMD command to the RDP session "RUN" window

    .. code-block:: python

        # USAGE
        from pyOpenRPA import Orchestrator

        lResultDict = Orchestrator.RDPSessionCMDRun(
            inGSettings = gSettings,
            inRDPSessionKeyStr = "RDPKey",
            inModeStr = 'LISTEN')
        # Orchestrator will send CMD to RDP and return the result (see return section)

    :param inGSettings: Global settings dict (singleton)
    :param inRDPSessionKeyStr: RDP Session string key - need for the further identification
    :param inCMDStr: Any CMD string
    :param inModeStr: Variants:
        "LISTEN" - Get result of the cmd command in result;
        "CROSSCHECK" - Check if the command was successfully sent
        "RUN" - Run without crosscheck and get clipboard
    :return: # OLD > True - CMD was executed successfully
         {
          "OutStr": <> # Result string
          "IsResponsibleBool": True|False # Flag is RDP is responsible - works only when inModeStr = CROSSCHECK
        }
    """
    lResult = {
        "OutStr": None,  # Result string
        "IsResponsibleBool": False  # Flag is RDP is responsible - works only when inModeStr = CROSSCHECK
    }
    # Check thread
    if not Core.IsProcessorThread(inGSettings=inGSettings):
        if inGSettings["Logger"]: inGSettings["Logger"].warning(f"RDP def was called not from processor queue - activity will be append in the processor queue.")
        lProcessorActivityDict = {
            "Def": RDPSessionCMDRun, # def link or def alias (look gSettings["Processor"]["AliasDefDict"])
            "ArgList": [],  # Args list
            "ArgDict": {"inRDPSessionKeyStr": inRDPSessionKeyStr,  "inCMDStr": inCMDStr, "inModeStr": inModeStr },  # Args dictionary
            "ArgGSettings": "inGSettings",  # Name of GSettings attribute: str (ArgDict) or index (for ArgList)
            "ArgLogger": None  # Name of GSettings attribute: str (ArgDict) or index (for ArgList)
        }
        inGSettings["ProcessorDict"]["ActivityList"].append(lProcessorActivityDict)
    else:
        #lResult = True
        # Calculate the session Hex
        lSessionHex = inGSettings["RobotRDPActive"]["RDPList"].get(inRDPSessionKeyStr,{}).get("SessionHex", None)
        # Run CMD
        if lSessionHex:
            lResult = Connector.SessionCMDRun(inSessionHex=lSessionHex, inCMDCommandStr=inCMDStr, inModeStr=inModeStr, inLogger=inGSettings["Logger"],
                                    inRDPConfigurationItem=inGSettings["RobotRDPActive"]["RDPList"][inRDPSessionKeyStr])
    return lResult

def RDPSessionProcessStop(inGSettings, inRDPSessionKeyStr, inProcessNameWEXEStr, inFlagForceCloseBool):
    """
    Send CMD command to the RDP session "RUN" window.

    .. code-block:: python

        # USAGE
        from pyOpenRPA import Orchestrator

        lResultDict = Orchestrator.RDPSessionProcessStop(
            inGSettings = gSettings,
            inRDPSessionKeyStr = "RDPKey",
            inProcessNameWEXEStr = 'notepad.exe',
            inFlagForceCloseBool = True)
        # Orchestrator will send CMD to RDP and return the result (see return section)

    :param inGSettings: Global settings dict (singleton)
    :param inRDPSessionKeyStr: RDP Session string key - need for the further identification
    :param inProcessNameWEXEStr: Process name to kill. Example: 'notepad.exe'
    :param inFlagForceCloseBool: True - force close the process. False - safe close the process
    :return: True every time
    """
    # Check thread
    if not Core.IsProcessorThread(inGSettings=inGSettings):
        if inGSettings["Logger"]: inGSettings["Logger"].warning(f"RDP def was called not from processor queue - activity will be append in the processor queue.")
        lResult = {
            "Def": RDPSessionProcessStop, # def link or def alias (look gSettings["Processor"]["AliasDefDict"])
            "ArgList": [],  # Args list
            "ArgDict": {"inRDPSessionKeyStr": inRDPSessionKeyStr,  "inProcessNameWEXEStr": inProcessNameWEXEStr, "inFlagForceCloseBool": inFlagForceCloseBool },  # Args dictionary
            "ArgGSettings": "inGSettings",  # Name of GSettings attribute: str (ArgDict) or index (for ArgList)
            "ArgLogger": None  # Name of GSettings attribute: str (ArgDict) or index (for ArgList)
        }
        inGSettings["ProcessorDict"]["ActivityList"].append(lResult)
    else:
        lResult = True
        lCMDStr = f'taskkill /im "{inProcessNameWEXEStr}" /fi "username eq %USERNAME%"'
        if inFlagForceCloseBool:
            lCMDStr+= " /F"
        # Calculate the session Hex
        lSessionHex = inGSettings["RobotRDPActive"]["RDPList"].get(inRDPSessionKeyStr,{}).get("SessionHex", None)
        # Run CMD
        if lSessionHex:
            Connector.SessionCMDRun(inSessionHex=lSessionHex, inCMDCommandStr=lCMDStr, inModeStr="CROSSCHECK", inLogger=inGSettings["Logger"], inRDPConfigurationItem=inGSettings["RobotRDPActive"]["RDPList"][inRDPSessionKeyStr])
    return lResult

def RDPSessionFileStoredSend(inGSettings, inRDPSessionKeyStr, inHostFilePathStr, inRDPFilePathStr):
    """
    Send file from Orchestrator session to the RDP session using shared drive in RDP (see RDP Configuration Dict, Shared drive)

    .. code-block:: python

        # USAGE
        from pyOpenRPA import Orchestrator

        lResultDict = Orchestrator.RDPSessionFileStoredSend(
            inGSettings = gSettings,
            inRDPSessionKeyStr = "RDPKey",
            inHostFilePathStr = "TESTDIR\\Test.py",
            inRDPFilePathStr = "C:\\RPA\\TESTDIR\\Test.py")
        # Orchestrator will send CMD to RDP and return the result (see return section)

    :param inGSettings: Global settings dict (singleton)
    :param inRDPSessionKeyStr: RDP Session string key - need for the further identification
    :param inHostFilePathStr: Relative or absolute path to the file location on the Orchestrator side. Example: "TESTDIR\\Test.py"
    :param inRDPFilePathStr: !Absolute! path to the destination file location on the RDP side. Example: "C:\\RPA\\TESTDIR\\Test.py"
    :return: True every time
    """
    # Check thread
    if not Core.IsProcessorThread(inGSettings=inGSettings):
        if inGSettings["Logger"]: inGSettings["Logger"].warning(f"RDP def was called not from processor queue - activity will be append in the processor queue.")
        lResult = {
            "Def": RDPSessionFileStoredSend, # def link or def alias (look gSettings["Processor"]["AliasDefDict"])
            "ArgList": [],  # Args list
            "ArgDict": {"inRDPSessionKeyStr": inRDPSessionKeyStr,  "inHostFilePathStr": inHostFilePathStr, "inRDPFilePathStr": inRDPFilePathStr },  # Args dictionary
            "ArgGSettings": "inGSettings",  # Name of GSettings attribute: str (ArgDict) or index (for ArgList)
            "ArgLogger": None  # Name of GSettings attribute: str (ArgDict) or index (for ArgList)
        }
        inGSettings["ProcessorDict"]["ActivityList"].append(lResult)
    else:
        lResult = True
        lCMDStr = CMDStr.FileStoredSend(inHostFilePath = inHostFilePathStr, inRDPFilePath = inRDPFilePathStr)
        # Calculate the session Hex
        lSessionHex = inGSettings["RobotRDPActive"]["RDPList"].get(inRDPSessionKeyStr, {}).get("SessionHex", None)
        #lSessionHex = inGlobalDict["RobotRDPActive"]["RDPList"][inRDPSessionKeyStr]["SessionHex"]
        # Run CMD
        if lSessionHex:
            Connector.SessionCMDRun(inSessionHex=lSessionHex, inCMDCommandStr=lCMDStr, inModeStr="LISTEN", inClipboardTimeoutSec = 120, inLogger=inGSettings["Logger"], inRDPConfigurationItem=inGSettings["RobotRDPActive"]["RDPList"][inRDPSessionKeyStr])
    return lResult

def RDPSessionFileStoredRecieve(inGSettings, inRDPSessionKeyStr, inRDPFilePathStr, inHostFilePathStr):
    """
    Recieve file from RDP session to the Orchestrator session using shared drive in RDP (see RDP Configuration Dict, Shared drive)

    .. code-block:: python

        # USAGE
        from pyOpenRPA import Orchestrator

        lResultDict = Orchestrator.RDPSessionFileStoredRecieve(
            inGSettings = gSettings,
            inRDPSessionKeyStr = "RDPKey",
            inHostFilePathStr = "TESTDIR\\Test.py",
            inRDPFilePathStr = "C:\\RPA\\TESTDIR\\Test.py")
        # Orchestrator will send CMD to RDP and return the result (see return section)

    :param inGSettings: Global settings dict (singleton)
    :param inRDPSessionKeyStr: RDP Session string key - need for the further identification
    :param inRDPFilePathStr: !Absolute! path to the destination file location on the RDP side. Example: "C:\\RPA\\TESTDIR\\Test.py"
    :param inHostFilePathStr: Relative or absolute path to the file location on the Orchestrator side. Example: "TESTDIR\\Test.py"
    :return: True every time
    """
    # Check thread
    if not Core.IsProcessorThread(inGSettings=inGSettings):
        if inGSettings["Logger"]: inGSettings["Logger"].warning(f"RDP def was called not from processor queue - activity will be append in the processor queue.")
        lResult = {
            "Def": RDPSessionFileStoredRecieve, # def link or def alias (look gSettings["Processor"]["AliasDefDict"])
            "ArgList": [],  # Args list
            "ArgDict": {"inRDPSessionKeyStr": inRDPSessionKeyStr, "inRDPFilePathStr": inRDPFilePathStr, "inHostFilePathStr": inHostFilePathStr },  # Args dictionary
            "ArgGSettings": "inGSettings",  # Name of GSettings attribute: str (ArgDict) or index (for ArgList)
            "ArgLogger": None  # Name of GSettings attribute: str (ArgDict) or index (for ArgList)
        }
        inGSettings["ProcessorDict"]["ActivityList"].append(lResult)
    else:
        lResult = True
        lCMDStr = CMDStr.FileStoredRecieve(inRDPFilePath = inRDPFilePathStr, inHostFilePath = inHostFilePathStr)
        # Calculate the session Hex
        lSessionHex = inGSettings["RobotRDPActive"]["RDPList"].get(inRDPSessionKeyStr,{}).get("SessionHex", None)
        # Run CMD
        if lSessionHex:
            Connector.SessionCMDRun(inSessionHex=lSessionHex, inCMDCommandStr=lCMDStr, inModeStr="LISTEN", inClipboardTimeoutSec = 120, inLogger=inGSettings["Logger"], inRDPConfigurationItem=inGSettings["RobotRDPActive"]["RDPList"][inRDPSessionKeyStr])
    return lResult

# # # # # # # # # # # # # # # # # # # # # # #
# # # # # Start orchestrator
# # # # # # # # # # # # # # # # # # # # # # #

def GSettingsAutocleaner(inGSettings):
    """
    HIDDEN Interval gSettings auto cleaner def to clear some garbage.

    :param inGSettings: Global settings dict (singleton)
    :return: None
    """
    while True:
        time.sleep(inGSettings["Autocleaner"]["IntervalSecFloat"])  # Wait for the next iteration
        lL = inGSettings["Logger"]
        if lL: lL.info(f"Autocleaner is running") # Info
        lNowDatetime = datetime.datetime.now() # Get now time
        # Clean old items in Client > Session > TechnicalSessionGUIDCache
        lTechnicalSessionGUIDCacheNew = {}
        for lItemKeyStr in inGSettings["Client"]["Session"]["TechnicalSessionGUIDCache"]:
            lItemValue = inGSettings["Client"]["Session"]["TechnicalSessionGUIDCache"][lItemKeyStr]
            if (lNowDatetime - lItemValue["InitDatetime"]).total_seconds() < inGSettings["Client"]["Session"]["LifetimeSecFloat"]: # Add if lifetime is ok
                lTechnicalSessionGUIDCacheNew[lItemKeyStr]=lItemValue # Lifetime is ok - set
            else:
                if lL: lL.debug(f"Client > Session > TechnicalSessionGUIDCache > lItemKeyStr: Lifetime is expired. Remove from gSettings")  # Info
        inGSettings["Client"]["Session"]["TechnicalSessionGUIDCache"] = lTechnicalSessionGUIDCacheNew # Set updated Cache
    # # # # # # # # # # # # # # # # # # # # # # # # # #

from .. import __version__ # Get version from the package

def Orchestrator(inGSettings):
    lL = inGSettings["Logger"]
    # https://stackoverflow.com/questions/130763/request-uac-elevation-from-within-a-python-script
    def is_admin():
        try:
            return ctypes.windll.shell32.IsUserAnAdmin()
        except:
            return False
    if not is_admin():
        # Re-run the program with admin rights
        ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, " ".join(sys.argv), None, 1)
    else:
        # Code of your program here
        #mGlobalDict = Settings.Settings(sys.argv[1])
        gSettingsDict = inGSettings # Alias for old name in alg
        inGSettings["VersionStr"] = __version__
        #Logger alias
        lL = gSettingsDict["Logger"]

        if lL: lL.info("Link the gSettings in submodules")  #Logging
        Processor.gSettingsDict = gSettingsDict
        Timer.gSettingsDict = gSettingsDict
        Timer.Processor.gSettingsDict = gSettingsDict
        Server.gSettingsDict = gSettingsDict
        Server.ProcessorOld.gSettingsDict = gSettingsDict # Backward compatibility

        # Check _SessionLast_RDPList.json in working directory. if exist - load into gsettings
        # GSettings
        #"RobotRDPActive": {
        #    "RDPList": {
        if os.path.exists("_SessionLast_RDPList.json"):
            lFile = open("_SessionLast_RDPList.json", "r", encoding="utf-8")
            lSessionLastRDPList = json.loads(lFile.read())
            lFile.close() # Close the file
            os.remove("_SessionLast_RDPList.json") # remove the temp file
            gSettingsDict["RobotRDPActive"]["RDPList"]=lSessionLastRDPList # Set the last session dict
            if lL: lL.warning(f"RDP Session List was restored from previous Orchestrator session")

        # Init SettingsUpdate defs from file list (after RDP restore)
        lSettingsUpdateFilePathList = gSettingsDict.get("OrchestratorStart", {}).get("DefSettingsUpdatePathList",[])
        lSubmoduleFunctionName = "SettingsUpdate"
        lSettingsPath = "\\".join(os.path.join(os.getcwd(), __file__).split("\\")[:-1])
        for lModuleFilePathItem in lSettingsUpdateFilePathList:  # Import defs with try catch
            try:  # Try to init - go next if error and log in logger
                lModuleName = lModuleFilePathItem[0:-3]
                lFileFullPath = os.path.join(lSettingsPath, lModuleFilePathItem)
                lTechSpecification = importlib.util.spec_from_file_location(lModuleName, lFileFullPath)
                lTechModuleFromSpec = importlib.util.module_from_spec(lTechSpecification)
                lTechSpecificationModuleLoader = lTechSpecification.loader.exec_module(lTechModuleFromSpec)
                if lSubmoduleFunctionName in dir(lTechModuleFromSpec):
                    # Run SettingUpdate function in submodule
                    getattr(lTechModuleFromSpec, lSubmoduleFunctionName)(gSettingsDict)
            except Exception as e:
                if lL: lL.exception(f"Error when init .py file in orchestrator '{lModuleFilePathItem}'. Exception is below:")

        # Turn on backward compatibility
        BackwardCompatibility.Update(inGSettings= gSettingsDict)

        # Append Orchestrator def to ProcessorDictAlias
        lModule = sys.modules[__name__]
        lModuleDefList = dir(lModule)
        for lItemDefNameStr in lModuleDefList:
            # Dont append alias for defs Orchestrator and ___deprecated_orchestrator_start__
            if lItemDefNameStr not in ["Orchestrator", "___deprecated_orchestrator_start__"]:
                lItemDef = getattr(lModule,lItemDefNameStr)
                if callable(lItemDef): inGSettings["ProcessorDict"]["AliasDefDict"][lItemDefNameStr]=lItemDef

        #Инициализация настроечных параметров
        lDaemonLoopSeconds=gSettingsDict["SchedulerDict"]["CheckIntervalSecFloat"]
        lDaemonActivityLogDict={} #Словарь отработанных активностей, ключ - кортеж (<activityType>, <datetime>, <processPath || processName>, <processArgs>)
        lDaemonLastDateTime=datetime.datetime.now()
        gSettingsDict["ServerDict"]["WorkingDirectoryPathStr"] = os.getcwd() # Set working directory in g settings

        #Инициализация сервера
        lThreadServer = Server.RobotDaemonServer("ServerThread", gSettingsDict)
        lThreadServer.start()
        if lL: lL.info("Web server has been started")  #Logging

        # Init the RobotScreenActive in another thread
        lRobotScreenActiveThread = threading.Thread(target= Monitor.CheckScreen)
        lRobotScreenActiveThread.daemon = True # Run the thread in daemon mode.
        lRobotScreenActiveThread.start() # Start the thread execution.
        if lL: lL.info("Robot Screen active has been started")  #Logging

        # Init the RobotRDPActive in another thread
        lRobotRDPThreadControlDict = {"ThreadExecuteBool":True} # inThreadControlDict = {"ThreadExecuteBool":True}
        lRobotRDPActiveThread = threading.Thread(target= RobotRDPActive.RobotRDPActive, kwargs={"inGSettings":gSettingsDict, "inThreadControlDict":lRobotRDPThreadControlDict})
        lRobotRDPActiveThread.daemon = True # Run the thread in daemon mode.
        lRobotRDPActiveThread.start() # Start the thread execution.
        if lL: lL.info("Robot RDP active has been started")  #Logging

        # Init autocleaner in another thread
        lAutocleanerThread = threading.Thread(target= GSettingsAutocleaner, kwargs={"inGSettings":gSettingsDict})
        lAutocleanerThread.daemon = True # Run the thread in daemon mode.
        lAutocleanerThread.start() # Start the thread execution.
        if lL: lL.info("Autocleaner thread has been started")  #Logging

        # Orchestrator start activity
        if lL: lL.info("Orchestrator start activity run")  #Logging
        for lActivityItem in gSettingsDict["OrchestratorStart"]["ActivityList"]:
            # Processor.ActivityListOrDict(lActivityItem)
            Processor.ActivityListExecute(inGSettings=gSettingsDict,inActivityList=[BackwardCompatibility.v1_2_0_ProcessorOld2NewActivityDict(lActivityItem)])
        # Processor thread
        lProcessorThread = threading.Thread(target= Processor.ProcessorRunSync, kwargs={"inGSettings":gSettingsDict, "inRobotRDPThreadControlDict":lRobotRDPThreadControlDict})
        lProcessorThread.daemon = True # Run the thread in daemon mode.
        lProcessorThread.start() # Start the thread execution.
        if lL: lL.info("Processor has been started (ProcessorDict)")  #Logging


        if lL: lL.info("Scheduler loop start")  #Logging
        gDaemonActivityLogDictRefreshSecInt = 10 # The second period for clear lDaemonActivityLogDict from old items
        gDaemonActivityLogDictLastTime = time.time() # The second perioad for clean lDaemonActivityLogDict from old items
        while True:
            try:
                lCurrentDateTime = datetime.datetime.now()
                #Циклический обход правил
                lFlagSearchActivityType=True
                # Periodically clear the lDaemonActivityLogDict
                if time.time()-gDaemonActivityLogDictLastTime>=gDaemonActivityLogDictRefreshSecInt:
                    gDaemonActivityLogDictLastTime = time.time() # Update the time
                    for lIndex, lItem in enumerate(lDaemonActivityLogDict):
                        if lItem["ActivityEndDateTime"] and lCurrentDateTime<=lItem["ActivityEndDateTime"]:
                            pass
                            # Activity is actual - do not delete now
                        else:
                            # remove the activity - not actual
                            lDaemonActivityLogDict.pop(lIndex,None)
                lIterationLastDateTime = lDaemonLastDateTime # Get current datetime before iterator (need for iterate all activities in loop)
                # Iterate throught the activity list
                for lIndex, lItem in enumerate(gSettingsDict["SchedulerDict"]["ActivityTimeList"]):
                    try:
                        # Prepare GUID of the activity
                        lGUID = None
                        if "GUID" in lItem and lItem["GUID"]:
                            lGUID = lItem["GUID"]
                        else:
                            lGUID = str(uuid.uuid4())
                            lItem["GUID"]=lGUID

                        #Проверка дней недели, в рамках которых можно запускать активность
                        lItemWeekdayList=lItem.get("WeekdayList", [0, 1, 2, 3, 4, 5, 6])
                        if lCurrentDateTime.weekday() in lItemWeekdayList:
                            if lFlagSearchActivityType:
                                #######################################################################
                                #Branch 1 - if has TimeHH:MM
                                #######################################################################
                                if "TimeHH:MMStr" in lItem:
                                    #Вид активности - запуск процесса
                                    #Сформировать временной штамп, относительно которого надо будет проверять время
                                    #часовой пояс пока не учитываем
                                    lActivityDateTime=datetime.datetime.strptime(lItem["TimeHH:MMStr"],"%H:%M")
                                    lActivityDateTime=lActivityDateTime.replace(year=lCurrentDateTime.year,month=lCurrentDateTime.month,day=lCurrentDateTime.day)
                                    #Убедиться в том, что время наступило
                                    if (
                                            lActivityDateTime>=lDaemonLastDateTime and
                                            lCurrentDateTime>=lActivityDateTime):
                                        # Log info about activity
                                        if lL: lL.info(f"Scheduler:: Activity list is started in new thread. Parameters are not available to see.")  #Logging
                                        # Do the activity
                                        lThread = threading.Thread(target=Processor.ActivityListExecute, kwargs={"inGSettings": inGSettings, "inActivityList":lItem["ActivityList"]})
                                        lThread.start()
                                        lIterationLastDateTime = datetime.datetime.now() # Set the new datetime for the new processor activity
                    except Exception as e:
                        if lL: lL.exception(f"Scheduler: Exception has been catched in Scheduler module when activity time item was initialising. ActivityTimeItem is {lItem}")
                lDaemonLastDateTime = lIterationLastDateTime # Set the new datetime for the new processor activity
                #Уснуть до следующего прогона
                time.sleep(lDaemonLoopSeconds)
            except Exception as e:
                if lL: lL.exception(f"Scheduler: Exception has been catched in Scheduler module. Global error")

# Backward compatibility below to 1.2.0
def __deprecated_orchestrator_start__():
    lSubmoduleFunctionName = "Settings"
    lFileFullPath = sys.argv[1]
    lModuleName = (lFileFullPath.split("\\")[-1])[0:-3]
    lTechSpecification = importlib.util.spec_from_file_location(lModuleName, lFileFullPath)
    lTechModuleFromSpec = importlib.util.module_from_spec(lTechSpecification)
    lTechSpecificationModuleLoader = lTechSpecification.loader.exec_module(lTechModuleFromSpec)
    gSettingsDict = None
    if lSubmoduleFunctionName in dir(lTechModuleFromSpec):
        # Run SettingUpdate function in submodule
        gSettingsDict = getattr(lTechModuleFromSpec, lSubmoduleFunctionName)()
    #################################################
    Orchestrator(inGSettings=gSettingsDict) # Call the orchestrator
