from prettytable import PrettyTable
from pyLog import options
import os

data_table = PrettyTable()

def review_by_year(start_date,end_date,review_by = options.log_method,path = options.log_file_path,file_root_names = options.log_file_name):
    try:
        os.chdir(path+"log")
    except:
        print("No such directory!")
        return
    else:
        print("found log files directory.")

    #TODO : ADD READING AND PARSING FILES

