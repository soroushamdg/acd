import asyncio,random
import os
import pathlib
import itertools as IT
import sys
import tempfile
import tornado.web
import tornado.ioloop
import socket
import settings
from netifaces import interfaces, ifaddresses, AF_INET
from PyQt5 import QtCore
import threading

import logging

from tornado.platform.asyncio import AnyThreadEventLoopPolicy

logging.basicConfig(filename=settings.SETTINGS['LOG_PATH'],filemode='a',level=settings.SETTINGS['LOG_LEVEL'],datefmt='%d-%b-%y %H:%M:%S',format="%(levelname)s -- %(asctime)s -- %(name)s -- %(message)s")

def get_platform_architecture():
    if sys.platform.startswith('linux') and sys.maxsize > 2 ** 32:
        platform = 'linux'
        architecture = '64'
    elif sys.platform == 'darwin':
        platform = 'mac'
        architecture = '64'
    elif sys.platform.startswith('win'):
        platform = 'win'
        architecture = '32'
    else:
        raise RuntimeError('Could not determine chromedriver download URL for this platform.')
    return platform, architecture

def uniquify(path, sep = ''):
    def name_sequence():
        count = IT.count()
        yield ''
        while True:
            yield '{s} - {n:d}'.format(s = sep, n = next(count))
    orig = tempfile._name_sequence
    with tempfile._once_lock:
        tempfile._name_sequence = name_sequence()
        path = os.path.normpath(path)
        dirname, basename = os.path.split(path)
        filename, ext = os.path.splitext(basename)
        fd, filename = tempfile.mkstemp(dir = dirname, prefix = filename, suffix = ext)
        tempfile._name_sequence = orig
    os.close(fd)
    return filename

def find_ip_address(ret_single_ip=False):
    addresses = []
    for ifaceame in interfaces():
        for i in ifaddresses(ifaceame).setdefault(AF_INET, [{'addr': 'No IP addr'}]):
            if '192.168' in i['addr']:
                addresses.append(i['addr'])
    return addresses if not ret_single_ip else addresses[0]



class shiftioUploadHandler(tornado.web.RequestHandler):
    def post(self):
        files = self.request.files["filesqueue"]
        for f in files:
            if f.filename.split('.')[-1] in settings.return_shiftio_valid_types():
                fh = open(uniquify(pathlib.Path(settings.SETTINGS['SHIFTIO_EXPORT_PATH']).joinpath(f.filename)),
                          "wb")
                fh.write(f.body)
                fh.close()
        self.redirect("/")

    def get(self):
        self.render(settings.return_shiftio_assets_path(html=True), file_types=' .'+" .".join(settings.return_shiftio_valid_types()))

class shiftIOServerThread(QtCore.QThread):

    status = False

    def __init__(self):
        QtCore.QThread.__init__(self)
        self.port = random.randrange(1000, 10000)
        self.ip_addresses = find_ip_address()
        self.main_ip = find_ip_address(ret_single_ip=True)
        self.hostname = socket.gethostname()

    def __del__(self):
        self.wait()

    def stop_server(self):
        try:
            tornado.ioloop.IOLoop.instance().stop()
        except:
            pass

    def run(self):
        try:
            asyncio.set_event_loop_policy(AnyThreadEventLoopPolicy())
            app = tornado.web.Application([
                ("/", shiftioUploadHandler),
                ("/assets/(.*)", tornado.web.StaticFileHandler, {'path': settings.return_shiftio_assets_path()})
            ])
            server = tornado.httpserver.HTTPServer(app,
                                                   max_buffer_size=167772160  # 160 MB
                                                   )
            server.listen(self.port)
            # logging.getLogger("tornado.access").propagate = False
        except Exception as msg:
            logging.debug(msg)
            self.status = False
            return
        else:
            self.status = True

        try:
            tornado.ioloop.IOLoop.instance().start()
        except Exception as msg:
            logging.debug(msg)
            return


