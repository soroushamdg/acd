"""
this file holds options and database vars
"""
import options_decoder
import os

options = {'selected_language':'en',
               'main_exe_path':'/'.join(os.path.realpath(__file__).split('\\')[:-2]),}
# selected languge
#driver_path
# main exe path
# ffmpeg_path
# db file
# driver path

def save_options():

    try:
        options_decoder.encrypt(options,'/'.join(os.path.realpath(__file__).split('\\')[:-2])+'/'+'settings.acds', 'vdhOVlS0ghzlRy75aQLK0paoRHmWUvfoQ-EhWWx6D_o=')
    except:
        return False
    else:
        return True

def load_options():
    global options
    try:
        file = open('/'.join(os.path.realpath(__file__).split('\\')[:-2])+r"/settings.acds",'r')
    except:
        assert save_options(),"can't save options files #25"
        return True
    else:
        options = options_decoder.decrypt('/'.join(os.path.realpath(__file__).split('\\')[:-2])+ r"/settings.acds",'vdhOVlS0ghzlRy75aQLK0paoRHmWUvfoQ-EhWWx6D_o=')
        return False

urls_db = {}

def load_database():
    global urls_db
    if 'db-path' in options:
        try:
            file = open(options['db-path'], 'r')
        except:
            return False
        else:
            urls_db = options_decoder.decrypt(
                options['db-path'],
                'vdhOVlS0ghzlRy75aQLK0paoRHmWUvfoQ-EhWWx6D_o=')
            return True
    try:
        file = open('/'.join(os.path.realpath(__file__).split('\\')[:-2])+'/'+'database.acddb','r')
    except:
        return False
    else:
        urls_db = options_decoder.decrypt('/'.join(os.path.realpath(__file__).split('\\')[:-2])+'/'+ 'database.acddb','vdhOVlS0ghzlRy75aQLK0paoRHmWUvfoQ-EhWWx6D_o=')
        return True
