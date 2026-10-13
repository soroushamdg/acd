import csv,logging
from mainThreads import acManager

def str_to_bool(string : str):
    if 'true' in string.lower():
        return True
    else:
        return False

def read_file_and_return_objects(acQueueListManager : acManager.acQueueManager,filepath,loginactionurl):
    try:
        csv_file = open(filepath)
    except Exception as msg:
        logging.debug(msg)
        return False
    try:
        csv_reader = csv.reader(csv_file,delimiter=',')
    except Exception as msg:
        logging.debug(msg)
        return False

    for row in csv_reader:
        if len(row) != 4:
            continue

        filename, dlassets, merge_files, course_link = row

        filename = str(filename).lstrip().rstrip()
        course_link = str(course_link).lstrip().rstrip()
        merge_files = str_to_bool(str(merge_files).lstrip().rstrip())
        dlassets = str_to_bool(str(dlassets).lstrip().rstrip())

        try:
            assert not acManager.check_if_filename_exists(filename=filename),f'QUEUE FILE PARSER : File name already exists in exports folder. \nName : {filename}'
        except Exception as msg:
            logging.debug(msg)
            logging.error(f'File name already exists in exports folder. -> {filename}')
            continue

        try:
            assert acManager.validate_input_url(loginurl=loginactionurl,courseurl=course_link),f'URL is not valid. {loginactionurl} != {course_link}'
        except Exception as msg:
            logging.debug(msg)
            logging.error(f'URL is not valid. {loginactionurl} != {course_link}')
            continue

        status = acQueueListManager.add_to_queue(course_url=course_link,
                                               filename=filename,
                                               merge_files=merge_files,
                                               download_assets=dlassets)
        if status == "DUPLICATE":
            logging.debug('Duplicated item' + 'Please enter different URL and filename.')
            continue

    return acQueueListManager
