import os, logging, datetime, sys

# Technical def - return GSettings structure with examples
def __Create__():
    return {
        "VersionStr": None, # Will be filled in orchestrator,
        "Autocleaner": {
            # Some gurbage is collecting in g settings. So you can configure autocleaner to periodically clear gSettings
            "IntervalSecFloat": 3600.0,  # Sec float to periodically clear gsettings
        },
        "Client": {  # Settings about client web orchestrator
            "Session": {
                # Settings about web session. Session algorythms works only for special requests (URL in ServerSettings)
                "LifetimeSecFloat": 600.0,
                # Client Session lifetime in seconds. after this time server will forget about this client session
                "LifetimeRequestSecFloat": 120.0,  # 1 client request lifetime in server in seconds
                "ControlPanelRefreshIntervalSecFloat": 1.5,  # Interval to refresh control panels for session,
                "TechnicalSessionGUIDCache": {  # TEchnical cache. Fills when web browser is requesting
                    # "SessionGUIDStr":{ # Session with some GUID str. On client session guid stored in cookie "SessionGUIDStr"
                    #    "InitDatetime": None, # Datetime when session GUID was created
                    #    "DatasetLast": {
                    #        "ControlPanel": {
                    #            "Data": None, # Struct to check with new iterations. None if starts
                    #            "ReturnBool": False # flag to return, close request and return data as json
                    #        }
                    #    },
                    #    "ClientRequestHandler": None, # Last client request handler
                    #    "UserADStr": None, # User, who connect. None if user is not exists
                    #    "DomainADStr": None, # Domain of the user who connect. None if user is not exists
                    # }
                },
            },
            # # # # # # Client... # # # # # # # #
            "DumpLogListRefreshIntervalSecFloat": 3.0,  # Duration between updates for the Client
            "DumpLogListCountInt": 100,  # Set the max row for the dump
            "DumpLogList": [],  # Will be filled automatically
            "DumpLogListHashStr": None,  # Will be filled automatically
            # # # # # # # # # # # # # # # # # #
        },
        "ServerDict": {
            "WorkingDirectoryPathStr": None,  # Will be filled automatically
            "RequestTimeoutSecFloat": 300,  # Time to handle request in seconds
            "ListenPort_": "Порт, по которому можно подключиться к демону",
            "ListenPort": 80,
            "ListenURLList": [
                {
                    "Description": "Local machine test",
                    "URL_": "Сетевое расположение сервера демона",
                    "URL": ""
                }
            ],
            "AccessUsers": {  # Default - all URL is blocked
                "FlagCredentialsAsk": True,  # Turn on Authentication
                "RuleDomainUserDict": {
                    # ("DOMAIN", "USER"): { !!!!! only in upper case !!!!
                    #    "MethodMatchURLBeforeList": [
                    #       {
                    #           "Method":"GET|POST",
                    #           "MatchType":"BeginWith|Contains|Equal|EqualCase",
                    #           "URL":"",
                    #           "FlagAccessDefRequestGlobalAuthenticate": None, #Return bool
                    #           "FlagAccess": True
                    #        }
                    #    ],
                    #    "ControlPanelKeyAllowedList":[], # If empty - all is allowed
                    #    "RoleHierarchyAllowedDict": {
                    #       "Orchestrator":{
                    #           "Controls": {
                    #               "RestartOrchestrator": {}, # Feature to restart orchestrator on virtual machine
                    #               "LookMachineScreenshots": {} # Feature to look machina screenshots
                    #          },
                    #           "RDPActive": { # Robot RDP active module
                    #               "ListRead": {} # Access to read RDP session list
                    #            }
                    #        }
                    #      }
                    #   }
                },
                "RuleMethodMatchURLBeforeList": [  # General MethodMatchURL list (no domain/user)
                    #       {
                    #           "Method":"GET|POST",
                    #           "MatchType":"BeginWith|Contains|Equal|EqualCase",
                    #           "URL":"",
                    #           "FlagAccessDefRequestGlobalAuthenticate": None, #Return bool
                    #           "FlagAccess": True
                    #        }
                ],
                "AuthTokensDict": {
                    # "<AuthToken>":{"User":"", "Domain":"", "TokenDatetime":<Datetime>, "FlagDoNotExpire":True}
                }
            },
            "URLList": [  # List of available URLs with the orchestrator server
                # {
                #    "Method":"GET|POST",
                #    "URL": "/index", #URL of the request
                #    "MatchType": "", #"BeginWith|Contains|Equal|EqualCase",
                #    "ResponseFilePath": "", #Absolute or relative path
                #    "ResponseFolderPath": "", #Absolute or relative path
                #    "ResponseContentType": "", #HTTP Content-type
                #    "ResponseDefRequestGlobal": None #Function with str result
                # }
                {
                    "Method": "GET",
                    "URL": "/test/",  # URL of the request
                    "MatchType": "BeginWith",  # "BeginWith|Contains|Equal|EqualCase",
                    # "ResponseFilePath": "", #Absolute or relative path
                    "ResponseFolderPath": "C:\Abs\Archive\scopeSrcUL\OpenRPA\Orchestrator\Settings",
                    # Absolute or relative path
                    # "ResponseContentType": "", #HTTP Content-type
                    # "ResponseDefRequestGlobal": None #Function with str result
                }
            ],

        },
        "OrchestratorStart": {
            "DefSettingsUpdatePathList": [],
            # List of the .py files which should be loaded before init the algorythms
            "ActivityList": [
                # {
                #    "Type": "ProcessStop", #Activity type
                #    "Name": "OpenRPARobotDaemon.exe", #Process name
                #    "FlagForce": True, #Force process close
                #    "User": "%username%" #Empty, user or %username%
                # },
                # {
                #     "Type": "ProcessStartIfTurnedOff", #Activity type
                #     "CheckTaskName": "notepad.exe", #Python function module name
                #     "Path": "notepad", #Python function name
                #     "ArgList": [] #Input python function args
                # },
                # {
                #     "Type": "RDPSessionConnect", #Activity type - start/connect RDP Session
                #     "RDPSessionKeyStr": "notepad.exe", #Python function module name
                #     "RDPConfigurationDict": {}
                # },
                # {
                #     "Type": "RDPSessionLogoff", #Activity type - logoff RDP Session
                #     "RDPSessionKeyStr": "notepad.exe", #Python function module name
                # },
                # {
                #     "Type": "RDPSessionDisconnect", #Activity type - disconnect the RDP Session without logoff
                #     "RDPSessionKeyStr": "notepad.exe", #Python function module name
                # },
                # {
                #     "Type": "RDPSessionFileSend", #Activity type - send file to RDP session
                #     ...
                # },
                # {
                #     "Type": "RDPSessionFileRecieve", #Activity type - recieve file from rdp session
                #     ...
                # },
                # {
                #     "Type": "RDPSessionProcessStart", #Activity type -
                #     ...
                # },
            ]
        },
        "SchedulerDict": {
            "CheckIntervalSecFloat": 5.0,  # Check interval in seconds
            "ActivityTimeList": [
                # {
                #    "TimeHH:MMStr": "22:23",  # Time [HH:MM] to trigger activity
                #    "WeekdayList": [0, 1, 2, 3, 4, 5, 6], #List of the weekday index when activity is applicable, Default [0,1,2,3,4,5,6]
                #    "ActivityList": [
                    #    {
                    #        "Type": "ProcessStart",  # Activity type
                    #        "Path": "start",  # Executable file path
                    #        "ArgList": ["cmd.exe", "/c", "PIPUpgrade.cmd"]  # List of the arguments
                    #    }
                #    ],
                #    "GUID": None # Will be filled in Orchestrator automatically - is needed for detect activity completion
                # },
            ],
        },
        "ProcessorDict": {  # Has been changed. New general processor (one threaded) v.1.2.0
            "ActivityList": [  # List of the activities
                # {
                #    "Def":"DefAliasTest", # def link or def alias (look gSettings["Processor"]["AliasDefDict"])
                #    "ArgList":[1,2,3], # Args list
                #    "ArgDict":{"ttt":1,"222":2,"dsd":3} # Args dictionary
                #    "ArgGSettings": # Name of GSettings attribute: str (ArgDict) or index (for ArgList)
                #    "ArgLogger": None # Name of GSettings attribute: str (ArgDict) or index (for ArgList)
                # },
            ],
            "AliasDefDict": {},  # Storage for def with Str alias. To use it see pyOpenRPA.Orchestrator.ControlPanel
            "CheckIntervalSecFloat": 1.0,  # Interval for check gSettings in ProcessorDict > ActivityList
            "ExecuteBool": True,  # Flag to execute thread processor
            "ThreadIdInt": None # Technical field - will be setup when processor init
        },
        "ControlPanelDict": { # Old structure > CPDict
            "RefreshSeconds": 5,  # deprecated parameter
            "RobotList": [
                #{
                #    "RenderFunction": RenderRobotR01,
                #    "KeyStr": "TestControlPanelKey"
                #}
            ]
        },
        "CPDict": {
            # "CPKey": {"HTMLRenderDef":None, "JSONGeneratorDef":None, "JSInitGeneratorDef":None}
        },
        # # # # # # # # # # # # # #
        "RobotRDPActive": {
            "RDPList": {
                # "RDPSessionKey":{
                #    "Host": "77.77.22.22",  # Host address
                #    "Port": "3389",  # RDP Port
                #    "Login": "test",  # Login
                #    "Password": "test",  # Password
                #    "Screen": {
                #        "Width": 1680,  # Width of the remote desktop in pixels
                #        "Height": 1050,  # Height of the remote desktop in pixels
                #        # "640x480" or "1680x1050" or "FullScreen". If Resolution not exists set full screen
                #        "FlagUseAllMonitors": False,  # True or False
                #        "DepthBit": "32"  # "32" or "24" or "16" or "15"
                #    },
                #    "SharedDriveList": ["c"],  # List of the Root sesion hard drives
                #    ###### Will updated in program ############
                #    "SessionHex": "",  # Hex is created when robot runs
                #    "SessionIsWindowExistBool": False, # Flag if the RDP window is exist, old name "FlagSessionIsActive". Check every n seconds
                #    "SessionIsWindowResponsibleBool": False, # Flag if RDP window is responsible (recieve commands). Check every nn seconds. If window is Responsible - window is Exist too
                #    "SessionIsIgnoredBool": False # Flag to ignore RDP window False - dont ignore, True - ignore
                # }
            },
            "ResponsibilityCheckIntervalSec": None,
            # Seconds interval when Robot check the RDP responsibility. if None - dont check
            "FullScreenRDPSessionKeyStr": None,
            # RDPSessionKeyStr of the current session which is full screened, None is no session in fullscreen
            "ActivityList": [
                # Technical Activity list for RobotRDPActive thread - equal to Main activity list, apply only RDP activity
                # {
                #    "DefNameStr":"test", # Function name in RobotRDPActive.Processor
                #    "ArgList":[1,2,3], # Args list
                #    "ArgDict":{"ttt":1,"222":2,"dsd":3} # Args dictionary
                # },
                # {
                #    "DefNameStr": "RDPSessionConnect",  # Function name in RobotRDPActive.Processor
                #    "ArgList": [],  # Args list
                #    "ArgDict": {"inRDPSessionKeyStr": "TestRDP", "inHostStr": "77.44.33.22", "inPortStr": "3389",
                #                "inLoginStr": "login", "inPasswordStr": "pass"}  # Args dictionary
                # },
                # {
                #    "DefNameStr": "RDPSessionDisconnect",  # Disconnect the RDP session without logoff. Function name in RobotRDPActive.Processor
                #    "ArgList": [],  # Args list
                #    "ArgDict": {"inRDPSessionKeyStr": "TestRDP"}
                # },
                # {
                #    "DefNameStr": "RDPSessionReconnect",  # Disconnect the RDP session without logoff. Function name in RobotRDPActive.Processor
                #    "ArgList": [],  # Args list
                #    "ArgDict": {"inRDPSessionKeyStr": "TestRDP"}
                # }
            ]
        },
        # # # # # # # # # # # # # #
        "FileManager": {
            "FileURLFilePathDict_help": "https://localhost:8081/filemanager/<file URL>. All FileURL s must be set in lowercase",
            "FileURLFilePathDict": {
                #"r01/report.xlsx": "C:\\RPA\\R01_IntegrationOrderOut\\Data\\Reestr_otgruzok.xlsx"
            }
        },
        "Logger": logging.getLogger("Orchestrator"),
        "Storage": {
            "Robot_R01_help": "Robot data storage in orchestrator env",
            "Robot_R01": {},
            "R01_OrchestratorToRobot": {"Test2": "Test2"}
        },
        "AgentDict": { # Will be filled when program runs
            #("HostNameUpperStr", "UserUpperStr"): { "IsListenBool": True, "QueueList": [] }
        }
    }

