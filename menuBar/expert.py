import platform
from settings import reset_program
architect = platform.machine()
running_platform = platform.platform()
system = platform.system()
processor = platform.processor()

def resetACD():
    reset_program()
