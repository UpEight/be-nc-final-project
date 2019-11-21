import json

import tornado.web

from pymongo import ReturnDocument


class PersonalityHandler(tornado.web.RequestHandler):
    async def patch(self, uuid):
        print(uuid)

        user = await self.settings["mongo_db"].users_collection.find_one_and_update(
            {"uuid": uuid},
            {"$set": {"personality": json.loads(self.request.body)}}, projection={"_id": 0}, return_document=ReturnDocument.AFTER
        )

        self.set_status(200)
        self.finish(json.dumps(user))
