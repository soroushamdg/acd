from pyLog import options
import os
import datetime
import csv

class logger():

    def file_name_generator(self):
        date = self.time_controller.now()
        if options.log_method.lower() == "mon":
            return str(f"{date.strftime('%m-%Y')}-" + options.log_file_name)
        elif options.log_method.lower() == "yr":
            return f"{date.strftime('%Y')}-" + options.log_file_name
        elif options.log_method.lower() == "day":
            return f"{date.strftime('%d-%m-%Y')}-" + options.log_file_name
        elif options.log_method.lower() == "aio":
            return options.log_file_name
        else:
            return False

    def init_log_file(self):

        self.log_file_name = self.file_name_generator()
        assert self.log_file_name,"Please fix log_method into proper value in options.py"

        try:
            csv_file = open(self.log_file_name, 'r')
        except:
            print(f"no {self.log_file_name} file found! We will create new one.")
            try:
                file = open(self.log_file_name, 'a+')
                header_writer = csv.writer(file)
                header_writer.writerow(
                    ["file creation date : " + str(datetime.datetime.now().strftime('%d %B %Y %H:%M:%S')), " ", " "])
                header_writer.writerow(["time", "origin", "message"])
                file.close()
                return True
            except Exception as msg:
                print("can't create new csv file. please check administrator access or problems ->", msg)
                return False
        else:
            csv_file.close()
            print(f"{self.log_file_name} file found successfully.")
            return True

    def __init__(self,print_logs = options.print_logging, logging_file_path = options.log_file_path):
        self.print_logs = print_logs
        self.logging_file_path = logging_file_path

        self.time_controller = datetime.datetime

        # Chaning path to logging destination
        while (True):
            try:
                os.chdir(options.log_file_path + r"\log")
            except:
                print("couldn't find ", options.log_file_path + r'\log')
                os.chdir(options.log_file_path)
                os.mkdir("log")
            else:
                break

        assert self.init_log_file(),"couldn't create or open log file."

        self.log_file = open(self.log_file_name,'a+')
        self.csv_log_writer = csv.writer(self.log_file)
        print("logger initiated successfully")
        self.log("LOGGER_MODULE","session Started.")



    # def __del__(self):
    #     self.log("LOGGER_MODULE","LOGGER_MODULE session finished.")
    #     self.log_file.close()


    def write_to_file(self,time,script_name,message):
        try:
            self.csv_log_writer.writerow([str(datetime.datetime.now().strftime('%d %B %Y %H:%M:%S')),
                            str(script_name),str(message)])
        except:
            print("Error in writing log into row")
        else:
            return True


    def log(self,origin,message):

        time = self.time_controller.now()

        assert self.write_to_file(time, origin,message), f"Problem in Logging!\n[{time}] , [{origin}] , [{message}]"

        if self.print_logs:
            print(f"[{time}] , [{origin}] , [{message}]")


    def close_file(self):
        self.log_file.close()