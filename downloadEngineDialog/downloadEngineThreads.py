import os
import subprocess
from PyQt5 import QtCore
import requests,sys
from time import sleep
import settings,pathlib
from zipfile import ZipFile
import logging
import stat

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

def get_url(url,stream=False):
    session = requests.Session()
    return session.get(url,stream=stream)

class downloadEngineThread(QtCore.QThread):
    check_dependencies_status = QtCore.pyqtSignal(bool)
    download_engine_status = QtCore.pyqtSignal(bool)
    extract_install_status = QtCore.pyqtSignal(bool)
    update_progress_bar_value = QtCore.pyqtSignal(int)
    max_progress_bar_value = QtCore.pyqtSignal(int)
    raise_dialog = QtCore.pyqtSignal(str,str,str,bool)
    raise_errorflag = QtCore.pyqtSignal()

    def __init__(self):
        QtCore.QThread.__init__(self)

    def __del__(self):
        self.wait()

    def run(self):
        try:
            res = get_url(
                f'https://chromedriver.storage.googleapis.com/LATEST_RELEASE_{".".join(get_chrome_version().split(".")[:-1])}')
        except Exception as msg:
            logging.debug(msg)
            self.raise_dialog.emit('Error', 'Error in accessing server',
                                   'Please connect to VPN or a proxy and try again.', True)
            return
        if res.status_code != 200:
            self.raise_dialog.emit('Error', 'Error in accessing server',
                                   'Please connect to VPN or a proxy and try again.', True)
            return
        try:
            res = get_url(
            f'https://chromedriver.storage.googleapis.com/{str(res.content.decode("utf-8"))}/chromedriver_{"".join(get_platform_architecture())}.zip',
            stream=True)
        except Exception as msg:
            logging.debug(msg)
            self.raise_dialog.emit('Error', 'Error in accessing server',
                                   'Please connect to VPN or a proxy and try again.', True)
            return
        self.check_dependencies_status.emit(True)
        if res.status_code == 200:
            full_size = int(res.headers['Content-length'])
            self.max_progress_bar_value.emit((int(full_size/1024)+1)*1024)
            try:
                file = open(pathlib.Path(settings.SETTINGS['ACD_ENGINE_PATH']+'z'), 'wb')
            except Exception as msg:
                logging.debug(msg)
                self.raise_dialog.emit('Error', 'Error in creating new file',
                                       'Please check file permissions.', True)
                return
            downloaded = 0
            try:
                for chunk in res.iter_content(chunk_size=1024):
                    file.write(chunk)
                    downloaded += 1024
                    self.update_progress_bar_value.emit(downloaded)
            except Exception as msg:
                logging.debug(msg)
                self.raise_dialog.emit('Error', 'Error in downloading files',
                                       'Please check internet connection.', True)
                return
            else:
                self.download_engine_status.emit(True)
            file.close()
            sleep(2)
            # unzip data
            try:
                zip = ZipFile(pathlib.Path(settings.SETTINGS['ACD_ENGINE_PATH'] + 'z'), 'r')
                for zfile in zip.filelist:
                    if 'chromedriver' in zfile.filename:
                        file = open(pathlib.Path(settings.SETTINGS['ACD_ENGINE_PATH']), 'wb')
                        file.write(zip.read(zfile.filename))
                        file.close()
                        zip.close()
                        break
            except Exception as msg:
                logging.debug(msg)
                logging.error('Error in extracting and installing engine.')
                self.raise_dialog.emit('Error', 'Error in extracting and installing engine',
                                       'Please check internet connection and directory permissions and try again.', True)
                return
            else:
                os.remove(pathlib.Path(settings.SETTINGS['ACD_ENGINE_PATH'] + 'z'))

            # CHANGE FILE PERMISSIONS IF MAC OR LINUX
            try:
                if get_platform_architecture()[0] == 'mac' or 'linux':
                    import stat
                    st = os.stat(str(pathlib.Path(settings.SETTINGS['ACD_ENGINE_PATH'])))
                    os.chmod(str(pathlib.Path(settings.SETTINGS['ACD_ENGINE_PATH'])), st.st_mode | stat.S_IEXEC)
            except Exception as msg:
                logging.debug(msg)
                logging.error('Error in changing file permissions.')
                self.raise_dialog.emit('Error', 'Error in changing file permissions.',
                                       'Please set acd_engine.acde file permissions to EXECUTABLE and restart the program.', False)

            self.extract_install_status.emit(True)
            sleep(3)
            return
        else:
            self.raise_dialog.emit('Error', 'Error in accessing server',
                                   'Please connect to VPN or a proxy and try again.', True)
            return
