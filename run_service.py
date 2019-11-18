import functools
import os

import motor.motor_tornado
import tornado.httpserver
import tornado.ioloop
import tornado.platform.asyncio
import tornado.web

from tornado.options import define, options

from service.handlers.users_handler import UsersHandler

define("port", default=9090, help="run on the given port", type=int)


def make_app(config):
    return tornado.web.Application([
        ("/api/users/(.*)", UsersHandler)
    ], **config)


def main(environ):
    tornado.platform.asyncio.AsyncIOMainLoop().install()
    ioloop = tornado.ioloop.IOLoop.current()

    motor_client = motor.motor_tornado.MotorClient(str(
        os.environ.get("PROD_MONGODB")))

    mongo_db = motor_client["hosting_test"]

    app = make_app({
        "motor_client": motor_client,
        "mongo_db": mongo_db
    })

    server = tornado.httpserver.HTTPServer(app)
    server.listen(options.port)

    ioloop.start()


if __name__ == "__main__":
    main(os.environ)
