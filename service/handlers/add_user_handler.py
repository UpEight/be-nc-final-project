import json

import tornado.web

from pymongo import ReturnDocument


class AddUserHandler(tornado.web.RequestHandler):
    async def post(self):
        if (json.loads(self.request.body)["uuid"] == ""):
            raise tornado.web.HTTPError(
                400, f"Bad Request")

        uuid = json.loads(self.request.body)["uuid"]

        existing_user = await self.settings["mongo_db"].users_collection.find_one(
            {"uuid": uuid}, {"_id": 0})

        if (existing_user != None):
            raise tornado.web.HTTPError(
                400, f"Bad Request - user already exists")

        new_user = await self.settings["mongo_db"].users_collection.insert_one(
            json.loads(self.request.body))
        print(new_user.inserted_id)

        if (new_user.acknowledged == True):
            self.set_status(200)
            self.finish(json.dumps(json.loads(self.request.body)))
