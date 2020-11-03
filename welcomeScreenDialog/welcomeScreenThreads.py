import subprocess,os
import sys,pathlib
from time import sleep

from PyQt5 import QtCore
import settings

# CONFIGURE LOGGING
import logging


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
    return platform, architecture

#%%

def get_chrome_version():
    """
    :return: the version of chrome installed on client
    """
    platform, _ = get_platform_architecture()
    if platform == 'linux':
        with subprocess.Popen(['chromium-browser', '--version'], stdout=subprocess.PIPE) as proc:
            version = proc.stdout.read().decode('utf-8').replace('Chromium', '').strip()
            version = version.replace('Google Chrome', '').strip()
    elif platform == 'mac':
        process = subprocess.Popen(['/Applications/Google Chrome.app/Contents/MacOS/Google Chrome', '--version'], stdout=subprocess.PIPE)
        version = process.communicate()[0].decode('UTF-8').replace('Google Chrome', '').strip()
    elif platform == 'win':
        process = subprocess.Popen(
            ['reg', 'query', 'HKEY_CURRENT_USER\\Software\\Google\\Chrome\\BLBeacon', '/v', 'version'],
            stdout=subprocess.PIPE, stderr=subprocess.DEVNULL, stdin=subprocess.DEVNULL
        )
        version = process.communicate()[0].decode('UTF-8').strip().split()[-1]
    else:
        return
    return version

class configurationThread(QtCore.QThread):
    check_dependencies_status = QtCore.pyqtSignal(bool)
    setting_basic_config_status = QtCore.pyqtSignal(bool)
    raise_dialog = QtCore.pyqtSignal(str, str, str, bool)
    raise_errorflag = QtCore.pyqtSignal()

    def __init__(self):
        QtCore.QThread.__init__(self)

    def __del__(self):
        self.wait()

    def run(self):
        sleep(3)
        # STAGE 1-1 -> Writing file permission.
        try:
            with open(pathlib.Path(settings.application_path()).joinpath('test.txt'),'w') as f:
                f.write('123...123...')
        except Exception as msg:
            logging.debug(msg)
            logging.error('error IN WRITING TEST FILE.')
            self.raise_dialog.emit('Error', 'Error in writing files',
                                   'Please check file and directory permissions, or run as administrator.', True)
            return
        else:
            f.close()
            os.remove(pathlib.Path(settings.application_path()).joinpath('test.txt'))

        # STAGE 1-2 -> Check if system has chrome installed.
        try:
            version = get_chrome_version()
            assert all([version != None,version != 0,version]), 'Chrome version not proper.'
        except Exception as msg:
            logging.debug(msg)
            logging.error('Google Chrome not installed.')
            self.raise_dialog.emit('Error', 'Chrome is not installer or corrupted',
                                   'Please check Google Chrome installed on your computer, or if you don\'t have it, install from https://chrome.google.com', True)
            return
        else:
            pass

        self.check_dependencies_status.emit(True)
        sleep(3)

        # STAGE 2-1 -> CHECK SETTINGS FILE, SAVE NEW ONE, OR UPDATE OLD ONE
        try:
            if settings.settings_file_exists() :
                # update build number and resave settings file.
                from exeinfo import BUILD_NUMBER
                settings.load_settings()
                settings.SETTINGS['BUILD_NUMBER'] = BUILD_NUMBER
                settings.save_settings()
            else:
                settings.save_settings()
        except Exception as msg:
            logging.debug(msg)
            logging.error('Error in reading and parsing settings file, please delete settings.es if exists.')
            self.raise_dialog.emit('Error', 'Error in reading settings file.',
                                   'Error in reading and parsing settings file, please delete settings.es if exists.', True)
            return
        else:
            self.setting_basic_config_status.emit(True)


        sleep(3)
        return

