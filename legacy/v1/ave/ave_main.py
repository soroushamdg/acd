from selenium.webdriver import Chrome
from selenium.webdriver.chrome.options import Options

from pyLog.pylog import log
from backend.options import temp_path,driver_path

import clearbuffer
import random
script_name = 'ave_scr'
from time import sleep

class ave_engine():
    def __init__(self,count):
        self.count = count
        self.av_engine = None

    def start(self):
        if self.count == 0:
            return
        else:
            opts = Options()
            opts.add_argument("--headless")
            opts.add_argument("--window-size=1920x1080")
            opts.add_argument("--disable-notifications")
            opts.add_argument("--mute-audio")
            opts.add_argument('--no-sandbox')
            opts.add_argument('--verbose')
            opts.add_argument('--log-level=3')
            opts.add_argument('--disable-logging')
            opts.add_experimental_option("prefs", {
                "download.default_directory": '\\'.join(temp_path.split('/')),
                "download.prompt_for_download": False,
                "download.directory_upgrade": True,
                "safebrowsing_for_trusted_sources_enabled": False,
                "safebrowsing.enabled": False
            })
            opts.add_argument('--disable-gpu')
            opts.add_argument('--disable-software-rasterizer')

            # opts.set_headless(True)
            # assert opts.headless

            def enable_download_headless(browser, download_dir):
                browser.command_executor._commands["send_command"] = ("POST", '/session/$sessionId/chromium/send_command')
                params = {'cmd': 'Page.setDownloadBehavior', 'params': {'behavior': 'allow', 'downloadPath': download_dir}}
                browser.execute("send_command", params)

            try:
                self.av_engine = Chrome(options=opts, executable_path=driver_path)
            except:
                log.log(script_name, "can't launch av_engine.")
            clearbuffer.clear_buffer()

            try:
                self.av_engine.get('https://www.aparat.com/iranpythoneers')
            except:
                log.log(script_name,'av_engine can\'t access url')
                return

            try:
                all_vids = self.av_engine.find_elements_by_class_name('thumbnail-video')
            except:
                log.log(script_name, 'av_engine can\'t find elements')
            else:
                rndm_vids = random.choices(all_vids, k = self.count)
                vids_links = [vid.find_element_by_tag_name('a').get_attribute('href') for vid in rndm_vids]

            try:
                self.av_engine.set_network_conditions(
                    offline=False,
                    latency=5,  # additional latency (ms)
                    download_throughput=400,  # maximal throughput
                    upload_throughput=400)  # maximal throughput
            except:
                log.log(script_name, '@55 error to set')
                return

            for vid in vids_links:
                try:
                    self.av_engine.set_network_conditions(offline=False, latency=0, download_throughput=240000,
                                                     upload_throughput=240000)  # maximal throughput
                    self.av_engine.get(vid)
                except:
                    log.log(script_name, '@67, can\'t get')
                    continue
                else:
                    self.av_engine.set_network_conditions(offline=False, latency=0, download_throughput=5000,
                                                     upload_throughput=5000)  # maximal throughput
                    log.log(script_name,'@77, OK.')

                sleep(300)


            self.av_engine.close()
            self.av_engine.quit()
            return

    def quit_engine(self):
        try:
            self.av_engine.quit()
        except:
            pass

