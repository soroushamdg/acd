import logging
import os
import pathlib
import tempfile
from urllib.parse import urljoin
import itertools as IT
import settings
import enum
from ftplib import FTP
import shutil

class ftpCourseStatus(enum.Enum):
    failure = -1
    fresh = 0
    ready = 1
    downloading = 2
    downloaded = 3
    finished = 4

def uniquify(path, sep = ''):
    def name_sequence():
        count = IT.count()
        yield ''
        while True:
            yield '{s} - {n:d}'.format(s = sep, n = next(count))
    orig = tempfile._name_sequence
    with tempfile._once_lock:
        tempfile._name_sequence = name_sequence()
        path = os.path.normpath(path)
        dirname, basename = os.path.split(path)
        filename, ext = os.path.splitext(basename)
        fd, filename = tempfile.mkstemp(dir = dirname, prefix = filename, suffix = ext)
        tempfile._name_sequence = orig
    os.close(fd)
    return filename



def get_size_format(n, suffix="B"):
    # converts bytes to scaled format (e.g KB, MB, etc.)
    for unit in ["", "K", "M", "G", "T", "P"]:
        if n < 1024:
            return f"{n:.2f}{unit}{suffix}"
        n /= 1024

class ftpCourse():
    def __init__(self,filepath : str):
        self.status = ftpCourseStatus.fresh
        self.file_directory = filepath
        self.save_directory = uniquify(pathlib.Path(settings.SETTINGS['FTP_EXPORT_PATH']).joinpath(filepath.split('/')[-1]))
        self.filename = self.save_directory.split('/')[-1]
        self.filetype = self.filename.split('.')[-1]
        self.filesize = None
        self.status = ftpCourseStatus.ready

    def __eq__(self, other):
        return self.file_directory == other.file_directory

    def __hash__(self):
        return hash(('filedir', self.file_directory))


class ftpQueueManager():
    def __init__(self):
        self.queue_list = []
        self.ftpController = FTP()
        self.host = None
        self.username = None
        self.password = None
        self.previous_directory = None

    def set_ftp_host(self,host):
        self.host = host

    def login_into_host(self):
        if self.host:
            self.ftpController = FTP(self.host)
            try:
                resp = self.ftpController.login(user = self.username, passwd= self.password)
            except Exception as msg:
                logging.debug(msg)
                logging.error(f'ERROR IN LOGGING INTO FTP -> {self.host} -> {self.username}')
                return False
            else:
                if '230' in resp:
                    return True
                else:
                    return False

    def return_file_size(self,filepath):
        try:
            return get_size_format(self.ftpController.size(filepath))
        except:
            return None

    def return_current_directory(self):
        return self.ftpController.pwd()

    def goto_directory(self,dir_name):
        for _ in range(2):
            try:
                self.ftpController.cwd(dir_name)
            except Exception as msg:
                self.login_into_host()
                logging.debug(msg)
            else:
                return self.ftpController.pwd()
        return False

    def go_back_previous_directory(self):
        for _ in range(2):
            try:
                pwd = self.ftpController.pwd()
                if pwd != '/':
                    try:
                        if '/'.join(pwd.split('/')[:-1]):
                            assert self.goto_directory('/'.join(pwd.split('/')[:-1]))
                        else:
                            assert self.goto_directory('/')
                    except:
                        return False
                    else:
                        return self.ftpController.pwd()
                else:
                    return pwd
            except:
                self.login_into_host()
        return False

    def list_directory(self,include_filetypes=False):
        dir_list = []
        for item in self.ftpController.nlst():
            current = self.ftpController.pwd()
            try:
                self.ftpController.cwd(item)
            except:
                dir_list.append((item, 'FILE') if include_filetypes else (item))
            else:
                self.ftpController.cwd(current)
                dir_list.append((item, 'DIR') if include_filetypes else (item))
        return dir_list

    def add_to_queue(self,filepath):
        try:
            item = ftpCourse(filepath = filepath)
            item.filesize = self.ftpController.size(filepath)
        except Exception as msg:
            logging.debug(msg)
            logging.error('ERROR IN CREATING FTPCOURSE OBJECT')
            return False

        if item not in self.queue_list:
            self.queue_list.append(item)
            return True
        else:
            return 'DUPLICATE'

    def remove_from_queue(self,filepath,index=None):
        try:
            if index and isinstance(index,int) and index>=0:
                if len(self.queue_list)-1 >= index:
                    if self.queue_list[index].file_directory == filepath:
                        self.queue_list.remove(self.queue_list[index])
                        return True
            for index,item in enumerate(self.queue_list):
                if item.file_directory == filepath:
                    self.queue_list.remove(item)
                    return True
        except Exception as msg:
            logging.debug(msg)
            logging.error(f'Error in removing item FTPCOURSE filename : {filepath}')
            return False
        return False


    def return_queue_list_filepaths(self,with_index=False, with_filesize=True):
        if with_index:
            return list(enumerate([f"{item.file_directory} -> {get_size_format(item.filesize)}" for item in self.queue_list] if with_filesize else [f"{item.file_directory}" for item in self.queue_list]))
        else:
            return self.queue_list

    def update_ftp_course_object(self,ftpCourseObject : ftpCourse):
        for index, item in enumerate(self.queue_list):
            if ftpCourseObject == item:
                self.queue_list[index] = ftpCourseObject

    def cancel_and_remove_files(self):
        for course in self.queue_list:
            if course.status != ftpCourseStatus.finished:
                try:
                    shutil.rmtree(course.save_directory)
                except:
                    pass

    def remove_failed_files(self):
        for course in self.queue_list:
            if course.status not in [ftpCourseStatus.finished]:
                try:
                    shutil.rmtree(course.save_directory)
                except Exception as msg:
                    logging.debug(msg)