import threading, socket, getpass, sys, uuid, subprocess, base64
from . import O2A, A2O # Data flow Orchestrator To Agent
from . import Processor # Processor Queue

# Create binary file by the base64 string (safe for JSON transmition)
def OSFileBinaryDataBase64StrCreate(inFilePathStr, inFileDataBase64Str,inGSettings = None):
    """ Create binary file by the base64 string (safe for JSON transmition)"""
    lFile = open(inFilePathStr, "wb")
    lFile.write(base64.b64decode(inFileDataBase64Str))
    lFile.close()
    lL = inGSettings.get("Logger", None) if type(inGSettings) is dict else None
    lMessageStr = f"AGENT Binary file {inFilePathStr} has been created."
    if lL: lL.info(lMessageStr)
    A2O.LogListSend(inGSettings=inGSettings, inLogList=[lMessageStr])

# Create text file by the string
def OSFileTextDataStrCreate(inFilePathStr, inFileDataStr, inEncodingStr = "utf-8",inGSettings = None):
    lFile = open(inFilePathStr, "w", encoding=inEncodingStr)
    lFile.write(inFileDataStr)
    lFile.close()
    lL = inGSettings.get("Logger", None) if type(inGSettings) is dict else None
    lMessageStr = f"AGENT Text file {inFilePathStr} has been created."
    if lL: lL.info(lMessageStr)
    A2O.LogListSend(inGSettings=inGSettings, inLogList=[lMessageStr])

# Send CMD to OS. Result return to log + Orchestrator by the A2O connection
def OSCMD(inCMDStr, inRunAsyncBool=True, inGSettings = None):
    lResultStr = ""
    # Subdef to listen OS result
    def _CMDRunAndListenLogs(inCMDStr, inGSettings = None):
        lL = inGSettings.get("Logger",None) if type(inGSettings) is dict else None
        lResultStr = ""
        lOSCMDKeyStr = str(uuid.uuid4())[0:4].upper()
        lCMDProcess = subprocess.Popen(f'cmd /c {inCMDStr}', stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        lListenBool = True
        lMessageStr = f"{lOSCMDKeyStr}: # # # # AGENT CMD Process has been STARTED # # # # "
        if lL: lL.info(lMessageStr)
        A2O.LogListSend(inGSettings=inGSettings,inLogList=[lMessageStr])
        lMessageStr = f"{lOSCMDKeyStr}: {inCMDStr}"
        if lL: lL.info(lMessageStr)
        A2O.LogListSend(inGSettings=inGSettings, inLogList=[lMessageStr])
        while lListenBool:
            lOutputLineBytes = lCMDProcess.stdout.readline()
            if lOutputLineBytes == b"":
                lListenBool = False
            lStr = lOutputLineBytes.decode('cp866')
            if lStr.endswith("\n"): lStr = lStr[:-1]
            lMessageStr = f"{lOSCMDKeyStr}: {lStr}"
            if lL: lL.info(lMessageStr)
            A2O.LogListSend(inGSettings=inGSettings, inLogList=[lMessageStr])
            lResultStr+=lStr
        lMessageStr = f"{lOSCMDKeyStr}: # # # # AGENT CMD Process has been FINISHED # # # # "
        if lL: lL.info(lMessageStr)
        A2O.LogListSend(inGSettings=inGSettings, inLogList=[lMessageStr])
        return lResultStr
    # New call
    if inRunAsyncBool:
        lThread = threading.Thread(target=_CMDRunAndListenLogs, kwargs={"inCMDStr":inCMDStr, "inGSettings":inGSettings})
        lThread.start()
        lResultStr="ActivityList has been started in async mode - no output is available here."
    else:
        lResultStr = _CMDRunAndListenLogs(inCMDStr=inCMDStr, inGSettings=inGSettings)
    #lCMDCode = "cmd /c " + inCMDStr
    #subprocess.Popen(lCMDCode)
    #lResultCMDRun = 1  # os.system(lCMDCode)
    return lResultStr


# Main def
def Agent(inGSettings):
    lL = inGSettings["Logger"]

    # Append Orchestrator def to ProcessorDictAlias
    lModule = sys.modules[__name__]
    lModuleDefList = dir(lModule)
    for lItemDefNameStr in lModuleDefList:
        # Dont append alias for defs Agent
        if lItemDefNameStr not in ["Agent"]:
            lItemDef = getattr(lModule,lItemDefNameStr)
            if callable(lItemDef): inGSettings["ProcessorDict"]["AliasDefDict"][lItemDefNameStr]=lItemDef

    # Detect Machine host name and username
    inGSettings["AgentDict"]["HostNameUpperStr"] = socket.gethostname().upper()
    inGSettings["AgentDict"]["UserUpperStr"] = getpass.getuser().upper()

    # Processor thread
    lProcessorThread = threading.Thread(target= Processor.ProcessorRunSync, kwargs={"inGSettings":inGSettings})
    lProcessorThread.daemon = True # Run the thread in daemon mode.
    lProcessorThread.start() # Start the thread execution.
    if lL: lL.info("Processor has been started (ProcessorDict)")  #Logging

    # Start thread to wait data from Orchestrator (O2A)
    lO2AThread = threading.Thread(target=O2A.O2A_Loop, kwargs={"inGSettings":inGSettings})
    lO2AThread.start()

    # Send log that Agent has been started
    A2O.LogListSend(inGSettings=inGSettings, inLogList=[f'Host: {inGSettings["AgentDict"]["HostNameUpperStr"]}, User: {inGSettings["AgentDict"]["UserUpperStr"]}, Agent has been started.'])