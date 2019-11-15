import functools
import os

import motor.motor_tornado
import tornado.httpserver
import tornado.ioloop
import tornado.platform.asyncio
import tornado.web

from service.handlers.users_handler import UsersHandler

from config import prod

# os.environ["MONGODB_URI"] = "mongodb://127.0.0.1:27017"

os.environ["MONGODB_URI"] = prod


os.environ["SERVER_PORT"] = "9090"


def make_app(config):
    return tornado.web.Application([
        ("/api/users/(.*)", UsersHandler)
    ], **config)


def main(environ):
    tornado.platform.asyncio.AsyncIOMainLoop().install()
    ioloop = tornado.ioloop.IOLoop.current()

    motor_client = motor.motor_tornado.MotorClient(
        environ["MONGODB_URI"])

    mongo_db = motor_client["hosting_test"]

    app = make_app({
        "motor_client": motor_client,
        "mongo_db": mongo_db
    })

    server = tornado.httpserver.HTTPServer(app)
    server.listen(int(environ["SERVER_PORT"]), "localhost")

    ioloop.start()


if __name__ == "__main__":
    main(os.environ)
