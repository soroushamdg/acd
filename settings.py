import logging
import os
import sys,pathlib
import json
from cryptography.fernet import Fernet
from exeinfo import BUILD_NUMBER
import random,string

DEBUG = False
CHECK_NEW_VERSION = False

def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

def get_random_string(length=16):
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(length))

def return_temp_path(DEBUG = DEBUG,filename=None):
    if not DEBUG:
        pathlib.Path(os.path.realpath(__file__)).parent.parent.joinpath('ACDTEMP').mkdir(parents=True, exist_ok=True)
        return str(pathlib.Path(os.path.realpath(__file__)).parent.parent.joinpath('ACDTEMP').joinpath(filename)) if filename else str(pathlib.Path(os.path.realpath(__file__)).parent.parent.joinpath('ACDTEMP'))
    else:
        pathlib.Path(application_path()).joinpath('ACD_EXPORTS').joinpath('ACDTEMP').mkdir(parents=True, exist_ok=True)
        return str(pathlib.Path(application_path()).joinpath('ACD_EXPORTS').joinpath('ACDTEMP').joinpath(filename)) if filename else str(pathlib.Path(application_path()).joinpath('ACD_EXPORTS').joinpath('ACDTEMP'))

def application_path(DEBUG = DEBUG):
    config_name = 'myapp.cfg'

    # determine if application is a script file or frozen exe
    if getattr(sys, 'frozen', True):
        application_path = os.path.dirname(sys.executable)
    elif __file__:
        application_path = os.path.dirname(__file__)

    config_path = os.path.join(application_path, config_name)
    return str(pathlib.Path(config_path).parent) if not DEBUG else str(pathlib.Path(config_path).parent.parent.parent.joinpath('DEBUG'))

def return_shiftio_assets_path(DEBUG = DEBUG, html=False):
    if html:
        return resource_path(
            str(pathlib.Path().joinpath('shiftIO').joinpath('grabber').joinpath('index.html'))) if not DEBUG else str(
            pathlib.Path(application_path()).parent.joinpath('shiftIO').joinpath('grabber').joinpath('index.html'))
    else:
        return resource_path(str(pathlib.Path().joinpath('shiftIO').joinpath('grabber').joinpath('assets'))) if not DEBUG else str(pathlib.Path(application_path()).parent.joinpath('shiftIO').joinpath('grabber').joinpath('assets'))

def src_path(src_name,DEBUG = DEBUG):
    config_name = 'myapp.cfg'

    # determine if application is a script file or frozen exe
    if getattr(sys, 'frozen', True):
        application_path = os.path.dirname(sys.executable)
    elif __file__:
        application_path = os.path.dirname(__file__)

    config_path = os.path.join(application_path, config_name)

    return resource_path(str(pathlib.Path().joinpath('src').joinpath(src_name))) if not DEBUG else str(
        pathlib.Path(config_path).parent.parent.parent.joinpath('src').joinpath(src_name))

