import logging
import pathlib
import subprocess
import sys
from settings import SETTINGS
import clearbuffer

def engine_file_exists():
    if pathlib.Path(SETTINGS['ACD_ENGINE_PATH']).exists():
        return True
    else:
        return False
def check_current_engine():
    """
    Check if current engine works ok
    :return: bool
    """
    if not pathlib.Path(SETTINGS['ACD_ENGINE_PATH']).exists():
        return False
    try:
        from selenium.webdriver import Chrome
        from selenium.webdriver.chrome.options import Options
        opts = Options()
        opts.add_argument("--headless")
        opts.add_argument("--no-sandbox")
        ac_browser = Chrome(options=opts, executable_path=SETTINGS['ACD_ENGINE_PATH'])
        clearbuffer.clear_buffer()
        ac_browser.close()
        ac_browser.quit()
        del ac_browser
        del opts
    except:
        return False
    else:
        return True

def current_engine_version():
    """
    Return current engine version from settings file.
    :return: str
    """
    if not pathlib.Path(SETTINGS['ACD_ENGINE_PATH']).exists():
        return False
    try:
        from selenium.webdriver import Chrome
        from selenium.webdriver.chrome.options import Options
        opts = Options()
        opts.add_argument("--headless")
        opts.add_argument("--no-sandbox")
        ac_browser = Chrome(options=opts, executable_path=SETTINGS['ACD_ENGINE_PATH'])
        clearbuffer.clear_buffer()
        version = ac_browser.capabilities['chrome']['chromedriverVersion'].split(' ')[0]
        ac_browser.close()
        ac_browser.quit()
        del ac_browser
        del opts
    except Exception as msg:
        logging.debug(msg)
        logging.error('Error in checking current engine version')
        return False
    else:
        return version if version else False

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
    if version:
        return version

    # get version using chrome driver
    if not pathlib.Path(SETTINGS['ACD_ENGINE_PATH']).exists():
        return False
    try:
        from selenium.webdriver import Chrome
        from selenium.webdriver.chrome.options import Options
        opts = Options()
        opts.add_argument("--headless")
        opts.add_argument("--no-sandbox")
        ac_browser = Chrome(options=opts, executable_path=SETTINGS['ACD_ENGINE_PATH'])
        clearbuffer.clear_buffer()
        version = ac_browser.capabilities['browserVersion']
        ac_browser.close()
        ac_browser.quit()
        del ac_browser
        del opts
    except:
        return False
    else:
        return version if version else False

def needs_new_engine_download():
    """
    Check if needs to update, repair or install engine.
    :return: bool
    """
    if not engine_file_exists():
        return True
    syschrome = get_chrome_version()
    currentengine = current_engine_version()
    if syschrome and currentengine:
        if str(syschrome).split('.')[0] == str(currentengine).split('.')[0]:
            return False
        else:
            return True
    else:
        return True