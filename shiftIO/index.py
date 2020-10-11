import asyncio
import tornado.web
import tornado.ioloop

class uploadImgHandler(tornado.web.RequestHandler):
    def post(self):
        files = self.request.files["fileImage"]
        print(files)
        for f in files:
            print(f)
            fh = open(f"upload/{f.filename}", "wb")
            fh.write(f.body)
            fh.close()
            self.write(f"http://localhost:1234/upload/{f.filename}")
    def get(self):
        self.render("index.html")

if (__name__ == "__main__"):
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

    app = tornado.web.Application([
        ("/", uploadImgHandler),
        ("/upload/(.*)", tornado.web.StaticFileHandler, {'path': 'upload'})
    ])
    # port = 8882
    # app.listen(port)
    # print(f"Application is ready and listening on port {port}")
    # tornado.ioloop.IOLoop.current().start()
    #

    import ifaddr

    adapters = ifaddr.get_adapters()

    for adapter in adapters:
        if 'wireless' in str(adapter.nice_name).lower():
            print(
            "IPs of network adapter " + adapter.nice_name)
            for ip in adapter.ips:
                print(
                "   %s/%s" % (ip.ip, ip.network_prefix))

    server = tornado.httpserver.HTTPServer(app, max_buffer_size=10485760000)  # 10G
    server.listen(1234)
    print("Listening on port 1234")

    tornado.ioloop.IOLoop.instance().start()