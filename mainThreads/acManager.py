import logging
import pathlib
from urllib.parse import urljoin
import threading
import settings
import enum

class acCourseStatus(enum.Enum):
    fresh = 0
    ready = 1
    downloaded = 2
    assets_downloaded = 3
    media_converted = 4
    finished = 5


def extract_download_url_from_course_url(url,filename):
    return urljoin(url,f'/output/filename.zip?{"".join(filename.split())}.cdata')

class acCourse():
    def __init__(self,course_url,filename,merge_files=False,download_assets=False):
        self.status = acCourseStatus.fresh
        self.course_url = course_url
        self.filename = ''.join(filename.split())
        self.merge_files = merge_files
        self.download_assets = download_assets
        self.download_url = extract_download_url_from_course_url(course_url,course_url)
        pathlib.Path(settings.SETTINGS['EXPORT_PATH']).joinpath(filename).mkdir(parents=True, exist_ok=True)
        self.export_folder = str(pathlib.Path(settings.SETTINGS['EXPORT_PATH']).joinpath(filename))

        # create assets folder
        if download_assets:
            pathlib.Path(settings.SETTINGS['EXPORT_PATH']).joinpath(filename).joinpath('assets').mkdir(parents=True, exist_ok=True)

        self.status = acCourseStatus.ready

    def __eq__(self, other):
        return self.course_url == other.course_url \
               or self.filename == other.filename

    def __hash__(self):
        return hash(('filename', self.filename,
                     'course_url', self.course_url))

class acQueueManager():
    def __init__(self):
        self.queue_list = []

    def add_to_queue(self,course_url,filename,merge_files,download_assets):
        try:
            item = acCourse(course_url=course_url,
                        filename=filename,
                        merge_files=merge_files,
                        download_assets=download_assets)
        except Exception as msg:
            logging.debug(msg)
            logging.error('ERROR IN CREATING ACCOURSE OBJECT')
            return True

        if item not in self.queue_list:
            self.queue_list.append(item)
            return True
        else:
            return 'DUPLICATE'

    def remove_from_queue(self,filename,index=None):
        try:
            if index and isinstance(index,int):
                if len(self.queue_list)-1 >= index:
                    if self.queue_list[index].filename == filename:
                        self.queue_list.remove(index)
                        return True
            for index,item in enumerate(self.queue_list):
                if item.filename == filename:
                    self.queue_list.remove(index)
                    return True
        except Exception as msg:
            logging.debug(msg)
            logging.error(f'Error in removing item ACCOURSE filename : {filename}')
            return False
        return False


    def return_queue_list_filenames(self,with_index=False):
        if with_index:
            return list(enumerate(self.queue_list))
        else:
            return self.queue_list