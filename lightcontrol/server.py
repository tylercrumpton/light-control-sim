import tornado.ioloop
import tornado.web
import os
import RPIO

# Setup the output pins:
RPIO.setup(22, RPIO.OUT)

class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.write("Hello, world")

class StaticHandler(tornado.web.StaticFileHandler):
    def get_absolute_path(self, root, path):
        if path == "":
            return super(StaticHandler, self).get_absolute_path(root, "index.html")
        else:
            return super(StaticHandler, self).get_absolute_path(root, path)
            
class SetLightByNameHandler(tornado.web.RequestHandler):
    def get(self, name, command):
        if command.lower() == "on":
            response = "Turning %s light on." % name.lower()
            RPIO.output(22, True)
        if command.lower() == "off":
            response = "Turning %s light off." % name.lower()
            RPIO.output(22, False)
        if command.lower() == "toggle":
            response = "Toggling %s light." % name.lower()
        print response
        self.write(response)
        
settings = {
    "static_path": os.path.join(os.path.dirname(__file__), "lightsim")
}
        
application = tornado.web.Application([
    (r"/lightsim/(.*)", StaticHandler, dict(path=settings['static_path'])),
    (r"/hardware/setlightbyname/([A-z]+)/([A-z]+)", SetLightByNameHandler),
    (r"/", MainHandler),
])

if __name__ == "__main__":
    application.listen(8888)
    tornado.ioloop.IOLoop.instance().start()
