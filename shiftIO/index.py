import asyncio,random
import tornado.web
import tornado.ioloop
import socket
import webbrowser


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

    webbrowser.open(f'http://{socket.gethostname()}:{port}',new=2)

    tornado.ioloop.IOLoop.instance().start()

