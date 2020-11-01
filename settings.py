import logging
import os
import sys,pathlib
import json
from cryptography.fernet import Fernet
from exeinfo import BUILD_NUMBER
def application_path(DEBUG = True):
    config_name = 'myapp.cfg'

    # determine if application is a script file or frozen exe
    if getattr(sys, 'frozen', True):
        application_path = os.path.dirname(sys.executable)
    elif __file__:
        application_path = os.path.dirname(__file__)

    config_path = os.path.join(application_path, config_name)
    return str(pathlib.Path(config_path).parent) if not DEBUG else str(pathlib.Path(config_path).parent.parent.parent.joinpath('DEBUG'))

# Default settings dictionary
SETTINGS = {
    'BUILD_NUMBER':BUILD_NUMBER, # by increasing build number, it will show welcome screen.
    'LOG_LEVEL':logging.DEBUG,
    'LOG_PATH' : str(pathlib.Path(application_path()).joinpath('log.log')),
    'EXE_PATH': str(pathlib.Path(application_path())),
    'APPLICATION_KEY': 'vdhOVlS0ghzlRy75aQLK0paoRHmWUvfoQ-EhWWx6D_o=',
    'ACD_ENGINE_PATH': str(pathlib.Path(application_path()).joinpath('acd_engine.acde')),
    'TOTAL_DOWNLOADED_COURSES':0,
    'TOTAL_FTP_DOWNLOAD':0,
    'TOTAL_SHIFTIO_TRANSFER':0,
    'SHIFTIO_FILE_TYPES':['jpg','png','jpeg','pdf','mp4','txt','docx','pptx','doc','ppt'],
    }

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
    SETTINGS['TOTAL_DOWNLOADED_COURSES']=data['TOTAL_DOWNLOADED_COURSES']
    SETTINGS['TOTAL_FTP_DOWNLOAD']=data['TOTAL_FTP_DOWNLOAD']
    SETTINGS['TOTAL_SHIFTIO_TRANSFER']= data['TOTAL_SHIFTIO_TRANSFER']
    SETTINGS['SHIFTIO_FILE_TYPES']= data['SHIFTIO_FILE_TYPES']

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
