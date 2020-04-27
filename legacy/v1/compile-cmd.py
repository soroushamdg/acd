import subprocess
data_filenames=['_acd_logo_1.png','_acd_logo_icon.png','acd_logo_Mzn_icon.ico','bug.png','github.png','it.png','ok.png']
data_cmd = ['--add-binary=' + filename+';DATA' for filename in data_filenames]
# subprocess.call(['pyinstaller',
#                  '--name',
#                  'acd',
#                  '--onefile',
#                  '-w',
#                  '--icon=acd_logo_Mzn_icon.ico'
#                  '--add-data', '"_acd_logo_1.png"', '--add-data', '"_acd_logo_icon.png"', '--add-data', '"acd_logo_Mzn_icon.ico"',
#                  '--add-data' ,'"bug.png"', '--add-data', '"github.png"', '"--add-data"', '"it.png"', '--add-data', '"ok.png"'
#                  ])
subprocess.call(['pyinstaller',
                 '--name',
                 'ACD-Launcher',
                 '--onefile',
                 '--icon=acd_logo_Mzn_icon.ico',
                 # '--specpath',
                 # 'datas.spec'
                 ]+data_cmd+['main.py'])