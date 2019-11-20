import json

import tornado.web

from pymongo import ReturnDocument

from datetime import datetime


class UsersHandler(tornado.web.RequestHandler):
    async def get(self, uuid):
        user = await self.settings["mongo_db"].users_collection.find_one(
            {"uuid": uuid}, {"_id": 0})

        if user is None:
            raise tornado.web.HTTPError(
                404, f"Missing user: {uuid}")

        current_date = datetime.today()
        start_of_current_date = current_date.replace(hour=00, minute=00)

        current_agenda = user["Agenda"]["going"]
        history = user["Agenda"]["history"]

        for item in current_agenda:
            meeting_date = item["date"]
            datetime_object = datetime.strptime(meeting_date, '%Y-%m-%d')
            end_of_meeting_date = datetime_object.replace(hour=23, minute=59)

            if (start_of_current_date > end_of_meeting_date):
                history.append(item)
                current_agenda.remove(item)

        user = await self.settings["mongo_db"].users_collection.find_one_and_update(
            {"uuid": uuid},
            {"$set": {"Agenda.going": current_agenda, "Agenda.history": history}}, projection={"_id": 0}, return_document=ReturnDocument.AFTER
        )

        self.set_status(200)
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

    async def delete(self, uuid):
        id = json.loads(self.request.body)["id"]

        if (id == ""):
            raise tornado.web.HTTPError(
                400, f"Bad Request")

        user = await self.settings["mongo_db"].users_collection.find_one(
            {"uuid": uuid}, {"_id": 0})

        current_agenda = user["Agenda"]["going"]

        for item in current_agenda:
            if (id == item["id"]):
                current_agenda.remove(item)

        user = await self.settings["mongo_db"].users_collection.find_one_and_update(
            {"uuid": uuid},
            {"$set": {"Agenda.going": current_agenda}}, projection={"_id": 0}, return_document=ReturnDocument.AFTER
        )

        self.set_status(200)
        self.finish(json.dumps(user))