# Create full configuration for
def __AgentDictItemCreate__():
    return {"IsListenBool":False, "ConnectionCountInt":0, "ConnectionFirstQueueItemCountInt":0, "ActivityList":[]}
# Create full configuration for
def __UACClientAdminCreate__():
    lResultDict = {
        "pyOpenRPADict":{
            "CPKeyDict":{ # Empty dict - all access
                # "CPKeyStr"{
                # }
            },
            "RDPKeyDict":{ # Empty dict - all access
                #"RDPKeyStr"{
                #   "FullscreenBool": True,
                #   "IgnoreBool":True,
                #   "ReconnectBool": True
                #   "NothingBool": True # USe option if you dont want to give some access to the RDP controls
                # }
            },
            "AgentKeyDict": { # Empty dict - all access
                # "AgentKeyStr"{
                # }
            },
            "AdminDict":{ # Empty dict - all access
                "LogViewerBool":True, # Show log viewer on the web page
                "CMDInputBool":True, # Execute CMD on the server side and result to the logs
                "ScreenshotViewerBool":True, # Show button to look screenshots
                "RestartOrchestratorBool": True, # Restart orchestrator activity
                "RestartOrchestratorGITPullBool": True, # Turn off (RDP remember) orc + git pull + Turn on (rdp remember)
                "RestartPCBool": True, # Send CMD to restart pc
                "NothingBool":True # USe option if you dont want to give some access to the RDP controls
            },
            "ActivityDict": { # Empty dict - all access
                "ActivityListExecuteBool": True,  # Execute activity at the current thread
                "ActivityListAppendProcessorQueueBool": True  # Append activity to the processor queue
            }
        }

    }
    return lResultDict


