import json

import tornado.web


class UsersHandler(tornado.web.RequestHandler):
    async def get(self, name):
        user = await self.settings["mongo_db"].users_collection.find_one(
            {"name": name})

        if user is None:
            raise tornado.web.HTTPError(
                404, f"Missing user: {name}")

        print(user['_id'])

        # self.finish(json.dumps(user.__class__))

        self.finish(json.dumps(
            {'name': user['name'], 'interests': user['interests']}))

    async def post(self, name):
        await self.settings["mongo_db"].users_collection.replace_one(
            {"name": name},
            {
                "name": name,
                "interests": json.loads(self.request.body)['interests'],
                "fruit": json.loads(self.request.body)['fruit'],
                "object": {"object1": json.loads(self.request.body)["object1"]}
            },
            upsert=True)

        self.set_status(204)
        self.finish()
