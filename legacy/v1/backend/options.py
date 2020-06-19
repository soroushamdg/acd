import os,pathlib

script_name = "adc-dl-bc-20420"
driver_path = ''
temp_path = ''
ffmpeg_directory_bin = ''
mp4_export_path = ''

#define temp path
def define_temp_path(exe_path):
    global temp_path
    for i in range(1):
        try:
            os.chdir(str(pathlib.Path(exe_path).joinpath('temp').joinpath('cache').joinpath(' '))[:-1])
        except:
            os.chdir(str(pathlib.Path(exe_path)))
            os.mkdir('temp')
            os.chdir(str(pathlib.Path(exe_path).joinpath('temp')))
            os.mkdir('cache')
        else:
            temp_path = str(pathlib.Path(exe_path).joinpath('temp').joinpath('cache'))
            break

#define export path
def define_export_path(exe_path):
    global mp4_export_path
    desktop_path = str(pathlib.Path().home().joinpath('Desktop'))
    for i in range(1):
        try:
            os.chdir(str(pathlib.Path(desktop_path).joinpath('exports')))
        except:
            os.chdir(str(pathlib.Path(desktop_path)))
            os.mkdir('exports')
        else:
            mp4_export_path = str(pathlib.Path(desktop_path).joinpath('exports').joinpath(' '))[:-1]
            break

def check_export_and_temp_dirs(exe_path):
    global temp_path
    for i in range(1):
        try:
            os.chdir(temp_path)
        except:
            os.chdir(str(pathlib.Path(exe_path)))
            os.mkdir('temp')
            os.chdir(str(pathlib.Path(exe_path).joinpath('temp')))
            os.mkdir('cache')
        else:
            temp_path = str(pathlib.Path(exe_path).joinpath('temp').joinpath('cache').joinpath(' '))[:-1]
            break

    global mp4_export_path
    desktop_path = str(pathlib.Path().home().joinpath('Desktop'))
    for i in range(1):
        try:
            os.chdir(str(pathlib.Path(desktop_path).joinpath('exports')))
        except:
            os.chdir(str(pathlib.Path(desktop_path)))
            os.mkdir('exports')
        else:
            mp4_export_path = str(pathlib.Path(desktop_path).joinpath('exports').joinpath(' '))[:-1]
            break


def remove_old_files_in_cache(filename):
    if os.listdir(temp_path):
        for file in os.listdir(temp_path):
            if filename.lower() in file.lower():
                try:
                    os.remove(temp_path+file)
                except Exception as msg:
                    print(msg)
                    return False
    return True

def get_file_size_in_cache(filename):
    try:
        size = os.path.getsize(pathlib.Path(temp_path).joinpath(filename))
    except:
        return False
    else:
        return size

def make_folder_to_export_into(coursename):
    try:
        os.chdir(mp4_export_path)
        os.mkdir(coursename)
    except:
        return False
    else:
        return True