# Init the log dump to WEB
# import pdb; pdb.set_trace()
############################################
def LoggerDumpLogHandlerAdd(inLogger, inGSettingsClientDict):
    lL = inLogger
    if len(lL.handlers) == 0:
        mRobotLoggerFormatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    else:
        mRobotLoggerFormatter = lL.handlers[0].formatter
    mHandlerDumpLogList = LoggerHandlerDumpLogList.LoggerHandlerDumpLogList(inDict=inGSettingsClientDict,
        inKeyStr="DumpLogList", inHashKeyStr="DumpLogListHashStr", inRowCountInt=inGSettingsClientDict[
                                                                                "DumpLogListCountInt"])
    mHandlerDumpLogList.setFormatter(mRobotLoggerFormatter)
    lL.addHandler(mHandlerDumpLogList)

# inModeStr:
#   "BASIC" - create standart configuration
from pyOpenRPA.Orchestrator.Utils import LoggerHandlerDumpLogList
def Create(inModeStr="BASIC"):
    if inModeStr=="BASIC":
        lResult = __Create__() # Create settings
        # Создать файл логирования
        # add filemode="w" to overwrite
        if not os.path.exists("Reports"):
            os.makedirs("Reports")
        ##########################
        # Подготовка логгера Robot
        #########################
        mRobotLogger = lResult["Logger"]
        mRobotLogger.setLevel(logging.INFO)
        # create the logging file handler
        mRobotLoggerFH = logging.FileHandler(
            "Reports\\" + datetime.datetime.now().strftime("%Y_%m_%d") + ".log")
        mRobotLoggerFormatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
        mRobotLoggerFH.setFormatter(mRobotLoggerFormatter)
        # add handler to logger object
        mRobotLogger.addHandler(mRobotLoggerFH)
        ####################Add console output
        handler = logging.StreamHandler(sys.stdout)
        handler.setFormatter(mRobotLoggerFormatter)
        mRobotLogger.addHandler(handler)
        ############################################
        LoggerDumpLogHandlerAdd(inLogger=mRobotLogger, inGSettingsClientDict=lResult["Client"])
        #mHandlerDumpLogList = LoggerHandlerDumpLogList.LoggerHandlerDumpLogList(inDict=lResult["Client"],
        #                                                                        inKeyStr="DumpLogList",
        #                                                                        inHashKeyStr="DumpLogListHashStr",
        #                                                                        inRowCountInt=lResult["Client"][
        #                                                                            "DumpLogListCountInt"])
        #mHandlerDumpLogList.setFormatter(mRobotLoggerFormatter)
        #mRobotLogger.addHandler(mHandlerDumpLogList)
    return lResult # return the result dict