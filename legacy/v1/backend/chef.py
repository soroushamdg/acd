"""
Chef
This script will get downloaded file and extract it, then convert into mp4 files.
"""
from backend.options import ffmpeg_directory_bin,script_name,temp_path,remove_old_files_in_cache,mp4_export_path,make_folder_to_export_into
import subprocess
from zipfile import ZipFile
from pyLog.pylog import log
import xml.etree.ElementTree as ET
import datetime

def run_command_in_ffmeg(command):
    ffmpeg_dir = ffmpeg_directory_bin
    try:
        output = subprocess.call(str(ffmpeg_dir + command).split())
    except:
        log.log("error in running command.")
        return False
    else:
        log.log(script_name,'ffmpeg ran, output is not specified.')
        return True


def read_and_extract_zip(zipname,files_to_extract,not_include):
    files = {}
    try:
        with ZipFile(temp_path+zipname+'.cdata') as zip:
            for filename in zip.namelist():
                if any(search_name.lower() in filename.lower() for search_name in files_to_extract) and all(ext.lower() not in filename.lower() for ext in not_include):
                    files[filename] = zip.read(filename)
    except:
        log.log(script_name,'problem to read cached data.')
        return False

    return files


def export_time_and_flv_screen_shares_and_voips(files_dict):
    screen_shares = {}
    voips = {}
    for item in files_dict.items():
        if 'flv' in item[0].lower():
            if 'cameravoip' in item[0].lower():
                voips[item[0].split('.')[0]] = [item[1],'notime']
            elif 'screenshare' in item[0].lower():
                screen_shares[item[0]] = [item[1],'notime']
            else:
                continue
        else:
            continue

    #FINDING TIME
    # for item in files_dict.items():
    #     if 'xml' in item[0].lower() and any(voipname in item[0] for voipname in voips.keys()):
    #         with open(temp_path + 'tmpxml.data','w') as tempxml:
    #             tempxml.write(item[1].decode('ascii'))
    #         tree = ET.parse(temp_path+'tmpxml.data')
    #         try:
    #             date = tree.getroot()[5][1][5]
    #         except:
    #             log.log(script_name,"error in finding time.")
    #             continue
    #         else:
    #             voips[item[0].split('.')[0]].append(date.text if len(str(date.text).split()) == 5 else '')
    #         assert remove_old_files_in_cache('tmpxml'),"can not delete cache file."


    return (sorted(voips.items(), key=lambda item: item[1]),sorted(screen_shares.items(), key=lambda item: item[1]))


months = {'jan':1,
          'feb':2,
          'mar':3,
          'apr':4,
          'may':5,
          'jun':6,
          'jul':7,
          'aug':8,
          'sep':9,
          'oct':10,
          'nov':11,
          'dec':12}

def create_export_video_file(filename,extention):
    try:
        with open(mp4_export_path+filename+'.'+extention ,'wb') as file:
            log.log(script_name,"export video attempt to create")
    except:
        log.log(script_name,"could not create video file.")
        return False
    else:
        log.log(script_name, "export video file created!")
        file.close()
        return True


def save_video_into_temp_file(filename,data):
    try:
        with open(temp_path+filename+'.flv','wb') as temp_flv:
            temp_flv.write(data)
    except:
        log.log(script_name,"error in writing video cache")
    else:
        temp_flv.close()


def remove_video_from_temp_file(filename):
    assert remove_old_files_in_cache(filename),"error in removing video cache."

def merge_and_export_videos(files_tuple,export_path,exportname,time_diff,audio_is_sooner,has_audio,has_video):
    #save audio
    if has_audio:
        save_video_into_temp_file(files_tuple[0][0][0],files_tuple[0][0][1][1])
    if has_video:
        save_video_into_temp_file(files_tuple[1][0][0],files_tuple[1][0][1][1])

    assert run_command_in_ffmeg(f"ffmpeg -i {files_tuple[0][0][0]}.flv {'-itsoffset '+time_diff if not audio_is_sooner else ''} -i {files_tuple[1][0][0]}.flv {'-itsoffset '+time_diff if audio_is_sooner else ''} -c copy -c:a aac -map {'1:0' if audio_is_sooner else '0:1'} -shortest {export_path+exportname}.mov"),"error in running ffmpeg command."
    remove_video_from_temp_file(files_tuple[0][0][0])
    remove_video_from_temp_file(files_tuple[1][0][0])

    return True

