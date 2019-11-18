import json

import tornado.web

from pymongo import ReturnDocument


class UsersHandler(tornado.web.RequestHandler):
    async def get(self, uuid):
        print(uuid)
        user = await self.settings["mongo_db"].users_collection.find_one(
            {"uuid": uuid}, {"_id": 0})

        if user is None:
            raise tornado.web.HTTPError(
                404, f"Missing user: {uuid}")

        self.finish(json.dumps(user))

    async def post(self):
        new_user = await self.settings["mongo_db"].users_collection.insert_one(
            json.loads(self.request.body))

        self.set_status(204)
        self.finish("new user added")

    async def patch(self, name):
        user = await self.settings["mongo_db"].users_collection.find_one_and_update(
            {"name": name},
            {"$push": {"fruit": json.loads(
                self.request.body)}}, projection={"_id": 0}, return_document=ReturnDocument.AFTER
        )

        self.set_status(200)
        self.finish(json.dumps(user))
