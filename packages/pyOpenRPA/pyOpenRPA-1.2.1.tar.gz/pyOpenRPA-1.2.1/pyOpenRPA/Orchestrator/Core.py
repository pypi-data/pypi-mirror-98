import threading

# Check if current execution is in Processor thread
def IsProcessorThread(inGSettings):
    return inGSettings["ProcessorDict"]["ThreadIdInt"] == threading.get_ident()