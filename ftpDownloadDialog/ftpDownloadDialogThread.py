import enum
import os
from time import sleep

from PyQt5 import QtCore
import ftplib
import settings,pathlib
from zipfile import ZipFile
import logging
from selenium.webdriver import Chrome
from mainThreads.ftpManager import ftpQueueManager, ftpCourse, ftpCourseStatus
import requests
from xmlparser import streamParser,assetsParser
import logging
from clearbuffer import clear_buffer
logging.basicConfig(filename=settings.SETTINGS['LOG_PATH'],filemode='a',level=settings.SETTINGS['LOG_LEVEL'],datefmt='%d-%b-%y %H:%M:%S',format="%(levelname)s -- %(asctime)s -- %(name)s -- %(message)s")

class downloadDialogStatus(enum.Enum):
    analyzing = 1
    downloading = 2
    cleanup = 3



def get_size_format(n, suffix="B"):
    # converts bytes to scaled format (e.g KB, MB, etc.)
    if n:
        for unit in ["", "K", "M", "G", "T", "P"]:
            if n < 1024:
                return f"{n:.2f} {unit}{suffix}"
            n /= 1024
    else:
        return "? B"

def byte_to_megabyte(n,withsuffix=False):
    return n / (1024*1024) if not withsuffix else f"{n / (1024*1024)} MB"

