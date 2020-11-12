import subprocess,sys,os,pathlib
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

# subprocess.call(['pyinstaller',
#                  '--name',
#                  'acd',
#                  '--onefile',
#                  '-w',
#                  '--icon=acd_logo_Mzn_icon.ico'
#                  '--add-data', '"_acd_logo_1.png"', '--add-data', '"_acd_logo_icon.png"', '--add-data', '"acd_logo_Mzn_icon.ico"',
#                  '--add-data' ,'"bug.png"', '--add-data', '"github.png"', '"--add-data"', '"it.png"', '--add-data', '"ok.png"'
#                  ])
def compile():
    if sys.platform == 'win32':
        print(" ".join(['pyinstaller',
                         "--distpath='EXPORTS'",
                         # '--clean',
                     '--name',
                     'ACD-Launcher',
                     '--onefile',
                     f"--icon={iconpath}",
                         r"--paths=venv\Lib\site-packages",
                         r'--hidden-import=tldextract', r'--hidden-import=pkgutil'
                     # '--specpath',
                     # 'datas.spec'
                     ]+data_cmd+['main.py']))
        subprocess.call(['pyinstaller',
                         "--distpath='EXPORTS'",
                         # '--clean',
                     '--name',
                     'ACD-Launcher',
                     # '--onefile',
                     f"--icon={iconpath}",
                         r"--paths=venv\Lib\site-packages",
                         r'--hidden-import=tldextract', r'--hidden-import=pkgutil'
                     # '--specpath',
                     # 'datas.spec'
                     ]+data_cmd+['main.py'],shell=False)
    elif sys.platform == 'darwin':
        # --add-binary = '/System/Library/Frameworks/Tk.framework/Tk':'tk' --add-binary = '/System/Library/Frameworks/Tcl.framework/Tcl':'tcl'
        print(' '.join(['pyinstaller',
                            ' main.py',
                            "--distpath='EXPORTS'",
                            '--windowed',
                            '-y',
                            # '--clean',
                            # '-F',
                            '--name',
                            'ACD-Launcher',
                            # '--onefile',
                            f"--icon={iconpath}",
                            r"--paths=venv\Lib\site-packages",
                            r'--hidden-import=tldextract', r'--hidden-import=pkgutil'
                            # '--specpath',
                            # 'datas.spec'
                            ] + data_cmd) + r" --add-binary='/System/Library/Frameworks/Tk.framework/Tk':'tk' --add-binary='/System/Library/Frameworks/Tcl.framework/Tcl':'tcl'")

        os.system(' '.join(['pyinstaller',
                            ' main.py',
                            "--distpath='EXPORTS'",
                            '--windowed',
                            '-y',
                            # '--clean',
                            # '-F',
                            '--name',
                            'ACD-Launcher',
                            '--onefile',
                            f"--icon={iconpath}",
                            r"--paths=venv\Lib\site-packages",
                            r'--hidden-import=tldextract', r'--hidden-import=pkgutil'
                            # '--specpath',
                            # 'datas.spec'
                            ] + data_cmd) + r" --add-binary='/System/Library/Frameworks/Tk.framework/Tk':'tk' --add-binary='/System/Library/Frameworks/Tcl.framework/Tcl':'tcl'")
    else:
        print(' '.join(['pyinstaller',
                            ' main.py',
                         '--name',
                         'ACD-Launcher',
                         '--onefile',
                         iconpath,
                         # '--specpath',
                         # 'datas.spec'
                         ]) + ' '.join(data_cmd) )
        os.system(' '.join(['pyinstaller',
                            ' main.py',
                         '--name',
                         'ACD-Launcher',
                         '--onefile',
                            f"--icon={iconpath}",
                            r"--paths=venv\Lib\site-packages",
                            r'--hidden-import=tldextract', r'--hidden-import=pkgutil'
                            # '--specpath',
                         # 'datas.spec'
                         ] + data_cmd))