def check_or_create_exports_folder(DEBUG = DEBUG):
    if not DEBUG:
        try:
            if not pathlib.Path(SETTINGS['MAIN_EXPORT_PATH']).exists():
                pathlib.Path(SETTINGS['MAIN_EXPORT_PATH']).mkdir(parents=True, exist_ok=True)
                pathlib.Path(SETTINGS['MAIN_EXPORT_PATH']).joinpath('ADOBE CONNECT').mkdir(parents=True, exist_ok=True)
                pathlib.Path(SETTINGS['MAIN_EXPORT_PATH']).joinpath('Transfers').mkdir(parents=True, exist_ok=True)
                pathlib.Path(SETTINGS['FTP_EXPORT_PATH']).joinpath('FTP').mkdir(parents=True, exist_ok=True)

        except Exception as msg:
            logging.debug(msg)
            logging.error('ERROR IN CREATING EXPORTS FOLDER')
            return False
        else:
            return True
    else:
        try:
            if not pathlib.Path(application_path()).joinpath('MAIN_EXPORT_PATH').exists():
                pathlib.Path(application_path()).joinpath('ACD_EXPORTS').mkdir(parents=True, exist_ok=True)
                pathlib.Path(application_path()).joinpath('ACD_EXPORTS').joinpath('ADOBE CONNECT').mkdir(parents=True, exist_ok=True)
                pathlib.Path(application_path()).joinpath('ACD_EXPORTS').joinpath('Transfers').mkdir(parents=True, exist_ok=True)
                pathlib.Path(application_path()).joinpath('ACD_EXPORTS').joinpath('FTP').mkdir(parents=True, exist_ok=True)


        except Exception as msg:
            logging.debug(msg)
            logging.error('ERROR IN CREATING EXPORTS FOLDER')
            return False
        else:
            SETTINGS['MAIN_EXPORT_PATH'] = str(pathlib.Path(application_path()).joinpath('ACD_EXPORTS'))
            SETTINGS['EXPORT_PATH'] = str(pathlib.Path(application_path()).joinpath('ACD_EXPORTS').joinpath('ADOBE CONNECT'))
            SETTINGS['SHIFTIO_EXPORT_PATH'] = str(pathlib.Path(application_path()).joinpath('ACD_EXPORTS').joinpath('Transfers'))
            SETTINGS['FTP_EXPORT_PATH'] = str(pathlib.Path(application_path()).joinpath('ACD_EXPORTS').joinpath('FTP'))

            return True

def reset_program():
    try:
        os.remove(SETTINGS['ACD_ENGINE_PATH'])
    except Exception as msg:
        pass
    try:
        os.remove(SETTINGS['ENGINE_COOKIE_PATH'])
    except:
        pass
    try:
        os.remove(SETTINGS['SETTINGS_PATH'])
    except:
        pass

def clear_cache():
    try:
        os.remove(SETTINGS['ENGINE_COOKIE_PATH'])
    except:
        pass
    try:
        os.remove(SETTINGS['ENGINE_DUMP_PATH'])
    except:
        pass

# Default settings dictionary
SETTINGS = {
    'BUILD_NUMBER':BUILD_NUMBER, # by increasing build number, it will show welcome screen.
    'LOG_LEVEL':logging.INFO,
    'LOG_PATH' : str(pathlib.Path(return_temp_path()).joinpath('log.log')),
    'EXE_PATH': str(pathlib.Path(application_path())),
    'SETTINGS_PATH' : str(pathlib.Path(application_path()).joinpath('settings.es')),
    'MAIN_EXPORT_PATH' : str(pathlib.Path(os.path.expanduser("~/Desktop/ACD_EXPORTS"))),
    'EXPORT_PATH' : str(pathlib.Path(os.path.expanduser("~/Desktop")).joinpath('ACD_EXPORTS').joinpath('ADOBE CONNECT')),
    'SHIFTIO_EXPORT_PATH' : str(pathlib.Path(os.path.expanduser("~/Desktop")).joinpath('ACD_EXPORTS').joinpath('Transfers')),
    'FTP_EXPORT_PATH' : str(pathlib.Path(os.path.expanduser("~/Desktop")).joinpath('ACD_EXPORTS').joinpath('FTP')),
    'TEMP_PATH' : return_temp_path(),
    'APPLICATION_KEY': 'vdhOVlS0ghzlRy75aQLK0paoRHmWUvfoQ-EhWWx6D_o=',
    'ACD_ENGINE_PATH': str(pathlib.Path(application_path()).joinpath('acd_engine.acde')),
    'ENGINE_COOKIE_PATH': str(pathlib.Path(application_path()).joinpath(f'{get_random_string(32)}.acdata')),
    'ENGINE_DUMP_PATH':  str(pathlib.Path(application_path()).joinpath('dumps')),
    'OUTPUT_BITRATE' : "90k",
    'OUTPUT_FORMAT': "mp4",
    'TOTAL_DOWNLOADED_COURSES':0,
    'TOTAL_FTP_DOWNLOAD':0,
    'TOTAL_SHIFTIO_TRANSFER':0,
    'SHIFTIO_FILE_TYPES':['jpg','png','jpeg','pdf','mp4','txt','docx','pptx','doc','ppt','mov','mp3','aac','mkv'],
    }

