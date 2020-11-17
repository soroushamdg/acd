import subprocess,sys,os,pathlib
import time
from settings import DEBUG,SETTINGS


def return_directory_tree(dirname):
    listOfFiles = list()
    for (dirpath, dirnames, filenames) in os.walk(dirname):
        listOfFiles += [(dirpath,os.path.join(dirpath, file)) for file in filenames]
    return listOfFiles
iconpath = 'mac_launcher_icon.icns' if sys.platform == 'darwin' else 'launcher_icon.ico'
# iconpath = 'launcher_icon.ico' if sys.platform == 'darwin' else 'launcher_icon.ico'

# data_filenames = [r for directory in ['src',str(pathlib.Path('shiftIO').joinpath('grabber'))] for r in return_directory_tree(directory)]
data_filenames = [('src','src'),('shiftIO/grabber','shiftIO/grabber'),('shiftIO/grabber/assets','shiftIO/grabber/assets')]
data_cmd = ['--add-binary=' + f"{filename}"+f';{dirpath}' for dirpath,filename in data_filenames] if sys.platform == 'win32' else [' --add-data=' + f"{filename}"+f":'{dirpath}'" for dirpath,filename in data_filenames]
# data_cmd = ['--add-binary=' + f"{filename}" for dirpath,filename in data_filenames] if sys.platform == 'win32' else [' --add-data=' + f"'{filename}'"+":'DATA'" for filename in data_filenames]

def compile():
    if DEBUG:
        print('Please change settings DEBUG to False and logging.INFO')
        return

    start_time = time.time()
    if sys.platform == 'win32':

        windows_args = ['pyinstaller',
                         "--distpath='EXPORTS'",
                         # '--clean',
                        '-w',
                     '--name',
                     'ACD-Launcher',
                     '--onefile',
                     f"--icon={iconpath}",
                         r"--paths=venv\Lib\site-packages",
                        #  r'--hidden-import=tldextract',
                        # r'--hidden-import=pkgutil'
                     # '--specpath',
                     # 'datas.spec'
                     ]+data_cmd+['main.py']
        print(" ".join(windows_args))
        subprocess.call(windows_args, shell=False)

    elif sys.platform == 'darwin':

        macos_args = ['pyinstaller',
                            ' main.py',
                            "--distpath='EXPORTS'",
                            '--windowed',
                            '-y', #confirm replace
                            '--clean',
                            # '-F',
                            '--name',
                            'ACD-Launcher',
                            '--onefile',
                            f"--icon={iconpath}",
                            r"--paths=venv\Lib\site-packages",
                            r'--hidden-import=tldextract', r'--hidden-import=pkgutil'
                            # '--specpath',
                            # 'datas.spec'
                            ] + data_cmd + [r" --add-binary='/System/Library/Frameworks/Tk.framework/Tk':'tk' --add-binary='/System/Library/Frameworks/Tcl.framework/Tcl':'tcl'"]
        print(' '.join(macos_args))
        os.system(' '.join(macos_args))
    else:

        linux_args = ['pyinstaller',
                            ' main.py',
                      "--distpath='EXPORTS'",
                      '--windowed',
                      '-y',  # confirm replace
                         '--name',
                         'ACD-Launcher',
                         '--onefile',
                            f"--icon={iconpath}",
                            r"--paths=venv\Lib\site-packages",
                      # r'--hidden-import=tldextract',
                      # r'--hidden-import=pkgutil'
                      # '--specpath',
                      # 'datas.spec'
                      ] + data_cmd
        print(' '.join(linux_args))
        os.system(' '.join(linux_args))
    print(f"Compile finished in : {int((time.time()-start_time)/60)}:{int((time.time()-start_time)%60)} ")
