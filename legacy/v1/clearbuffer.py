import sys,os
def clear_buffer():
    if sys.platform == 'win32':
        for _ in range(20):
            os.system('cls')
    elif sys.platform == 'darwin':
        for _ in range(20):
            os.system('clear')
    else:
        for _ in range(20):
            os.system('clear')