def export_videos_sepratly(files_tuple,export_path,exportname):
    try:
        assert make_folder_to_export_into(exportname),"error in creating export folder"
    except:
        log.log(script_name,'error in creating export folder')

    log.log(script_name,'starting audio files')
    #export audios
    for index,file in enumerate(files_tuple[0]):
        log.log(script_name,f'started {index} audio')
        try:
            save_video_into_temp_file(file[0],file[1][0])
        except:
            log.log("error in saving to cache.")
        try:
            assert run_command_in_ffmeg(f"ffmpeg -i {temp_path}{file[0]}.flv -c copy -c:a aac -y {export_path}{exportname}/audio_{exportname}_{str(index)}.mp4"),"error in writing audio sepratly"
        except:
            log.log('error in running command')
        try:
            remove_video_from_temp_file(file[0])
        except:
            log.log('error in removing cached data')
    #export videos
    log.log(script_name,'starting video files')
    for index,file in enumerate(files_tuple[1]):
        log.log(script_name,f'started {index} video')
        try:
            save_video_into_temp_file(file[0], file[1][0])
        except:
            log.log("error in saving to cache.")
        try:
            assert run_command_in_ffmeg(
                f"ffmpeg -i {temp_path}{file[0]}.flv -c copy -c:a aac -y {export_path}{exportname}/video_{exportname}_{str(index)}.mov"), "error in writing video sepratly"
        except:
            log.log('error in running command')
        try:
            remove_video_from_temp_file(file[0])
        except:
            log.log('error in removing cached data')

    return True




def export_files_as_mov(files_tuple,export_path,course_name,merge = False):
    """
    if (merge and each video and audio 1 element) -> merge and export to mp4
    if not export each audio and video into seprate files
    :param files_tuple:
    :param export_path:
    :param merge:
    :return:
    """
    if merge and len(files_tuple[0]) < 2 and len(files_tuple[1]) < 2:
        has_audio = True if len(files_tuple[0]) != 0 else False
        has_video = True if len(files_tuple[1]) != 0 else False
        #check time diffs
        if has_audio and has_video:
            if files_tuple[0][0][1][1] != '' and files_tuple[1][0][1][1] != '':
                audio_started_sooner = False
                with (str(files_tuple[0][0][1]).split(),str(files_tuple[1][0][1]).split()) as times:
                    try:
                        time_diffs = datetime.datetime(times[0][0],months[times[0][1]],times[0][2],times[0][3].split(':')[0],times[0][3].split(':')[1],times[0][3].split(':')[2]) - datetime.datetime(times[1][0],months[times[1][1]],times[1][2],times[1][3].split(':')[0],times[1][3].split(':')[1],times[1][3].split(':')[2])
                    except:
                        log.log(script_name,"video started sooner")
                        time_diffs =  datetime.datetime(times[1][0],
                                                                                                      months[
                                                                                                          times[1][1]],
                                                                                                      times[1][2],
                                                                                                      times[1][3].split(
                                                                                                          ':')[0],
                                                                                                      times[1][3].split(
                                                                                                          ':')[1],
                                                                                                      times[1][3].split(
                                                                                                          ':')[2]) - datetime.datetime(times[0][0], months[times[0][1]], times[0][2],
                                                       times[0][3].split(':')[0], times[0][3].split(':')[1],
                                                       times[0][3].split(':')[2])
                        audio_started_sooner = True
                    finally:
                        assert merge_and_export_videos(files_tuple,export_path,course_name,time_diffs,audio_started_sooner,has_audio,has_video),"error in exporting merge."
                        return True
            else:
                assert export_videos_sepratly(files_tuple,export_path,course_name),"error in exporting sepratly #156"
                return True
        else:
            assert export_videos_sepratly(files_tuple, export_path, course_name), "error in exporting sepratly #158"
            return True
    else:
        try:
            assert export_videos_sepratly(files_tuple, export_path, course_name), "error in exporting sepratly #169"
        except:
            log.log(script_name,"error in wtf man!!! i'm exhausted, please work this time. 7_7")
        return True



# files = read_and_extract_zip('p11xf635hhb',['cameraVoip'],[])
# parsedfiles = export_time_and_flv_screen_shares_and_voips(files)
# export_files_as_mov(parsedfiles,mp4_export_path,'p11xf635hhb')

