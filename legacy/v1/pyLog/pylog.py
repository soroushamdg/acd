# initiating logger object
from pyLog import logger
log = logger.logger()

def stop():
    log.close_file()
