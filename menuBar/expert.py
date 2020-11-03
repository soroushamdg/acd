import platform
from settings import reset_program
architect = platform.machine()
running_platform = platform.platform()
system = platform.system()
processor = platform.processor()

def resetACD(appexit):
    reset_program(appexit)
