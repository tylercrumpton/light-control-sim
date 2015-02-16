import tornado.ioloop
import tornado.web
import os
import RPIO

# Define the room LED IO pins:
rooms = {"living":{"pin":2, "on":True},   #J8 pin: 3
         "kitchen":{"pin":3, "on":True},  #J8 pin: 5
         "bed1":{"pin":4, "on":True},     #J8 pin: 7
         "bed2":{"pin":17, "on":True},    #J8 pin: 11
         "bed3":{"pin":18, "on":True},    #J8 pin: 12
         "laundry":{"pin":27, "on":True}, #J8 pin: 13
        }

# Setup the output pins:
for room in rooms:
    RPIO.setup(rooms[room]["pin"], RPIO.OUT)

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
        name_lower = name.lower()
        command_lower = command.lower()
        if name_lower in rooms.keys():
            if command_lower == "on":
                response = "Turning '{}' light on.".format(name_lower)
                rooms[name_lower]["on"] = True
                RPIO.output(rooms[name_lower]["pin"], True)
            elif command_lower == "off":
                response = "Turning '{}' light off.".format(name_lower)
                rooms[name_lower]["on"] = True
                RPIO.output(rooms[name_lower]["pin"], False)
            elif command_lower == "toggle":
                new_state = not rooms[name_lower]["on"]
                rooms[name_lower]["on"] = new_state
                response = "Toggling '{}' light from {}.".format(name_lower, "off to on" if new_state else "on to off")
                RPIO.output(rooms[name_lower]["pin"], new_state)
            else:
                response = "Cannot perform command '{}' on room '{}'.".format(command_lower, name_lower)
        else:
            response = "No room with name '{}' exists.".format(name_lower)
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
