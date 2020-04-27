"""
Prosumer
This script will download file into selected path, will return status of download and will show progress.
"""

from selenium.webdriver import Chrome
from selenium.webdriver.chrome.options import Options

from pyLog.pylog import log
from backend.options import script_name, temp_path,get_file_size_in_cache, remove_old_files_in_cache,driver_path

from time import sleep

opts = Options()
# opts.add_argument("--headless")
opts.add_argument("--window-size=1920x1080")
opts.add_argument("--disable-notifications")
opts.add_argument('--no-sandbox')
opts.add_argument('--verbose')
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

def enable_download_headless(browser,download_dir):
    browser.command_executor._commands["send_command"] = ("POST", '/session/$sessionId/chromium/send_command')
    params = {'cmd':'Page.setDownloadBehavior', 'params': {'behavior': 'allow', 'downloadPath': download_dir}}
    browser.execute("send_command", params)

try:
    ac_browser = Chrome(options=opts, executable_path= driver_path)
except:
    log.log(script_name,"can't launch acd_engine.")

def check_if_link_is_valid(link):
    if 'adobeconnect/joinrecording' in link and 'http' in link:
        return True
    elif 'lms3.srbiau.ac.ir' in link and any(['http' in link,'https' in link]) and len(link.split('/')) == 4:
        return True
    else:
        return False

def get_download_progress(filename):
    """
    alogrithm : -> checks if file with .crdownload is there, if it is get size, if not download is completed.
    :return:
    """
    # with .crdownload
    if get_file_size_in_cache(filename=filename+'.crdownload') != False:
        return ('inprogress',get_file_size_in_cache(filename=filename+'.crdownload'))
    else:
        if get_file_size_in_cache(filename) != False:
            return ('finished',get_file_size_in_cache(filename=filename))
        else:
            return (False,0)

def clear_old_file_cache(filename):
    assert remove_old_files_in_cache(filename),"error in removing old cache."
    return True

def delete_cookies():
    ac_browser.delete_all_cookies()


logged_in = False
def login_into_system(info_dict,username,password):
    """
    dict map:
    {"university_id":{"login_url":"",
    "username_find_method": "" -> class,name,id
    "username_find_value": "" -> class name or...
    "username_find_list_index": -> int
    "password_find_method": "" -> class,name,id
    "password_find_value": "" -> class name or...
    "password_find_list_index": -> int
    "submit_find_method": "" -> class,name,id
    "submit_find_value": "" -> class name or...
    "submit_find_list_index": -> int
    "can_submit_by_keyboard": "" -> True , False

    }

    """
    # info_dict = {"login_url":"https://vc.kntu.ac.ir/login/index.php",
    #              "ufm":"id",
    #              "ufv":"username",
    #              "ufli":0,
    #              "pfm":"id",
    #              "pfv":"password",
    #              "pfli":0,
    #              "sfm":"id",
    #              "sfv":"submit",
    #              "sfli":0,
    #              "csbk":True
    #              }
    for i in range(5):
        try:
            ac_browser.get(info_dict["login_url"])
        except:
            if i <4:
                sleep(1)
                continue
            else:
                log.log(script_name,"can't get url, check your internet connection")
                return False
        else:
            sleep(3)
            break

    assert 'ورود' in ac_browser.title,"LOGIN PAGE DIDN'T LOAD UP!"

    #find username field.

    try:
        if info_dict["ufm"] == "id":
            username_field = ac_browser.find_element_by_id(info_dict["ufv"])
        elif info_dict["ufm"] == "class":
            username_field = ac_browser.find_elements_by_class_name(info_dict["ufv"])[int(info_dict["ufli"])]
        else:
            username_field = ac_browser.find_elements_by_name(info_dict["ufv"])[int(info_dict["ufli"])]
    except:
        log.log(script_name,"can't find username field, something wrong with url maybe. please contact me.")
        return False
    else:
        username_field.send_keys(username)

    #find password field.
    try:
        if info_dict["pfm"] == "id":
            password_field = ac_browser.find_element_by_id(info_dict["pfv"])
        elif info_dict["pfm"] == "class":
            password_field = ac_browser.find_elements_by_class_name(info_dict["pfv"])[int(info_dict["pfli"])]
        else:
            password_field = ac_browser.find_elements_by_name(info_dict["pfv"])[int(info_dict["pfli"])]
    except:
        log.log(script_name,"can't find password field, something wrong with url maybe. please contact me.")
        return False
    else:
        password_field.send_keys(password)

    #find and click submit button.
    if info_dict["csbk"]:
        password_field.submit()
    else:
        try:
            if info_dict["sfm"] == "id":
                submit_field = ac_browser.find_element_by_id(info_dict["sfv"])
            elif info_dict["sfm"] == "class":
                submit_field = ac_browser.find_elements_by_class_name(info_dict["sfv"])[int(info_dict["sfli"])]
            else:
                submit_field = ac_browser.find_elements_by_name(info_dict["sfv"])[int(info_dict["sfli"])]
        except:
            log.log(script_name, "can't find password field, something wrong with url maybe. please contact me.")
            return False
        else:
            submit_field.click()


    #wait for login
    sleep(3)
    assert all(['ورود' not in ac_browser.title, 'login' not in str(ac_browser.title).lower()]),'ERR:112,CAN NOT LOGIN ~ CHECK YOUR USERNAME PASS, IF CORRECT CONTACT ME.'

    log.log(script_name,"login successful.")

    global logged_in
    logged_in = True

    return True


