import functools
import os

import motor.motor_tornado
import tornado.httpserver
import tornado.ioloop
import tornado.platform.asyncio
import tornado.web

from service.handlers.users_handler import UsersHandler
from service.handlers.add_user_handler import AddUserHandler
from service.handlers.locations_handler import LocationsHandler
from service.handlers.personality_handler import PersonalityHandler
from service.handlers.api_handler import ApiHandler


def make_app(config):
    return tornado.web.Application([
        ("/api/users/(.*)", UsersHandler),
        ("/api/users", AddUserHandler),
        ("/api/locations/(.*)", LocationsHandler),
        ("/api/personality/(.*)", PersonalityHandler),
        ("/api", ApiHandler)
    ], **config)


def main(environ):
    tornado.platform.asyncio.AsyncIOMainLoop().install()
    ioloop = tornado.ioloop.IOLoop.instance()

    motor_client = motor.motor_tornado.MotorClient(str(
        os.environ.get("PROD_MONGODB")))

    mongo_db = motor_client["hosting_test"]

    app = make_app({
        "motor_client": motor_client,
        "mongo_db": mongo_db
    })

    server = tornado.httpserver.HTTPServer(app)
    port = int(os.environ.get("PORT", 9090))
    server.listen(port)

    ioloop.start()


if __name__ == "__main__":
    main(os.environ)
