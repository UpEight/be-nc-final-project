import json

import tornado.web

from pymongo import ReturnDocument


class UsersHandler(tornado.web.RequestHandler):
    async def get(self, name):
        user = await self.settings["mongo_db"].users_collection.find_one(
            {"name": name}, {"_id": 0})

        if user is None:
            raise tornado.web.HTTPError(
                404, f"Missing user: {name}")

        self.finish(json.dumps(user))

    async def post(self, name):
        await self.settings["mongo_db"].users_collection.replace_one(
            {"name": name},
            {
                "name": name,
                "interests": json.loads(self.request.body)['interests'],
                "fruit": json.loads(self.request.body)['fruit']
            },
            upsert=True)

        self.set_status(204)
        self.finish()

    async def patch(self, name):
        user = await self.settings["mongo_db"].users_collection.find_one_and_update(
            {"name": name},
            {"$push": {"fruit": json.loads(
                self.request.body)}}, projection={"_id": 0}, return_document=ReturnDocument.AFTER
        )

        self.set_status(200)
        self.finish(json.dumps(user))
