import logging
import pathlib
from urllib.parse import urljoin
import settings
import enum
import tldextract
import shutil

class acCourseStatus(enum.Enum):
    failure = -1
    fresh = 0
    ready = 1
    downloaded = 2
    parsedstreams = 3
    assets_downloaded = 40
    exported_media = 4
    assetsdl_mediaexport = 44
    mixed_converted_audio = 50
    converted_video = 5
    mixed_converted_audio_video = 55
    merged_audio_video = 6
    merge_video_audio_failure = -6
    finished = 7
    cleanedup = 8

def check_if_filename_exists(filename):
    return pathlib.Path(settings.SETTINGS['EXPORT_PATH']).joinpath(filename).exists()

def validate_input_url(loginurl,courseurl):
    return tldextract.extract(loginurl).domain == tldextract.extract(courseurl).domain and tldextract.extract(loginurl).suffix == tldextract.extract(courseurl).suffix

def return_domain(url):
    extract = tldextract.extract(url)
    return f"{extract.domain}.{extract.suffix}"

def extract_download_url_from_course_url(url,filename):
    return urljoin(url,f'output/{"".join(filename.split())}.cdata?download=zip')

class acCourse():
    def __init__(self,course_url,filename,merge_files=False,download_assets=False):
        self.status = 0
        self.course_url = course_url
        self.filename = ''.join(filename.split())
        self.merge_files = merge_files
        self.download_assets = download_assets
        self.media_streams_objects = []
        self.assets_streams_objects = []
        self.download_url = extract_download_url_from_course_url(course_url,filename)
        pathlib.Path(settings.SETTINGS['EXPORT_PATH']).joinpath(filename).mkdir(parents=True, exist_ok=True)
        self.export_folder = str(pathlib.Path(settings.SETTINGS['EXPORT_PATH']).joinpath(filename))
        self.status = 1

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

    def asset_download_url(self,asseturl):
        return urljoin(self.course_url,asseturl)

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
            if index and isinstance(index,int) and index>=0:
                if len(self.queue_list)-1 >= index:
                    if self.queue_list[index].filename == filename:
                        self.queue_list.remove(index)
                        return True
            for index,item in enumerate(self.queue_list):
                if item.filename == filename:
                    self.queue_list.remove(item)
                    return True
        except Exception as msg:
            logging.debug(msg)
            logging.error(f'Error in removing item ACCOURSE filename : {filename}')
            return False
        return False


    def return_queue_list_filenames(self,with_index=False):
        if with_index:
            return list(enumerate([item.filename for item in self.queue_list]))
        else:
            return self.queue_list

    def update_ac_course_object(self,acCourseObject : acCourse):
        for index, item in enumerate(self.queue_list):
            if acCourseObject == item:
                self.queue_list[index] = acCourseObject


    def cancel_and_remove_files(self):
        for course in self.queue_list:
            if course.status not in [acCourseStatus.finished, acCourseStatus.cleanedup]:
                try:
                    shutil.rmtree(pathlib.Path(settings.SETTINGS['EXPORT_PATH']).joinpath(course.filename))
                except:
                    pass

    def remove_failed_files(self):
        for course in self.queue_list:
            if course.status not in [acCourseStatus.finished, acCourseStatus.cleanedup]:
                try:
                    shutil.rmtree(pathlib.Path(settings.SETTINGS['EXPORT_PATH']).joinpath(course.filename))
                except Exception as msg:
                    logging.debug(msg)