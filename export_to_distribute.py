import sys
import time
from os.path import basename
from zipfile import ZipFile
import os
from compile_cmd import compile
import pathlib

def get_platform_architecture():
    if sys.platform.startswith('linux') and sys.maxsize > 2 ** 32:
        platform = 'linux'
        architecture = '64'
    elif sys.platform == 'darwin':
        platform = 'mac'
        architecture = '64'
    elif sys.platform.startswith('win'):
        platform = 'win'
        architecture = '32'
    else:
        raise RuntimeError('Could not determine chromedriver download URL for this platform.')
    return platform+architecture

tutorials = [pathlib.Path().joinpath("Design").joinpath("Tutorial Videos").joinpath("ac_tutorial_low.mp4"),
             pathlib.Path().joinpath("Design").joinpath("Tutorial Videos").joinpath("acd_shiftio_tutorial_low.mp4")]

if __name__ == "__main__":
    print('Starting...')
    start = time.time()
    # Compile Binary
    compile()

    # Create zip file
    print('Zipping...')
    if pathlib.Path("EXPORTS").exists():
        filename = os.listdir("EXPORTS")[0]
        zipfile = ZipFile(pathlib.Path("GITHUB").joinpath("RELEASE").joinpath(f"acd_{get_platform_architecture()}.zip"),'w')
        zipfile.write(pathlib.Path("'EXPORTS'").joinpath(filename),basename(filename))

    elif pathlib.Path("'EXPORTS'").exists():
        filename = os.listdir("'EXPORTS'")[0]
        zipfile = ZipFile(pathlib.Path("GITHUB").joinpath("RELEASE").joinpath(f"acd_{get_platform_architecture()}.zip"),'w')
        zipfile.write(pathlib.Path("'EXPORTS'").joinpath(filename),basename(filename))
    else:
        print("NO EXPORTS FOLDER")

    for file in tutorials:
        zipfile.write(file,basename(file))

    print(f"Process finished in : {int((time.time()-start)/60)}:{int((time.time()-start)%60)} ")


