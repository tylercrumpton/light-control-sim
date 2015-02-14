import tornado.ioloop
import tornado.web
import os

class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.write("Hello, world")

class StaticHandler(tornado.web.StaticFileHandler):
    def get_absolute_path(self, root, path):
        if path == "":
            return super(StaticHandler, self).get_absolute_path(root, "index.html")
        else:
            return super(StaticHandler, self).get_absolute_path(root, path)
        
settings = {
    "static_path": os.path.join(os.path.dirname(__file__), "lightsim")
}
        
application = tornado.web.Application([
    (r"/lightsim/(.*)", StaticHandler, dict(path=settings['static_path'])),
    (r"/", MainHandler),
])

if __name__ == "__main__":
    application.listen(8888)
    tornado.ioloop.IOLoop.instance().start()