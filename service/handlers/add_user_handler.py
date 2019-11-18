import json

import tornado.web

from pymongo import ReturnDocument


class AddUserHandler(tornado.web.RequestHandler):
    async def post(self):
        new_user = await self.settings["mongo_db"].users_collection.insert_one(
            json.loads(self.request.body))

        self.set_status(204)
        self.finish("new user added")
