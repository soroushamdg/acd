import asyncio,random
import tornado.web
import tornado.ioloop
import socket
import webbrowser
from netifaces import interfaces, ifaddresses, AF_INET


def find_ip_address(ret_single_ip=False):
    addresses = []
    for ifaceame in interfaces():
        for i in ifaddresses(ifaceame).setdefault(AF_INET, [{'addr': 'No IP addr'}]):
            if '192.168' in i['addr']:
                addresses.append(i['addr'])
    return addresses if not ret_single_ip else addresses[0]

class uploadImgHandler(tornado.web.RequestHandler):
    def post(self):
        files = self.request.files["fileImage"]
        print(files)
        for f in files:
            print(type(f),f.keys())
            fh = open(f"upload/{f.filename}", "wb")
            fh.write(f.body)
            fh.close()
            self.write(f"http://{socket.gethostname()}:{port}/upload/{f.filename}")
    def get(self):
            self.render("index.html")

if (__name__ == "__main__"):
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

    app = tornado.web.Application([
        ("/", uploadImgHandler),
        ("/upload/(.*)", tornado.web.StaticFileHandler, {'path': 'upload'})
    ])

    server = tornado.httpserver.HTTPServer(app,
                                           max_buffer_size=167772160  # 160 MB
     )
    port = random.randrange(1000,10000)
    server.listen(port)
    print(f"Listening on {socket.gethostname()}:{port}")
    for address in find_ip_address():
        print(f'connect via -> {address}:{port}')

    webbrowser.open(f'http://{socket.gethostname()}:{port}',new=2)

    tornado.ioloop.IOLoop.instance().start()

