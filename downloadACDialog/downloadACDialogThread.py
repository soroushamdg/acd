import os
import subprocess
from PyQt5 import QtCore
import requests,sys
from time import sleep
import settings,pathlib
from zipfile import ZipFile
import logging,threading

from selenium.webdriver import Chrome
from mainThreads.acManager import acQueueManager, acCourse


class downloadACThread(QtCore.QThread):
    add_to_progressbar_max_value = QtCore.pyqtSignal(int)
    add_to_progressbar_value = QtCore.pyqtSignal(int)
    reset_all_lcd_counters = QtCore.pyqtSignal()
    increase_downloaded_lcd_number = QtCore.pyqtSignal(int)
    increase_exctracted_lcd_number = QtCore.pyqtSignal(int)
    increase_downloaded_assets_lcd_number = QtCore.pyqtSignal(int)
    increase_converted_lcd_number = QtCore.pyqtSignal(int)
    raise_dialog = QtCore.pyqtSignal(str,str,str,bool)
    raise_errorflag = QtCore.pyqtSignal()

    def __init__(self,queuemanager : acQueueManager, acbrowser : Chrome):
        QtCore.QThread.__init__(self)

    def __del__(self):
        self.wait()

    # OPERATION FUNCTIONS
    def course_download_files(self,course : acCourse):
        pass

    def course_parse_stream_files(self,course : acCourse):
        pass

    def course_download_assets(self,course : acCourse):
        pass

    def course_extract_audio_video_files(self,course : acCourse):
        pass

    def course_concatenate_convert_audio(self,course : acCourse):
        pass

    def course_concatenate_convert_video(self,course : acCourse):
        pass

    def course_merge_video_audio(self,course : acCourse):
        pass


    def run(self):
        pass