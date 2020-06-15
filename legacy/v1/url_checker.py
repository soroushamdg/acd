
def extract_download_url(url,filename = None,selected_login = False):
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
    elif selected_login and 'special_dl_link' in selected_login:
        return {
            "filename": urllist[3],
            "url": str(urllist[0] + "//" + urllist[2] + '/' + urllist[3] + '/' if urllist[0] == "http" or "https" else "http://" +urllist[0] + '/' +urllist[1] + '/') + f'output/{filename}.cdata?download=zip',
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


def check_if_link_is_valid(link,selected_login = False):
    if 'adobeconnect/joinrecording' in link and 'http' in link:
        return True
    elif 'lms3.srbiau.ac.ir' in link and any(['http' in link,'https' in link]) and len(link.split('/')) == 4:
        return True
    elif 'vc25.sbu.ac.ir' in link and any(['http' in link,'https' in link]) and len(link.split('/')) == 4:
        return True
    elif selected_login != False and "special_dl_url" in selected_login and any(['http' in link,'https' in link]):
        return True
    else:
        return False

def check(url,db):
    print("URL VALIDATION :",check_if_link_is_valid(url,db))
    print("URL EXTRACTION :",extract_download_url(url,None,db))