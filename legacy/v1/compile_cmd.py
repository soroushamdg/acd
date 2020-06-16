import subprocess,sys,os
data_filenames=['_acd_logo_1.png','_acd_logo_icon.png','acd_logo_Mzn_icon.ico','bug.png','github.png','it.png','ok.png']
data_cmd = ['--add-binary=' + filename+';DATA' for filename in data_filenames] if sys.platform == 'win32' else [' --add-binary=' + f"'{filename}'"+":'DATA'" for filename in data_filenames]
# subprocess.call(['pyinstaller',
#                  '--name',
#                  'acd',
#                  '--onefile',
#                  '-w',
#                  '--icon=acd_logo_Mzn_icon.ico'
#                  '--add-data', '"_acd_logo_1.png"', '--add-data', '"_acd_logo_icon.png"', '--add-data', '"acd_logo_Mzn_icon.ico"',
#                  '--add-data' ,'"bug.png"', '--add-data', '"github.png"', '"--add-data"', '"it.png"', '--add-data', '"ok.png"'
#                  ])
if sys.platform == 'win32':
    subprocess.call(['pyinstaller',
                 '--name',
                 'ACD-Launcher',
                 '--onefile',
                 '--icon=acd_logo_Mzn_icon.ico',
                 # '--specpath',
                 # 'datas.spec'
                 ]+data_cmd+['main.py'],shell=False)
elif sys.platform == 'darwin':
    # --add-binary = '/System/Library/Frameworks/Tk.framework/Tk':'tk' --add-binary = '/System/Library/Frameworks/Tcl.framework/Tcl':'tcl'
    print(' '.join(['pyinstaller',
                    ' main.py',
                    '--name',
                    'ACD-Launcher',
                    '--onefile',
                    '--icon=acd_logo_Mzn_icon.ico',
                    # '--specpath',
                    # 'datas.spec'
                    ]) + ' '.join(data_cmd)+ r" --add-binary='/System/Library/Frameworks/Tk.framework/Tk':'tk' --add-binary='/System/Library/Frameworks/Tcl.framework/Tcl':'tcl'")
    os.system(' '.join(['pyinstaller',
                        ' main.py',
                        '--windowed',
                        '-y',
                        '--clean',
                        '-F',
                        '--name',
                        'ACD-Launcher',
                        '--onefile',
                        '--icon=acd_logo_Mzn_icon.ico',
                        # '--specpath',
                        # 'datas.spec'
                        ]) + ' '.join(data_cmd) +  r" --add-binary='/System/Library/Frameworks/Tk.framework/Tk':'tk' --add-binary='/System/Library/Frameworks/Tcl.framework/Tcl':'tcl'")
else:
    print(' '.join(['pyinstaller',
                        ' main.py',
                     '--name',
                     'ACD-Launcher',
                     '--onefile',
                     '--icon=acd_logo_Mzn_icon.ico',
                     # '--specpath',
                     # 'datas.spec'
                     ]) + ' '.join(data_cmd) )
    os.system(' '.join(['pyinstaller',
                        ' main.py',
                     '--name',
                     'ACD-Launcher',
                     '--onefile',
                     '--icon=acd_logo_Mzn_icon.ico',
                     # '--specpath',
                     # 'datas.spec'
                     ]) + ' '.join(data_cmd) )