class ftpDownloadThread(QtCore.QThread):

    max_progress_bar_value = QtCore.pyqtSignal(int)
    update_progress_bar_value = QtCore.pyqtSignal(int)
    add_to_progressbar_current_value = QtCore.pyqtSignal(int)

    update_dialog_title = QtCore.pyqtSignal(int, downloadDialogStatus,str)
    raise_dialog = QtCore.pyqtSignal(str,str,str,bool)
    raise_errorflag = QtCore.pyqtSignal()


    def __init__(self,queuemanager : ftpQueueManager):
        QtCore.QThread.__init__(self)
        self.ftpQueueManager = queuemanager

    def __del__(self):
        self.wait()

    # PROGRESSBAR CONTROLLER
    def progressbar_reset(self):
        self.max_progress_bar_value.emit(1)
        self.update_progress_bar_value.emit(0)

    def progressbar_set_max(self,value):
        self.max_progress_bar_value.emit(int(value))

    def progressbar_set_value(self,value):
        self.update_progress_bar_value.emit(int(value))

    def progressbar_add_value(self,value):
        self.add_to_progressbar_current_value.emit(round(value))


    # DIALOG DIALOG TITLE
    def dialog_update_title(self,index, stage,filesize = ""):
        try:
            self.update_dialog_title.emit(index, stage, filesize)
        except Exception as msg:
            logging.debug(msg)

    # OPERATION FUNCTIONS
    def allowed_to_do(self, ftpcourse : ftpCourse):
        """
        This function will return True or False based on ftpcourse status,
        example, if status code is 2 (downloaded), it can do parse operation and not others.
        failure = -1
    fresh = 0
    ready = 1
    downloading = 2
    downloaded = 3
    finished = 4
        :return: returns functions that are allowed to run according to course status.
        """

        if ftpcourse.status == ftpCourseStatus.failure or ftpcourse.status == ftpCourseStatus.fresh:
            return []

        if ftpcourse.status == ftpCourseStatus.ready:
            return [self.course_get_filesize_and_set_progressbar_max, self.course_download_file, self.course_generate_write_handler]

        if ftpcourse.status == ftpCourseStatus.downloading:
            return [self.course_download_file]

        if ftpcourse.status == ftpCourseStatus.downloaded:
            return [self.course_check_downloaded_and_examined_filesize]

        if ftpcourse.status == ftpCourseStatus.finished:
            return []

    def ftp_controller_login(self):
        try:
            assert self.ftpQueueManager.login_into_host()
        except:
            return False
        else:
            return True

    def course_get_filesize_and_set_progressbar_max(self,course : ftpCourse):
        self.progressbar_reset()
        # Trying to get file size.
        for _ in range(2):
            try:
                assert self.ftpQueueManager.return_file_size(course.file_directory),f'ERROR IN GETTING FILE SIZE -> {course.file_directory}'
            except Exception as msg:
                logging.debug(msg)
                logging.error(f'ERROR IN GETTING FILE SIZE -> {course.file_directory}, TRYING AGAIN.')
                self.ftp_controller_login()
            else:
                self.progressbar_set_max(course.filesize if course.filesize else self.ftpQueueManager.return_file_size(course.file_directory))
                return True
        logging.error(f'ERROR IN GETTING FILE SIZE -> {course.file_directory}, SETTING AS FAILURE.')
        course.status = ftpCourseStatus.failure
        self.ftpQueueManager.update_ftp_course_object(course)
        return False

    def course_generate_write_handler(self,course : ftpCourse):
        try:
            self.download_destination_file = open(course.save_directory,'wb')
        except Exception as msg:
            logging.debug(msg)
            logging.error(f'ERROR IN CREATING FILE -> {course.save_directory}, SETTING AS FAILURE.')
            course.status = ftpCourseStatus.failure
            self.ftpQueueManager.update_ftp_course_object(course)
            return False

        def write_handler(data):
            self.download_destination_file.write(data)
            self.add_to_progressbar_current_value.emit(len(data))

        return write_handler

    def course_download_file(self,course : ftpCourse, write_handler):
        for _ in range(2):
            try:
                course.status = ftpCourseStatus.downloading
                self.ftpQueueManager.update_ftp_course_object(course)
                self.ftpQueueManager.ftpController.retrbinary('RETR ' + course.file_directory, write_handler)
            except Exception as msg:
                logging.debug(msg)
                logging.error(f'ERROR IN DOWNLOADING FILE -> {course.file_directory}, TRYING AGAIN.')
                self.ftp_controller_login()
                continue
            else:
                try:
                    if not self.download_destination_file.closed:
                        self.download_destination_file.close()
                except:
                    pass
                course.status = ftpCourseStatus.downloaded
                self.ftpQueueManager.update_ftp_course_object(course)
                return True

        try:
            if not self.download_destination_file.closed:
                self.download_destination_file.close()
        except:
            pass

        logging.error(f'ERROR IN DOWNLOADING FILE -> {course.file_directory}, SETTING AS FAILURE.')
        course.status = ftpCourseStatus.failure
        self.ftpQueueManager.update_ftp_course_object(course)
        return False

    def course_check_downloaded_and_examined_filesize(self,course : ftpCourse):
        try:
            if course.filesize == os.path.getsize(course.save_directory):
                return True
            else:
                logging.error(f'DOWNLOADED AND ORIGIN FILES SIZE OF FILE {course.file_directory} ARE NOT SAME!')
                return False
        except Exception as msg:
            logging.debug(msg)
            logging.error(f'ERROR IN EXAMINING DOWNLOADED FILE SIZE OF {course.file_directory}')



    def run(self):
        # RESET UI
        self.progressbar_reset()

        # START LOOPING EVERY QUEUE OBJECT
        for index, course in enumerate(self.ftpQueueManager.queue_list):
            # PREPARE
            self.dialog_update_title(index=index, stage=downloadDialogStatus.analyzing)
            sleep(1)
            if course.status == ftpCourseStatus.fresh or course.status == ftpCourseStatus.failure or course.status == ftpCourseStatus.finished :
                continue
            else:
                pass

            # GET FTP FILE SIZE
            if self.course_get_filesize_and_set_progressbar_max not in self.allowed_to_do(ftpcourse= course):
                continue
            else:
                try:
                    assert self.course_get_filesize_and_set_progressbar_max(course= course),'ERROR IN GETTING FTP FILE INFORMATION, CONTINUE TO NEXT QUEUE ITEM'
                except Exception as msg:
                    logging.error(msg)
                    continue

            # GENERATING FILE WRITE HANDLER
            if self.course_generate_write_handler not in self.allowed_to_do(ftpcourse= course):
                continue
            else:
                try:
                    write_handler = self.course_generate_write_handler(course= course)
                    if write_handler == False:
                        assert write_handler,'ERROR IN GENERATING FILE HANDLER, CONTINUE TO NEXT QUEUE ITEM'
                except Exception as msg:
                    logging.error(msg)
                    continue


            # CHECK IF FTP FILE IS NOT FAILURE
            if course.status == -1:
                logging.error('COURSE FLAGGED AS FAILURE, CONTINUE TO NEXT QUEUE ITEM')
                continue

            # START DOWNLOADING FILES
            if self.course_download_file not in self.allowed_to_do(ftpcourse=course):
                continue
            else:
                self.dialog_update_title(index=index, stage=downloadDialogStatus.downloading,filesize= get_size_format(course.filesize))

                try:
                    assert self.course_download_file(course=course,write_handler=write_handler), 'ERROR IN DOWNLOADING FTP FILE, CONTINUE TO NEXT QUEUE ITEM'
                except Exception as msg:
                    logging.error(msg)
                    continue

            # START CHECK DOWNLOADED FILES
            if self.course_check_downloaded_and_examined_filesize not in self.allowed_to_do(ftpcourse=course):
                pass
            else:
                self.dialog_update_title(index=index, stage=downloadDialogStatus.cleanup)

                try:
                    assert self.course_check_downloaded_and_examined_filesize(
                        course=course), 'ERROR IN EXAMINING DOWNLOADED FTP FILE, CONTINUE TO NEXT QUEUE ITEM'
                except Exception as msg:
                    logging.error(msg)
                    pass

            course.status = ftpCourseStatus.finished
            self.ftpQueueManager.update_ftp_course_object(course)


            logging.info(f'COURSE WITH DIRECTORY {course.file_directory} SAVED TO {course.save_directory} AND FINISHED PROCESSING.')

            continue