check_or_create_exports_folder()

def engine_cookie_path():
    load_settings()
    return SETTINGS['ENGINE_COOKIE_PATH']

def settings_file_exists():
    return pathlib.Path(application_path()).joinpath('settings.es').exists()

def save_settings():
    f = Fernet(SETTINGS['APPLICATION_KEY'].encode('utf-8'))
    encrypted_data = f.encrypt(json.dumps(SETTINGS).encode('utf-8'))
    with open(str(pathlib.Path(application_path()).joinpath('settings.es')), "wb") as file:
        file.write(encrypted_data)
    file.close()

def load_settings():
    f = Fernet(SETTINGS['APPLICATION_KEY'].encode('utf-8'))
    with open(str(pathlib.Path(application_path()).joinpath('settings.es')), "rb") as file:
        encrypted_data = file.read()
    file.close()
    data = json.loads(f.decrypt(encrypted_data))
    SETTINGS['BUILD_NUMBER'] = data['BUILD_NUMBER']
    SETTINGS['OUTPUT_BITRATE'] = data['OUTPUT_BITRATE']
    SETTINGS['OUTPUT_FORMAT'] = data['OUTPUT_FORMAT']
    SETTINGS['ENGINE_COOKIE_PATH'] = data['ENGINE_COOKIE_PATH']
    SETTINGS['TOTAL_DOWNLOADED_COURSES']=data['TOTAL_DOWNLOADED_COURSES']
    SETTINGS['TOTAL_FTP_DOWNLOAD']=data['TOTAL_FTP_DOWNLOAD']
    SETTINGS['TOTAL_SHIFTIO_TRANSFER']= data['TOTAL_SHIFTIO_TRANSFER']
    SETTINGS['SHIFTIO_FILE_TYPES']= data['SHIFTIO_FILE_TYPES']

def return_output_bitrate():
    try:
        load_settings()
    except:
        return "90k"
    else:
        return SETTINGS['OUTPUT_BITRATE']

def set_output_bitrate(bitrate):
    try:
        load_settings()
        SETTINGS['OUTPUT_BITRATE'] = bitrate
        save_settings()
    except:
        return False
    else:
        return True

def return_output_format():
    try:
        load_settings()
    except Exception as msg:
        return "mp4"
    else:
        return SETTINGS['OUTPUT_FORMAT']

def set_output_format(format):
    try:
        load_settings()
        SETTINGS['OUTPUT_FORMAT'] = format
        save_settings()
    except:
        return False
    else:
        return True

def return_shiftio_valid_types():
    try:
        load_settings()
    except:
        return ['jpg','png','jpeg','pdf','mp4','txt','docx','pptx','doc','ppt','mov','mp3','aac','mkv']
    else:
        return SETTINGS['SHIFTIO_FILE_TYPES']

def ret_buildnumber():
    try:
        load_settings()
    except:
        return 0
    else:
        return SETTINGS['BUILD_NUMBER']

def add_downloaded_courses(number):
    load_settings()
    if isinstance(number,int):
        SETTINGS['TOTAL_DOWNLOADED_COURSES'] += number
    save_settings()

def add_ftp_download(number):
    load_settings()
    if isinstance(number,int):
        SETTINGS['TOTAL_FTP_DOWNLOAD'] += number
    save_settings()

def add_shiftio_transfer(number):
    load_settings()
    if isinstance(number,int):
        SETTINGS['TOTAL_SHIFTIO_TRANSFER'] += number
    save_settings()

def change_shiftio_filetypes(to : list):
    load_settings()
    if isinstance(to,list):
        SETTINGS['SHIFTIO_FILE_TYPES'] = list
    save_settings()
