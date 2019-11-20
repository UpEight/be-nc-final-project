import json

import tornado.web

from pymongo import ReturnDocument


class LocationsHandler(tornado.web.RequestHandler):
    async def get(self, id):
        count = await self.settings["mongo_db"].users_collection.count_documents(
            {"Agenda.going": {"$elemMatch": {"id": id}}})
        self.set_status(200)
        self.finish(json.dumps(count))
