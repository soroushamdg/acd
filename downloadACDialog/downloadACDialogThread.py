import enum
import os
import subprocess
from PyQt5 import QtCore
import requests,sys
from time import sleep
from PIL import Image
from moviepy.audio.AudioClip import CompositeAudioClip
from moviepy.audio.io.AudioFileClip import AudioFileClip
from moviepy.video.VideoClip import ColorClip, ImageClip
from moviepy.video.compositing.concatenate import concatenate_videoclips
from moviepy.video.io.VideoFileClip import VideoFileClip
from pyffmpeg import FFmpeg

import settings,pathlib
from zipfile import ZipFile
import logging,threading
from selenium.webdriver import Chrome
from mainThreads.acManager import acQueueManager, acCourse, acCourseStatus
import pickle
import requests
from xmlparser import streamParser,assetsParser
import logging
from clearbuffer import clear_buffer
logging.basicConfig(filename=settings.SETTINGS['LOG_PATH']+'thread',filemode='a',level=logging.INFO,datefmt='%d-%b-%y %H:%M:%S',format="%(levelname)s -- %(asctime)s -- %(name)s -- %(message)s")

logger = 'bar'
verbose = True

class downloadDialogStatus(enum.Enum):
    analyzing = 1
    downloading = 2
    processing = 3
    dlassets_extracting = 4
    extracting = 5
    processing_media = 6
    merging = 7
    cleanup = 8

def milisec2sec(miliseconds):
    return (miliseconds/1000)

def get_size_format(n, suffix="B"):
    # converts bytes to scaled format (e.g KB, MB, etc.)
    for unit in ["", "K", "M", "G", "T", "P"]:
        if n < 1024:
            return f"{n:.2f} {unit}{suffix}"
        n /= 1024

def byte_to_megabyte(n,withsuffix=False):
    return n / (1024*1024) if not withsuffix else f"{n / (1024*1024)} MB"

