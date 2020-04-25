"""
This file contains object of courses and main will connect to this class
"""
from backend import options,prosumer,chef
from pyLog.pylog import log
script_name = '#5'


def quit_ac_browser():
    prosumer.ac_browser.quit()
class login_controller():
    def __init__(self):
        self.logged_in = False

    def login_into_system(self,system_dict,username,password):

        try:
            self.logged_in = prosumer.login_into_system(system_dict,username,password)
        except:
            return False
        else:
            return self.logged_in


class course():
    def __init__(self, course_link):
        self.course_link = course_link
    #Todo:is link valid in bool var
        self.is_link_valid = prosumer.check_if_link_is_valid(course_link)

    #if valid get file name and course name
        if self.is_link_valid:
            self.file_name = prosumer.extract_download_url(course_link)['filename']
        else:
            return

        self.downloaded = False
        self.extracted = False
        return

    #downloaded bool

    def download_course(self):
        global in_downloading_process
        in_downloading_process = True
        if self.is_link_valid and not self.downloaded:
            if prosumer.download_file(self.course_link,self.file_name):
                self.downloaded = True
                in_downloading_process = False
                return True
            else:
                log.log(script_name,"failed to download file.")
                in_downloading_process = False
                self.downloaded = False
                return False
        else:
            in_downloading_process = False
            return False


    #extracted bool

    def extract_course(self):
        if self.downloaded:
            try:
                files = chef.read_and_extract_zip(self.file_name,['cameraVoip','screenshare'],[])
            except:
                log.log(script_name,"error in getting files")
                self.extracted = False
                return False
            try:
                parsedfiles = chef.export_time_and_flv_screen_shares_and_voips(files)
            except:
                log.log(script_name, "error in parsing files")
                self.extracted = False
                return False
            try:
                result = chef.export_files_as_mov(parsedfiles,options.mp4_export_path,self.file_name)
            except:
                log.log(script_name, "error in converting files")
                self.extracted = False
                return False
            else:
                if result == True:
                    self.extracted = True
                else:
                    self.extracted = False
                    return False
        else:
            self.extracted = False
            return False

    def clear_cache_and_data(self):
            prosumer.clear_old_file_cache(filename=self.file_name)





