def progress_percentage(self, jobs_done):
    return 100 * jobs_done / (len(self.courses) * 2)


def get_and_show_downloaded_bytes(self, pre_message, downloading_object):
    print('getting download status.')
    while (not downloading_object.downloaded):
        QtWidgets.QApplication.processEvents()
        time.sleep(5)
        if bytes_downloaded > 1000:
            self.statusbar.showMessage(pre_message + ' ' + str(bytes_downloaded / 1000) + 'KBs downloaded')
        elif bytes_downloaded > 1000000:
            self.statusbar.showMessage(pre_message + ' ' + str(bytes_downloaded / 1000000) + 'MBs downloaded')
        elif bytes_downloaded < 1000:
            self.statusbar.showMessage(pre_message + ' ' + str(bytes_downloaded) + 'Bytes downloaded')
        else:
            self.statusbar.showMessage(pre_message + ' ' + str(bytes_downloaded / 1000000000) + 'GBs downloaded')


def start_downloading_button(self):
    self.statusbar.clearMessage()
    QtWidgets.QApplication.processEvents()
    time.sleep(0.5)
    if self.check_start_download_stage():
        jobs_done = 0
        failed = 0
        self.enable_disable_stages([], ['stage1', 'stage2', 'stage3'])
        self.downloadProgressBar.setEnabled(True)
        self.failDownloadLCDNumber.setEnabled(True)
        QtWidgets.QApplication.processEvents()
        to_download_list = list(self.courses.values())
        for i in range(len(to_download_list) + 1):
            threads = []

            # add jobs to threads
            if i == 0:
                t_download = threading.Thread(target=to_download_list[i].download_course)
                threads.append(t_download)
                msg = f'Downloading {to_download_list[i].file_name}'
                t_message = threading.Thread(target=self.get_and_show_downloaded_bytes,
                                             args=(msg, to_download_list[i],))
                threads.append(t_message)
                # to_download_list[i].download_course()
            elif i == len(to_download_list):
                t_extract = threading.Thread(target=to_download_list[i - 1].extract_course)
                self.statusbar.showMessage(f'Extracting {to_download_list[i - 1].file_name}')
                threads.append(t_extract)
                # to_download_list[i-1].extract_course()
            else:
                t_download = threading.Thread(target=to_download_list[i].download_course)
                threads.append(t_download)
                t_extract = threading.Thread(target=to_download_list[i - 1].extract_course)
                threads.append(t_extract)
                msg = f'Downloading {to_download_list[i].file_name} + Extracting {to_download_list[i - 1].file_name}'
                t_message = threading.Thread(target=self.get_and_show_downloaded_bytes,
                                             args=(msg, to_download_list[i],))
                threads.append(t_message)

            QtWidgets.QApplication.processEvents()

            log.log(__name__, f'added jobs to threads. round {i + 1}')
            # starting threads
            for thread in threads:
                thread.start()

            QtWidgets.QApplication.processEvents()
            # waiting to finish

            for thread in threads:
                thread.join()

            self.statusbar.clearMessage()
            QtWidgets.QApplication.processEvents()
            # checking which is done which not.
            if i == 0:
                if to_download_list[i].downloaded:
                    jobs_done += 1
                else:
                    failed += 1
            elif i == len(to_download_list):
                if to_download_list[i - 1].downloaded and to_download_list[i - 1].extracted:
                    jobs_done += 2
                elif to_download_list[i - 1].downloaded and not to_download_list[i - 1].extracted:
                    failed += 1
                else:
                    pass
            else:
                if to_download_list[i].downloaded:
                    jobs_done += 1
                if to_download_list[i - 1].downloaded and to_download_list[i - 1].extracted:
                    jobs_done += 2
                elif to_download_list[i - 1].downloaded and not to_download_list[i - 1].extracted:
                    failed += 1
                else:
                    pass
            # update ui progress
            self.downloadProgressBar.setValue(int(self.progress_percentage(jobs_done)))
            self.failDownloadLCDNumber.display(failed)
            QtWidgets.QApplication.processEvents()
        self.show_message_box('Yohooo!',
                              f'{len(to_download_list) - failed} course(s) download and extracting finished!')
        QtWidgets.QApplication.processEvents()
        self.clean_up_after_download()
        return True
    else:
        self.show_message_box('Error', "Something is wrong and I can't find what it is:| cantact my creator.")
        QtWidgets.QApplication.processEvents()
        return False