class downloadACThread(QtCore.QThread):

    max_progress_bar_value = QtCore.pyqtSignal(int)
    update_progress_bar_value = QtCore.pyqtSignal(int)
    add_to_progressbar_current_value = QtCore.pyqtSignal(int)
    devide_progressbar_to  = QtCore.pyqtSignal(int)
    fill_progressbar_devide  = QtCore.pyqtSignal(int)
    reset_all_lcd_counters = QtCore.pyqtSignal()
    increase_downloaded_lcd_number = QtCore.pyqtSignal(int)
    increase_exctracted_lcd_number = QtCore.pyqtSignal(int)
    increase_downloaded_assets_lcd_number = QtCore.pyqtSignal(int)
    increase_converted_lcd_number = QtCore.pyqtSignal(int)
    update_dialog_title = QtCore.pyqtSignal(int, downloadDialogStatus)
    raise_dialog = QtCore.pyqtSignal(str,str,str,bool)
    raise_errorflag = QtCore.pyqtSignal()


    def __init__(self,queuemanager : acQueueManager, acbrowser : Chrome):
        QtCore.QThread.__init__(self)
        self.acQueueManager = queuemanager
        self.acBrowser = acbrowser

    def __del__(self):
        self.wait()

    def generate_blank_screen_image(self,width,height,output=None):
        background = Image.new(mode="RGB", size=(width,height), color=(0,0,0))
        info = Image.open(settings.src_path('novideo.jpg'))
        offset = int((width/2)-300), int((height/2)-300)
        background.paste(info, offset)
        background.save(output if output else settings.return_temp_path(filename=str(width)+str(height) + '.jpg'), format='JPEG', optimize=True, quality= 20 if width * height >= 422500 else 80)
        return output if output else settings.return_temp_path(filename=str(width)+str(height) + '.jpg')


    def create_blank_screen_video(self,duration, size, output=None):
        img = self.generate_blank_screen_image(size[0],size[1],output=output)
        clip = ImageClip(img).set_duration(duration)
        clip = concatenate_videoclips([clip],method="compose")
        clip.write_videofile(output if output else settings.return_temp_path(filename=str(duration) + f'.{settings.return_output_format()}'), fps=3 if size[0] * size[1] >= 422500 else 25, preset="ultrafast" ,verbose=verbose,
            logger=logger)
        clip.close()
        return output if output else settings.return_temp_path(filename=str(duration) + f'.{settings.return_output_format()}')

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

    def progressbar_devide_into(self,to):
        self.devide_progressbar_to.emit(to)

    def progressbar_fill_one_devide(self,to):
        self.fill_progressbar_devide.emit(to)


    # DIALOG DIALOG TITLE
    def dialog_update_title(self,index, stage):
        try:
            self.update_dialog_title.emit(index, stage)
        except Exception as msg:
            print(msg)

    # OPERATION FUNCTIONS
    def allowed_to_do(self,accourse : acCourse):
        """
        This function will return True or False based on accourse status,
        example, if status code is 2 (downloaded), it can do parse operation and not others.
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
        :return: returns functions that are allowed to run according to course status.
        """
        print(accourse.status)
        if accourse.status == acCourseStatus.failure or accourse.status == acCourseStatus.fresh:
            return []

        if accourse.status == acCourseStatus.ready:
            return [self.course_download_files]

        if accourse.status == acCourseStatus.downloaded:
            return [self.course_parse_stream_files]

        if accourse.status == acCourseStatus.parsedstreams:
            return [self.course_download_assets, self.course_extract_audio_video_files]

        if accourse.status == acCourseStatus.assets_downloaded:
            return [self.course_extract_audio_video_files]

        if accourse.status == acCourseStatus.exported_media:
            return [self.course_download_assets, self.course_concatenate_convert_audio, self.course_convert_video]

        if accourse.status == acCourseStatus.assetsdl_mediaexport:
            return [self.course_concatenate_convert_audio, self.course_convert_video]

        if accourse.status == acCourseStatus.mixed_converted_audio:
            return [self.course_convert_video, self.course_merge_video_audio, self.course_cleanup]

        if accourse.status == acCourseStatus.converted_video:
            return [self.course_concatenate_convert_audio, self.course_merge_video_audio, self.course_cleanup]

        if accourse.status == acCourseStatus.mixed_converted_audio_video:
            return [self.course_merge_video_audio]

        if accourse.status == acCourseStatus.merged_audio_video:
            return [self.course_cleanup]

        if accourse.status == acCourseStatus.merge_video_audio_failure:
            return [self.course_concatenate_convert_audio, self.course_convert_video, self.course_cleanup]

        if accourse.status == acCourseStatus.finished:
            return [self.course_cleanup]

        if accourse.status == acCourseStatus.cleanedup:
            return []

    def course_download_files(self,course : acCourse):
        self.progressbar_reset()
        self.acBrowser.get(course.course_url)
        clear_buffer()
        course_cookies = self.acBrowser.get_cookies()
        clear_buffer()
        ## preparing requests session
        session = requests.Session()
        try:
            for cookie in course_cookies:
                session.cookies.set(name=cookie["name"],
                          value=cookie["value"],
                          domain=cookie.get("domain"),
                          path=cookie.get("path"),
                          secure=cookie.get("secure"),
                          )
        except Exception as msg:
            logging.debug(msg)
            logging.error('Error happened in applying acCourse cookies into session.')
            print(msg)
        # SENDING GET REQUEST
        try:
            request = session.get(course.download_url,stream=True)
            assert request.status_code == 200, f'Request code = {request.status_code}'
        except Exception as msg:
            logging.debug(msg)
            logging.error(f'Error happened in requesting session, tagged as failure. -> {course.filename}')
            print(msg)
            course.status = acCourseStatus.failure
            self.acQueueManager.update_ac_course_object(course)
            return False
        # GETTING FULL SIZE OF FILE
        try:
            full_size = int(request.headers['Content-length'])
            self.progressbar_set_max(full_size)
        except Exception as msg:
            logging.debug(msg)
            logging.error(f'Error happened in getting request headers, tagged as failure. -> {course.filename}')
            print(msg)
            course.status = acCourseStatus.failure
            self.acQueueManager.update_ac_course_object(course)
            return False

        # START DOWNLOADING FILE
        try:
            f = open(str(pathlib.Path(course.export_folder).joinpath(f'{course.filename}.cdata')), "wb")
            dl_size = 0
            for chunk in request.iter_content(chunk_size=1048576):
                f.write(chunk)
                dl_size += 1048576 # 1 Mega-byte
                self.progressbar_set_value(dl_size)
                print(f'downloaded {get_size_format(dl_size)}/{get_size_format(full_size)}')
            sleep(1)
            f.close()
            assert os.path.getsize(str(pathlib.Path(course.export_folder).joinpath(f'{course.filename}.cdata'))) == full_size, 'File size not equal, corrupted download.'
        except Exception as msg:
            logging.debug(msg)
            logging.error(f'Error happened in getting request headers, tagged as failure. -> {course.filename}')
            print(msg)
            course.status = acCourseStatus.failure
            self.acQueueManager.update_ac_course_object(course)
            return False
        else:
            self.increase_downloaded_lcd_number.emit(1)
            course.status = acCourseStatus.downloaded
            self.acQueueManager.update_ac_course_object(course)
            return True

    def course_parse_stream_files(self,course : acCourse):
        self.progressbar_reset()
        self.progressbar_set_max(3)
        # OPEN DOWNLOADED FILE AS ZIP
        try:
            cdatazip = ZipFile(str(pathlib.Path(course.export_folder).joinpath(f'{course.filename}.cdata')), 'r')
            cdatazip.namelist()
        except Exception as msg:
            logging.debug(msg)
            logging.error(f'Error happened in opening cdata file, tagged as failure. -> {course.filename}')
            print(msg)
            try:
                cdatazip.close()
            except:
                pass
            course.status = acCourseStatus.failure
            self.acQueueManager.update_ac_course_object(course)
            return False
        self.progressbar_set_value(1)
        # READ INDEX BYTES DATA
        try:

            index = cdatazip.read('indexstream.xml')
            main = cdatazip.read('mainstream.xml')
        except Exception as msg:
            logging.debug(msg)
            logging.error(f'Error happened in reading cdata index files, tagged as failure. -> {course.filename}')
            print(msg)
            try:
                cdatazip.close()
            except:
                pass
            course.status = acCourseStatus.failure
            self.acQueueManager.update_ac_course_object(course)
            return False
        self.progressbar_set_value(2)
        # PARSING INDEX DATA
        try:
            course.media_streams_objects = streamParser.parseindexstream(bytesdata=index)
            if course.download_assets:
                course.assets_streams_objects = assetsParser.parsemainstream(bytesdata=main)
            else:
                course.assets_streams_objects = []
        except Exception as msg:
            try:
                cdatazip.close()
            except:
                pass

            logging.debug(msg)
            logging.error(f'Error happened in parsing cdata index files, tagged as failure. -> {course.filename}')
            print(msg)
            course.status = acCourseStatus.failure
            self.acQueueManager.update_ac_course_object(course)

            return False
        try:
            cdatazip.close()
        except:
            pass
        # UPDATING OBJECT STATUS
        course.status = acCourseStatus.parsedstreams
        self.acQueueManager.update_ac_course_object(course)

        self.progressbar_set_value(3)

        return True

    def course_download_assets(self,course : acCourse):
        self.progressbar_reset()
        if course.download_assets:
            if len(course.assets_streams_objects) > 0:
                for index, asset in enumerate(course.assets_streams_objects):
                    session = requests.Session()
                    # SENDING GET REQUEST
                    try:
                        course.assets_streams_objects[index].request_get = session.get(course.asset_download_url(asseturl=asset.directory), stream=True)
                    except Exception as msg:
                        logging.debug(msg)
                        logging.error(f'Error happened in requesting session for asset.> {asset.filename}')
                        del course.assets_streams_objects[index]
                        print(msg)
                        continue
                for index, asset in enumerate(course.assets_streams_objects):
                    # GETTING FULL SIZE OF FILE
                    try:
                        if asset.request_get:
                            full_size = int(asset.request_get.headers['Content-length'])
                            course.assets_streams_objects[index].filesize = full_size
                    except Exception as msg:
                        logging.debug(msg)
                        logging.error(
                            f'Error happened in requesting session for asset. -> {asset.filename}')
                        del course.assets_streams_objects[index]
                        print(msg)
                        continue

                self.progressbar_set_max(sum([byte_to_megabyte(item.filesize) for item in course.assets_streams_objects]))

                for index, asset in enumerate(course.assets_streams_objects):
                    try:
                        f = open(str(pathlib.Path(course.export_folder).joinpath('assets').joinpath(f'{asset.filename}')), "wb")
                        dl_size = 0
                        for chunk in asset.request_get.iter_content(chunk_size=1048576):
                            f.write(chunk)
                            dl_size += 1048576  # 1 Mega-byte
                            self.progressbar_add_value(byte_to_megabyte(1048576))
                            print(f'downloaded {get_size_format(dl_size)}/{get_size_format(full_size)}')
                        sleep(1)
                        f.close()
                        print(f.closed)
                        assert os.path.getsize(str(pathlib.Path(course.export_folder).joinpath('assets').joinpath(f'{asset.filename}'))) == full_size, 'asset file size not equal, corrupted download.'
                    except Exception as msg:
                        logging.debug(msg)
                        logging.error(
                            f'Error happened in downloading asset, tagged as failure. -> {asset.filename}')
                        print(msg)
                        continue
                    else:
                        self.increase_downloaded_assets_lcd_number.emit(1)
                        logging.info(f'Downloaded asset -> {asset.filename}')
                        continue
                if course.status != acCourseStatus.exported_media:
                    course.status = acCourseStatus.assets_downloaded
                else:
                    course.status = acCourseStatus.assetsdl_mediaexport
                self.acQueueManager.update_ac_course_object(course)
                return True

    def course_extract_audio_video_files(self,course : acCourse):
        sleep(3)
        total = len(course.media_streams_objects['audio'])+len(course.media_streams_objects['video'])
        self.progressbar_devide_into(total)

        # OPEN DOWNLOADED FILE AS ZIP
        try:
            cdatazip = ZipFile(str(pathlib.Path(course.export_folder).joinpath(f'{course.filename}.cdata')), 'r')
            cdatazip.namelist()
        except Exception as msg:
            logging.debug(msg)
            logging.error(f'Error happened in opening cdata file, tagged as failure. -> {course.filename}')
            print(msg)
            try:
                cdatazip.close()
            except:
                pass
            course.status = acCourseStatus.failure
            self.acQueueManager.update_ac_course_object(course)
            return False

        # READ AND EXTRACT FILES TO EXTRACT FROM INDEX
        try:
            for audio in course.media_streams_objects['audio']:
                data = cdatazip.read(audio.filename)
                with open(str(pathlib.Path(course.export_folder).joinpath(f'{audio.new_filename}.flv')), "wb") as file:
                    file.write(data)
                file.close()
                self.progressbar_fill_one_devide(total)
                self.increase_exctracted_lcd_number.emit(1)
            for video in course.media_streams_objects['video']:
                data = cdatazip.read(video.filename)
                with open(str(pathlib.Path(course.export_folder).joinpath(f'{video.new_filename}.flv')), "wb") as file:
                    file.write(data)
                file.close()
                self.progressbar_fill_one_devide(total)
                self.increase_exctracted_lcd_number.emit(1)
        except Exception as msg:
            logging.debug(msg)
            logging.error(f'Error in extracting course files, tagged as failure. -> {course.filename}')
            print(msg)
            try:
                cdatazip.close()
            except:
                pass
            course.status = acCourseStatus.failure
            self.acQueueManager.update_ac_course_object(course)
            return False
        else:
            if course.status != acCourseStatus.assets_downloaded:
                course.status = acCourseStatus.exported_media
            else:
                course.status = acCourseStatus.assetsdl_mediaexport

            try:
                cdatazip.close()
            except:
                pass

            self.acQueueManager.update_ac_course_object(course)
            return True

    def course_concatenate_convert_audio(self,course : acCourse, exportasvideo=False):
        # READ FILES FROM INDEX + CREATING AUDIO OBJECT
        try:
            audios = []
            for audio in course.media_streams_objects['audio']:
                audios.append(AudioFileClip(str(pathlib.Path(course.export_folder).joinpath(f'{audio.new_filename}.flv'))).set_start(
                    tuple([milisec2sec(audio.delay)])))
                self.progressbar_add_value(1)
        except Exception as msg:
            logging.debug(msg)
            logging.error(f'Error in creating audio object course files, tagged as failure. -> {course.filename}')
            print(msg)
            course.status = acCourseStatus.failure
            self.acQueueManager.update_ac_course_object(course)
            return False
        else:
            if not audios:
                return True

        # CREATING COMPOSITE OBJECT
        try:
            mixed = CompositeAudioClip(audios)
            mixed.fps = audios[0].fps
        except Exception as msg:
            logging.debug(msg)
            logging.error(f'Error in creating composite audio object course files, tagged as failure. -> {course.filename}')
            print(msg)
            course.status = acCourseStatus.failure
            self.acQueueManager.update_ac_course_object(course)
            return False

        if not exportasvideo:
            # WRITING NEW AUDIO
            try:
                mixed.write_audiofile(
                    str(pathlib.Path(course.export_folder).joinpath(f'audio_{course.filename}.mp3')),
                    verbose=verbose, logger=logger)
                mixed.close()
            except Exception as msg:
                try:
                    mixed.close()
                except:
                    pass
                logging.debug(msg)
                logging.error(f'Error in creating composite audio object course files, tagged as failure. -> {course.filename}')
                print(msg)
                course.status = acCourseStatus.failure
                self.acQueueManager.update_ac_course_object(course)
                return False
            else:
                self.progressbar_add_value(1)
                if course.status == acCourseStatus.converted_video:
                    course.status = acCourseStatus.mixed_converted_audio_video
                else:
                    course.status = acCourseStatus.mixed_converted_audio
                self.increase_converted_lcd_number.emit(1)
                self.acQueueManager.update_ac_course_object(course)
                return True
        else:
            # GENERATE IMAGE
            try:
                img = self.generate_blank_screen_image(650, 650)
            except Exception as msg:
                logging.debug(msg)
                logging.error(
                    f'Error in generating image, tagged as failure. -> {course.filename}')
                print(msg)
                course.status = acCourseStatus.failure
                self.acQueueManager.update_ac_course_object(course)
                return False

            # MERGE AUDIO + IMAGE
            try:
                clip = ImageClip(img).set_duration(mixed.duration)
                clip = clip.set_audio(mixed)
                clip.write_videofile(
                    str(pathlib.Path(course.export_folder).joinpath(f'{course.filename}.{settings.return_output_format()}')),
                    fps=10, verbose=verbose,
            logger=logger)
                clip.close()
            except Exception as msg:
                try:
                    clip.close()
                except:
                    pass
                logging.debug(msg)
                logging.error(
                    f'Error in generating output video-audio files, tagged as failure. -> {course.filename}')
                print(msg)
                course.status = acCourseStatus.failure
                self.acQueueManager.update_ac_course_object(course)
                return False
            else:
                self.progressbar_add_value(1)
                self.increase_converted_lcd_number.emit(1)
                course.status = acCourseStatus.merged_audio_video
                self.acQueueManager.update_ac_course_object(course)
                return True

    def course_convert_video(self,course : acCourse):
        """
        Just convert video files to mp4.
        :param course:
        :return:
        """
        if course.media_streams_objects['video']:
            # RUN FFMPEG COMMAND TO MERGE AUDIO + VIDEO
            try:
                for video in course.media_streams_objects['video']:
                    try:
                        ff = FFmpeg(course.export_folder)
                        ff.overwrite = True
                        ff.loglevel = ff.loglevels[0] # quiet log level
                        output = ff.convert(video.filename,video.new_filename+f'.{settings.return_output_format()}')
                    except:
                        continue
                    else:
                        self.progressbar_add_value(1)
                        self.increase_converted_lcd_number.emit(1)
            except Exception as msg:
                logging.debug(msg)
                logging.error(
                    f'Error in converting object course files, tagged as failure. -> {course.filename}')
                print(msg)
                course.status = acCourseStatus.failure
                self.acQueueManager.update_ac_course_object(course)
                return False
            else:
                logging.debug(output)
                logging.info(output)
                course.status = acCourseStatus.converted_video
                self.acQueueManager.update_ac_course_object(course)
                return True

    def course_merge_video_audio(self,course : acCourse):
        """
        Concat videos and mix with merged audio.
        :param course:
        :return:
        """
        self.progressbar_reset()
        if course.media_streams_objects['video']:
            self.progressbar_set_max(len(course.media_streams_objects['video'])+10)
            # READ FILES FROM INDEX + CREATING VIDEO OBJECT
            try:
                videos = []
                for vid in course.media_streams_objects['video']:
                    try:
                        video = VideoFileClip(str(pathlib.Path(course.export_folder).joinpath(f'{vid.new_filename}.flv')))
                    except Exception as msg:
                        print(msg)
                        continue
                    else:
                        videos.append(video.set_start(tuple([milisec2sec(vid.delay)])))
                    finally:
                        self.progressbar_add_value(1)
            except Exception as msg:
                logging.debug(msg)
                logging.error(f'Error in creating video object course files, tagged as failure. -> {course.filename}')
                print(msg)
                course.status = acCourseStatus.failure
                self.acQueueManager.update_ac_course_object(course)
                return False

            # ADD BLANK SCREENS
            try:
                for index, item in enumerate(videos):
                    if index == 0:
                        if item.start != 0:
                            blank_screen = VideoFileClip(
                                self.create_blank_screen_video(duration = item.start, size=(item.w, item.h)))
                            videos.insert(0, blank_screen)
                            continue
                    else:
                        if item.start - videos[index - 1].start - videos[index - 1].duration > 0:
                            blank_screen = VideoFileClip(self.create_blank_screen_video(
                                duration=item.start - (videos[index - 1].start + videos[index - 1].duration),size=(item.w,item.h)))
                            videos.insert(index, blank_screen)
            except Exception as msg:
                logging.debug(msg)
                logging.error(f'Error in creating video object course files, tagged as failure. -> {course.filename}')
                print(msg)
                course.status = acCourseStatus.failure
                self.acQueueManager.update_ac_course_object(course)
                return False


            # CHECK IF AUDIO EXISTS
            try:
                assert pathlib.Path(course.export_folder).joinpath(f'audio_{course.filename}.mp3').exists(),'Mixed audio object does not exist.'
            except Exception as msg:
                if course.media_streams_objects['audio']:
                    logging.debug(msg)
                    logging.error(
                        f'Error in finding mixed audio object course files, tagged as failure. -> {course.filename}')
                    print(msg)
                    course.status = acCourseStatus.failure
                    self.acQueueManager.update_ac_course_object(course)
                    return False
                else:
                    audio_command = False
            else:
                audio_command = True

            # RUN FFMPEG COMMAND TO MERGE AUDIO + VIDEO
            try:
                ff = FFmpeg()
                ff.overwrite = True
                ff.loglevel = ff.loglevels[0] # quiet log level
                args = (f"-i {pathlib.Path(course.export_folder).joinpath(f'audio_{course.filename}.mp3')}", # AUDIO INPUT
                        " ".join([f"-i {video.filename}" for video in videos]), # VIDEOS INPUT
                        "-filter_complex",
                        f'"{" ".join([f"[{index + 1 if audio_command else index}:v]fps=25[v{index + 1 if audio_command else index}];" if item.fps != 25 else "" for index, item in enumerate(videos)]).lstrip()}',
                        f'{" ".join([f"[v{index + 1 if audio_command else index}]" if item.fps != 25 else f"[{index + 1 if audio_command else index}:v]" for index, item in enumerate(videos)]).rstrip()} concat=n={len(videos)}:v=1{":a=0" if audio_command else ""} [outv]"',
                        "-map [outv]",
                        f"-map 0:a:0" if audio_command else "",
                        # '-c:v libx264 -c:a aac',
                        f'-b:v {settings.return_output_bitrate()} -threads 3 -preset ultrafast',
                        # "-movflags +faststart",
                        '-stats',
                        str(pathlib.Path(course.export_folder).joinpath(f'{course.filename}.{settings.return_output_format()}')))
                output = ff.options(" ".join(args))
            except Exception as msg:
                logging.debug(msg)
                logging.error(
                    f'Error in creating merging video with audio object course files, tagged as failure. -> {course.filename}')
                print(msg)
                course.status = acCourseStatus.failure
                self.acQueueManager.update_ac_course_object(course)
                return False
            else:
                logging.debug(output)
                logging.info(output)
                self.progressbar_add_value(1)
                self.increase_converted_lcd_number.emit(1)
                course.status = acCourseStatus.merged_audio_video
                self.acQueueManager.update_ac_course_object(course)
                return True
        else:
            self.progressbar_set_max(2)
            # CHECK IF AUDIO EXISTS
            try:
                assert pathlib.Path(course.export_folder).joinpath(
                    f'audio_{course.filename}.mp3').exists(), 'Mixed audio object does not exist.'
            except Exception as msg:
                logging.debug(msg)
                logging.error(
                    f'Error in finding mixed audio object course files, tagged as failure. -> {course.filename}')
                print(msg)
                course.status = acCourseStatus.failure
                self.acQueueManager.update_ac_course_object(course)
                return False
            self.progressbar_add_value(1)
            # GENERATE IMAGE
            try:
                img = self.generate_blank_screen_image(650,650)
            except Exception as msg:
                logging.debug(msg)
                logging.error(
                    f'Error in generating image, tagged as failure. -> {course.filename}')
                print(msg)
                course.status = acCourseStatus.failure
                self.acQueueManager.update_ac_course_object(course)
                return False

            # MERGE AUDIO + IMAGE
            try:
                audio = AudioFileClip(pathlib.Path(course.export_folder).joinpath(
                    f'audio_{course.filename}.mp3'))
                clip = ImageClip(img).set_duration(audio.duration)
                clip = clip.set_audio(audio)
                clip.write_videofile(
                    str(pathlib.Path(course.export_folder).joinpath(f'{course.filename}.{settings.return_output_format()}')),
                    fps=10, verbose=verbose,
            logger=logger)
                clip.close()
            except Exception as msg:
                try:
                    clip.close()
                except:
                    pass
                logging.debug(msg)
                logging.error(
                    f'Error in generating output video-audio files, tagged as failure. -> {course.filename}')
                print(msg)
                course.status = acCourseStatus.failure
                self.acQueueManager.update_ac_course_object(course)
                return False
            else:
                course.status = acCourseStatus.merged_audio_video
                self.acQueueManager.update_ac_course_object(course)
                self.progressbar_add_value(1)
                self.increase_converted_lcd_number.emit(1)
                return True

    def course_cleanup(self,course : acCourse):
        self.progressbar_set_max(1+len(os.listdir(course.export_folder)))
        for file in os.listdir(settings.return_temp_path()):
            try:
                os.remove(settings.return_temp_path(filename=file))
            except:
                continue
        self.progressbar_add_value(1)
        for file in os.listdir(course.export_folder):
            try:
                if file.split('.')[-1] == 'flv':
                    os.remove(pathlib.Path(course.export_folder).joinpath(file))
            except:
                continue
            finally:
                self.progressbar_add_value(1)
        course.status = acCourseStatus.cleanedup
        self.acQueueManager.update_ac_course_object(course)
        return True

    def run(self):
        # RESET UI
        self.reset_all_lcd_counters.emit()
        self.progressbar_reset()

        # START LOOPING EVERY QUEUE OBJECT
        for index, course in enumerate(self.acQueueManager.queue_list):
            # PREPARE
            self.dialog_update_title(index=index, stage=downloadDialogStatus.analyzing)
            sleep(3)
            if course.status == 0 or course.status == -1 :
                continue
            else:
                pass

            # DOWNLOAD MEETING FILES
            if self.course_download_files not in self.allowed_to_do(accourse= course):
                continue
            else:
                try:
                    self.dialog_update_title(index= index, stage=downloadDialogStatus.downloading)
                    assert self.course_download_files(course= course),'ERROR IN DOWNLOADING COURSE, CONTINUE TO NEXT QUEUE ITEM'
                except Exception as msg:
                    logging.error(msg)
                    continue

            # PARSE STREAM FILES
            if self.course_parse_stream_files not in self.allowed_to_do(accourse= course):
                continue
            else:
                try:
                    self.dialog_update_title(index= index, stage=downloadDialogStatus.processing)
                    assert self.course_parse_stream_files(course= course),'ERROR IN PARSING COURSE FILES, CONTINUE TO NEXT QUEUE ITEM'
                except Exception as msg:
                    logging.error(msg)
                    continue

            # DEFINE THREADING OBJECT FOR 1. EXTRACTING FILES, 2. DOWNLOADING ASSETS.
            threads = []

            # DOWNLOADING ASSETS THREAD
            if self.course_download_assets in self.allowed_to_do(accourse=course) and course.download_assets:
                threads.append(
                    threading.Thread(target=self.course_download_assets, args=(course,))
                )

            # EXTRACTING THREAD
            if self.course_extract_audio_video_files in self.allowed_to_do(accourse= course) and course.download_assets:
                threads.append(
                    threading.Thread(target = self.course_extract_audio_video_files,args = (course,))
                )
            else:
                course.status = acCourseStatus.failure
                continue

            if len(threads) == 2:
                self.dialog_update_title(index=index, stage=downloadDialogStatus.dlassets_extracting)
            else:
                self.dialog_update_title(index=index, stage=downloadDialogStatus.extracting)

            for job in threads:
                job.start()

            # WAIT FOR THREADS TO FINISH
            for job in threads:
                job.join()

            threads.clear()

            # CHECK IF COURSE OBJECT IS NOT FAILURE
            if course.status == -1:
                logging.error('COURSE FLAGGED AS FAILURE, CONTINUE TO NEXT QUEUE ITEM')
                continue

            # DEFINE THREADING OBJECT FOR 1. CONCAT + CONVERT AUDIOS, 2. CONVERT VIDEOS.
            threads = []
            # CONCAT + CONVERT AUDIOS THREAD
            if self.course_concatenate_convert_audio in self.allowed_to_do(
                    accourse=course):
                if not course.media_streams_objects['video']: # IF JUST HAS AUDIO
                    threads.append(
                        threading.Thread(target=self.course_concatenate_convert_audio, args=(course,True,))
                    )
                else: # ELSE HAS VIDEO TOO.
                    threads.append(
                        threading.Thread(target=self.course_concatenate_convert_audio, args=(course,))
                    )

            # CONVERT VIDEOS THREAD
            if self.course_convert_video in self.allowed_to_do(accourse=course) and not course.merge_files:
                threads.append(
                    threading.Thread(target=self.course_convert_video, args=(course,))
                )
            self.progressbar_reset()
            if len(threads) == 2:
                self.progressbar_set_max(
                    len(course.media_streams_objects['audio']) + 1 + len(course.media_streams_objects['video'])
                )
            else:
                self.progressbar_set_max(
                    len(course.media_streams_objects['audio']) + 1 # +1 is for command and others for reading and parsing.
                )

            self.dialog_update_title(index=index, stage=downloadDialogStatus.processing_media)

            for job in threads:
                job.start()

            # WAIT FOR THREADS TO FINISH
            for job in threads:
                job.join()

            # CHECK IF COURSE OBJECT IS NOT FAILURE
            if course.status == -1:
                logging.error('COURSE FLAGGED AS FAILURE, CONTINUE TO NEXT QUEUE ITEM')
                continue

            # MERGE FILES
            if self.course_merge_video_audio not in self.allowed_to_do(accourse=course):
                pass
            else:
                if course.media_streams_objects['video'] and course.merge_files:
                    try:
                        self.dialog_update_title(index=index, stage=downloadDialogStatus.merging)
                        assert self.course_merge_video_audio(
                            course=course), 'ERROR IN MERGING COURSE FILES, TRYING TO JUST CONVERT FILES.'
                    except Exception as msg:
                        logging.error(msg)
                        self.course_convert_video(course= course)
                        # CHECK IF COURSE OBJECT IS NOT FAILURE
                        if course.status == -1:
                            logging.error('ERROR IN CONVERTING FILES AFTER TRYING TO MERGE COURSE FILES, CONTINUE TO NEXT QUEUE ITEM')
                            continue

            course.status = acCourseStatus.finished
            self.acQueueManager.update_ac_course_object(course)

            # CLEAN UP FILES
            if self.course_cleanup not in self.allowed_to_do(accourse=course):
                continue
            else:
                try:
                    self.dialog_update_title(index= index, stage=downloadDialogStatus.cleanup)
                    assert self.course_cleanup(
                        course=course), 'ERROR IN CLEANING UP COURSE, CONTINUE TO NEXT QUEUE ITEM'
                except Exception as msg:
                    logging.error(msg)
                    continue
                else:
                    logging.info(f'COURSE WITH FILENAME {course.filename} FINISHED PROCESSING.')









