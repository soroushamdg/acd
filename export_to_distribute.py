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


def mac_sign_exported_app():
    print("Start signing STAGE -> 1")
    sign_command = [
        'codesign',
        '-s',
        'Jupiter',
        '-v',
        '--deep',
        '--timestamp',
        '--entitlements',
        'EXPORTS/entitlements.plist',
         '-o',
        'runtime',
        "EXPORTS/ACD-Launcher.app"
    ]
    print(' '.join(sign_command))
    os.system(' '.join(sign_command))
    print("Finished siging STAGE -> 1")
    print("Starting siging STAGE -> 2")
    sign_command = ['ditto',
 '-c',
 '-k',
 '--keepParent',
 '"EXPORTS/ACD-Launcher.app"',
 'EXPORTS/ACD.zip',
 'xcrun',
 'altool',
 '--notarize-app',
 '-t',
 'osx',
 '-f',
 'EXPORTS/ACD.zip',
 '--primary-bundle-id',
 'com.acd.acdlauncher',
 '-u',
 'soroushdev@outlook.com',
 '--password',
 '"@keychain:AC_PASSWORD"']
    print(' '.join(sign_command))
    os.system(' '.join(sign_command))
    print("Finished siging STAGE -> 2")
    print("Starting siging STAGE -> 3")
    sign_command = ['xcrun', 'stapler', 'staple', '"EXPORTS/ACD-Launcher.app"']
    print(' '.join(sign_command))
    os.system(' '.join(sign_command))
    print("Finished siging STAGE -> 3")
    print("Starting siging STAGE -> 4")
    sign_command = ['spctl',
 '--assess',
 '--type',
 'execute',
 '-vvv',
 '"EXPORTS/ACD-Launcher.app"']
    print(' '.join(sign_command))
    os.system(' '.join(sign_command))
    print("Finished siging STAGE -> 4")




if __name__ == "__main__":
    print('Starting...')
    start = time.time()
    # Compile Binary
    compile()

    if sys.platform == 'darwin':
        print("Starting to sign...")
        mac_sign_exported_app()
        print("Ended siging")



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


