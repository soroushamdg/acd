import os

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
            os.chdir(exe_path+r'/temp/cache')
        except:
            os.chdir(exe_path)
            os.mkdir('temp')
            os.chdir(exe_path+'/temp')
            os.mkdir('cache')
        else:
            temp_path = exe_path + "/temp/cache" + '/'
            break
#define export path
def define_export_path(exe_path):
    global mp4_export_path
    desktop_path = os.environ["HOMEPATH"] + '/Desktop'
    for i in range(1):
        try:
            os.chdir(desktop_path+'/exports')
        except:
            os.chdir(desktop_path)
            os.mkdir('exports')
        else:
            mp4_export_path = desktop_path+'/exports/'
            break

def check_export_and_temp_dirs(exe_path):
    global temp_path
    for i in range(1):
        try:
            os.chdir(temp_path)
        except:
            os.chdir(exe_path)
            os.mkdir('temp')
            os.chdir(exe_path + '/temp')
            os.mkdir('cache')
        else:
            temp_path = exe_path + "/temp/cache" + '/'
            break

    global mp4_export_path
    desktop_path = '/'.join(os.environ["HOMEPATH"].split('\\'))+'/Desktop'
    for i in range(1):
        try:
            os.chdir(mp4_export_path)
        except:
            os.chdir(desktop_path)
            os.mkdir('exports')
        else:
            mp4_export_path = desktop_path + '/exports/'
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
        size = os.path.getsize(temp_path + filename)
    except:
        return False
    else:
        return size

def make_folder_to_export_into(coursename):
    try:
        os.chdir(mp4_export_path)
        os.mkdir(mp4_export_path+coursename)
    except:
        return False
    else:
        return True