def extract_download_url(url,filename = None):
    urllist = url.split('/')
    if "get-player" in url:
        return {"filename" : urllist[-2],
                "url": str(urllist[0] + "//" + urllist[2] + '/' + urllist[-2] + '/' if urllist[0] == "http" or "https" else "http://" + urllist[0] + '/' + urllist[-2] + '/') + f'output/{filename}.cdata?download=zip',}
    elif 'joinrecording' in url:
        return {"filename" : urllist[5].split('&')[1].split('=')[1] if urllist[0] == "http" or "https" else urllist[3].split('&')[1].split('=')[1],
            "url" : str(urllist[0] + "//" + urllist[2] + '/' + urllist[3] + '/' if urllist[0] == "http" or "https" else "http://" + urllist[0] + '/' + urllist[1] + '/') + f'output/{filename}.cdata?download=zip',
            }
    elif 'lms3.srbiau.ac.ir' in url:
        return {"filename" : urllist[3],
                "url" : str(urllist[0] + "//" + urllist[2] + '/' + urllist[3] + '/' if urllist[0] == "http" or "https" else "http://" + urllist[0] + '/' + urllist[1] + '/') + f'output/{filename}.cdata?download=zip',
                }
    else:
        return {
            "filename": urllist[3] if urllist[0] == "http" or "https" else urllist[1],
            "url": str(urllist[0] + "//" + urllist[2] + '/' + urllist[3] + '/' if urllist[
                                                                                      0] == "http" or "https" else "http://" +
                                                                                                                   urllist[
                                                                                                                       0] + '/' +
                                                                                                                   urllist[
                                                                                                                       1] + '/') + f'output/{filename}.cdata?download=zip',
            }

def download_file(url,filename):



    ac_browser.get(url)
    sleep(5)
    # enable_download_headless(ac_browser,temp_path)
    filename = filename
    try:
        clear_old_file_cache(filename)
    except:
        log.log(script_name,"error in removing old cache.")
        assert False,"error in removing old cache."

    if 'lms3.srbiau.ac.ir' in url:
        ac_browser.get(extract_download_url(url,filename)["url"])
    else:
        ac_browser.get(extract_download_url(ac_browser.current_url,filename)["url"])



    while(1):
        sleep(1)
        dlstatus = get_download_progress(filename+'.cdata')
        if 'inprogress' == dlstatus[0]:
            log.log(script_name,f"{filename} -> {dlstatus[1]} bytes downloaded. in progress.")
        elif 'finished' == dlstatus[0]:
            log.log(script_name,f"{filename} download finished.{dlstatus[1]} bytes downloaded.")
            return True
        else:
            assert dlstatus[0],"ERR194 - ERROR IN DOWNLOADING OR SAVING DATA."




#
# info_dict = {'kntu':{"login_url":"https://vc.kntu.ac.ir/login/index.php",
#                   "ufm":"id",
#              "ufv":"username",
#                  "ufli":0,
#                 "pfm":"id",
#                   "pfv":"password",
#                   "pfli":0,
#                   "sfm":"id",
#                   "sfv":"submit",
#                   "sfli":0,
#                   "csbk":True
#                  },
#              'lm13-iauec': {"login_url": "http://lms13.iauec.ac.ir/login/index.php",
#                       "ufm": "id",
#                       "ufv": "username",
#                       "ufli": 0,
#                       "pfm": "id",
#                       "pfv": "password",
#                       "pfli": 0,
#                       "sfm": "id",
#                       "sfv": "submit",
#                       "sfli": 0,
#                       "csbk": True
#                       }
#              }

# # print(login_into_system(info_dict['lm13-iauec'],"9625512482","0021581770"))
# print(login_into_system(info_dict['kntu'],"9628503","9628503"))
#
# ac_browser.save_screenshot("afterlogin.png")
# download_file("https://vc.kntu.ac.ir/mod/adobeconnect/joinrecording.php?id=13167&recording=1038179&groupid=0&sesskey=Dt1XDsiLWN")
# ac_browser.save_screenshot("afterdownload.png")
#
#
# log.close_file()