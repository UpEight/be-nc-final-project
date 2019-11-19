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

    async def patch(self, uuid):
        id = json.loads(self.request.body)["id"]

        if (id == ""):
            raise tornado.web.HTTPError(
                400, f"Bad Request")

        user = await self.settings["mongo_db"].users_collection.find_one(
            {"uuid": uuid}, {"_id": 0})

        current_agenda = user["Agenda"]["going"]

        for item in current_agenda:
            if (id == item["id"]):
                raise tornado.web.HTTPError(
                    400, f"Bad Request - Agenda item already exists")

        user = await self.settings["mongo_db"].users_collection.find_one_and_update(
            {"uuid": uuid},
            {"$push": {"Agenda.going": json.loads(
                self.request.body)}}, projection={"_id": 0}, return_document=ReturnDocument.AFTER
        )

        self.set_status(200)
        self.finish(json.dumps(user))
