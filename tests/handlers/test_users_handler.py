import json
import os
import unittest
from unittest import mock

import motor.motor_tornado
import tornado.testing

from run_service import make_app
from tests.handlers.handler_test_case import HandlerTestCase


class TestUsersHandler(HandlerTestCase):
    def tearDown(self):
        self.io_loop.run_sync(
            lambda: self.motor_client.drop_database(self.mongo_db))

        super().tearDown()

    def get_app(self):
        self.motor_client = motor.motor_tornado.MotorClient(
            os.environ.get("MONGODB_URI", "mongodb://127.0.0.1:27017"))
        self.mongo_db = self.motor_client["test_db"]

        return make_app({
            "motor_client": self.motor_client,
            "mongo_db": self.mongo_db
        })

    @tornado.testing.gen_test
    async def test_get_returns_404_when_document_does_not_exist_in_database(self):
        response = await self.fetch("/api/users/missing")

        self.assertEqual(404, response.code)

    @tornado.testing.gen_test
    async def test_get_returns_200_when_user_does_exist_in_database(self):
        await self.mongo_db["users_collection"].insert_one({
            "uuid": "PAOy3tOLQNTNpifOKT4bZ5NrKSm2",
            "email": "c.beckett@dummy.com",
            "username": "lordbecks",
            "Profile": {
                "firstname": "Cutler",
                "lastname": "Beckett",
                "img": "",
                "user_description": "Top Boy",
                "age": "45",
                "gender": "m"
            },
            "Agenda": {
                "history": [],
                "going": []
            }})
        response = await self.fetch("/api/users/PAOy3tOLQNTNpifOKT4bZ5NrKSm2")

        self.assertEqual(200, response.code)

    @tornado.testing.gen_test
    async def test_get_user_moves_Agenda_going_items_to_Agenda_history_if_date_is_passed(self):
        await self.mongo_db["users_collection"].insert_one(
            {"uuid": "Sdjhjhj123",
             "email": "c.beckett@dummy.com",
             "username": "lordbecks",
             "Profile": {
                 "firstname": "Cutler",
                 "lastname": "Beckett",
                 "img": "",
                 "user_description": "Top Boy",
                 "age": "45",
                 "gender": "m"
             },
             "Agenda": {
                 "history": [],
                 "going": [
                     {
                         "id": "61c34247dcf1be30d9aba564a005e77749d1dbaf",
                         "date": "2419-12-24",
                         "chatKey": "61c34247dcf1be30d9aba564a005e77749d1dbaf2019-12-24",
                         "name": "London"
                     },
                     {
                         "id": "9cc5acae16ff76d52d7cb449494976935871df85",
                         "date": "2019-11-13",
                         "chatKey": "9cc5acae16ff76d52d7cb449494976935871df852019-11-13",
                         "name": "Royal Exchange Theatre"
                     }
                 ]
             }})

        response = await self.fetch("/api/users/Sdjhjhj123")

        self.assertEqual(200, response.code)

        self.assertEqual(
            {
                "_id": mock.ANY,
                "uuid": "Sdjhjhj123",
                "email": "c.beckett@dummy.com",
                "username": "lordbecks",
                "Profile": {
                    "firstname": "Cutler",
                    "lastname": "Beckett",
                    "img": "",
                    "user_description": "Top Boy",
                    "age": "45",
                    "gender": "m"
                },
                "Agenda": {
                    "history": [
                        {
                            "id": "9cc5acae16ff76d52d7cb449494976935871df85",
                            "date": "2019-11-13",
                            "chatKey": "9cc5acae16ff76d52d7cb449494976935871df852019-11-13",
                            "name": "Royal Exchange Theatre"
                        }
                    ],
                    "going": [
                        {
                            "id": "61c34247dcf1be30d9aba564a005e77749d1dbaf",
                            "date": "2419-12-24",
                            "chatKey": "61c34247dcf1be30d9aba564a005e77749d1dbaf2019-12-24",
                            "name": "London"
                        }
                    ]
                }},
            await self.mongo_db["users_collection"].find_one({"uuid": "Sdjhjhj123"})
        )

    @tornado.testing.gen_test
    async def test_post_inserts_document_into_database_and_returns_inserted_document(self):
        response = await self.fetch("/api/users", method="POST", body=json.dumps(
            {"uuid": "PAOy3tOLQNTNpifOKT4bZ5NrKSm2",
             "email": "c.beckett@dummy.com",
             "username": "lordbecks",
             "Profile": {
                 "firstname": "Cutler",
                 "lastname": "Beckett",
                 "img": "",
                 "user_description": "Top Boy",
                 "age": "45",
                 "gender": "m"
             },
             "Agenda": {
                 "history": [],
                 "going": []
             }}))

        self.assertEqual(200, response.code)

        self.assertEqual(
            {
                "_id": mock.ANY,
                "uuid": "PAOy3tOLQNTNpifOKT4bZ5NrKSm2",
                "email": "c.beckett@dummy.com",
                "username": "lordbecks",
                "Profile": {
                    "firstname": "Cutler",
                    "lastname": "Beckett",
                    "img": "",
                    "user_description": "Top Boy",
                    "age": "45",
                    "gender": "m"
                },
                "Agenda": {
                    "history": [],
                    "going": []
                }

            },
            await self.mongo_db["users_collection"].find_one({"uuid": "PAOy3tOLQNTNpifOKT4bZ5NrKSm2"})
        )

    @tornado.testing.gen_test
    async def test_post_returns_400_if_document_with_given_uuid_exists_in_database(self):
        await self.mongo_db["users_collection"].insert_one({"uuid": "Sdjhjhj123"})

        response = await self.fetch("/api/users", method="POST", body=json.dumps(
            {"uuid": "Sdjhjhj123",
             "email": "c.beckett@dummy.com",
             "username": "lordbecks",
             "Profile": {
                 "firstname": "Cutler",
                 "lastname": "Beckett",
                 "img": "",
                 "user_description": "Top Boy",
                 "age": "45",
                 "gender": "m"
             },
             "Agenda": {
                 "history": [],
                 "going": []
             }}))

        self.assertEqual(400, response.code)

    @tornado.testing.gen_test
    async def test_post_returns_400_if_request_body_does_not_have_uuid(self):
        response = await self.fetch("/api/users", method="POST", body=json.dumps(
            {"uuid": "",
             "email": "c.beckett@dummy.com",
             "username": "lordbecks",
             "Profile": {
                 "firstname": "Cutler",
                 "lastname": "Beckett",
                 "img": "",
                 "user_description": "Top Boy",
                 "age": "45",
                 "gender": "m"
             },
             "Agenda": {
                 "history": [],
                 "going": []
             }}))

        self.assertEqual(400, response.code)

    @tornado.testing.gen_test
    async def test_patch_adds_request_body_to_Agenda_going_list(self):
        await self.mongo_db["users_collection"].insert_one(
            {"uuid": "Sdjhjhj123",
             "email": "c.beckett@dummy.com",
             "username": "lordbecks",
             "Profile": {
                 "firstname": "Cutler",
                 "lastname": "Beckett",
                 "img": "",
                 "user_description": "Top Boy",
                 "age": "45",
                 "gender": "m"
             },
             "Agenda": {
                 "history": [],
                 "going": []
             }})

        response = await self.fetch("/api/users/Sdjhjhj123", method="PATCH", body=json.dumps(
            {
                "id": "61c34247dcf1be30d9aba564a005e77749d1dbaf",
                "date": "2019-12-24",
                "chatKey": "61c34247dcf1be30d9aba564a005e77749d1dbaf2019-12-24",
                "name": "London"
            }
        ))

        self.assertEqual(200, response.code)

        self.assertEqual(
            {
                "_id": mock.ANY,
                "uuid": "Sdjhjhj123",
                "email": "c.beckett@dummy.com",
                "username": "lordbecks",
                "Profile": {
                    "firstname": "Cutler",
                    "lastname": "Beckett",
                    "img": "",
                    "user_description": "Top Boy",
                    "age": "45",
                    "gender": "m"
                },
                "Agenda": {
                    "history": [],
                    "going": [
                        {
                            "id": "61c34247dcf1be30d9aba564a005e77749d1dbaf",
                            "date": "2019-12-24",
                            "chatKey": "61c34247dcf1be30d9aba564a005e77749d1dbaf2019-12-24",
                            "name": "London"
                        }
                    ]
                }

            },
            await self.mongo_db["users_collection"].find_one({"uuid": "Sdjhjhj123"})
        )

    @tornado.testing.gen_test
    async def test_patch_returns_400_if_request_body_contains_id_already_in_Agenda_going_list(self):
        await self.mongo_db["users_collection"].insert_one(
            {"uuid": "Sdjhjhj123",
             "email": "c.beckett@dummy.com",
             "username": "lordbecks",
             "Profile": {
                 "firstname": "Cutler",
                 "lastname": "Beckett",
                 "img": "",
                 "user_description": "Top Boy",
                 "age": "45",
                 "gender": "m"
             },
             "Agenda": {
                 "history": [],
                 "going": [
                     {
                         "id": "61c34247dcf1be30d9aba564a005e77749d1dbaf",
                         "date": "2019-12-24",
                         "chatKey": "61c34247dcf1be30d9aba564a005e77749d1dbaf2019-12-24",
                         "name": "London"
                     }
                 ]
             }})

        response = await self.fetch("/api/users/Sdjhjhj123", method="PATCH", body=json.dumps(
            {
                "id": "61c34247dcf1be30d9aba564a005e77749d1dbaf",
                "date": "2019-12-24",
                "chatKey": "61c34247dcf1be30d9aba564a005e77749d1dbaf2019-12-24",
                "name": "London"
            }
        ))

        self.assertEqual(400, response.code)

        self.assertEqual(
            {
                "_id": mock.ANY,
                "uuid": "Sdjhjhj123",
                "email": "c.beckett@dummy.com",
                "username": "lordbecks",
                "Profile": {
                    "firstname": "Cutler",
                    "lastname": "Beckett",
                    "img": "",
                    "user_description": "Top Boy",
                    "age": "45",
                    "gender": "m"
                },
                "Agenda": {
                    "history": [],
                    "going": [
                        {
                            "id": "61c34247dcf1be30d9aba564a005e77749d1dbaf",
                            "date": "2019-12-24",
                            "chatKey": "61c34247dcf1be30d9aba564a005e77749d1dbaf2019-12-24",
                            "name": "London"
                        }
                    ]
                }

            },
            await self.mongo_db["users_collection"].find_one({"uuid": "Sdjhjhj123"})
        )

    @tornado.testing.gen_test
    async def test_delete_removes_item_with_matching_id_from_Agenda_going_list_and_returns_the_updated_user_object(self):
        await self.mongo_db["users_collection"].insert_one(
            {"uuid": "Sdjhjhj123",
             "email": "c.beckett@dummy.com",
             "username": "lordbecks",
             "Profile": {
                 "firstname": "Cutler",
                 "lastname": "Beckett",
                 "img": "",
                 "user_description": "Top Boy",
                 "age": "45",
                 "gender": "m"
             },
             "Agenda": {
                 "history": [],
                 "going": [
                     {
                         "id": "61c34247dcf1be30d9aba564a005e77749d1dbaf",
                         "date": "2019-12-24",
                         "chatKey": "61c34247dcf1be30d9aba564a005e77749d1dbaf2019-12-24",
                         "name": "London"
                     },
                     {
                         "id": "9cc5acae16ff76d52d7cb449494976935871df85",
                         "date": "2019-11-13",
                         "chatKey": "9cc5acae16ff76d52d7cb449494976935871df852019-11-13",
                         "name": "Royal Exchange Theatre"
                     }
                 ]
             }})

        response = await self.fetch("/api/users/Sdjhjhj123", method="DELETE", body=json.dumps(
            {
                "id": "61c34247dcf1be30d9aba564a005e77749d1dbaf"
            }
        ))

        self.assertEqual(200, response.code)

        self.assertEqual(
            {
                "_id": mock.ANY,
                "uuid": "Sdjhjhj123",
                "email": "c.beckett@dummy.com",
                "username": "lordbecks",
                "Profile": {
                    "firstname": "Cutler",
                    "lastname": "Beckett",
                    "img": "",
                    "user_description": "Top Boy",
                    "age": "45",
                    "gender": "m"
                },
                "Agenda": {
                    "history": [],
                    "going": [
                        {
                            "id": "9cc5acae16ff76d52d7cb449494976935871df85",
                            "date": "2019-11-13",
                            "chatKey": "9cc5acae16ff76d52d7cb449494976935871df852019-11-13",
                            "name": "Royal Exchange Theatre"
                        }
                    ]
                }

            },
            await self.mongo_db["users_collection"].find_one({"uuid": "Sdjhjhj123"})
        )

    @tornado.testing.gen_test
    async def test_delete_returns_404_if_request_body_has_no_id_value(self):
        await self.mongo_db["users_collection"].insert_many([
            {"uuid": "Sdjhjhj123",
             "email": "c.beckett@dummy.com",
             "username": "lordbecks",
             "Profile": {
                 "firstname": "Cutler",
                 "lastname": "Beckett",
                 "img": "",
                 "user_description": "Top Boy",
                 "age": "45",
                 "gender": "m"
             },
             "Agenda": {
                 "history": [],
                 "going": [
                     {
                         "id": "61c34247dcf1be30d9aba564a005e77749d1dbaf",
                         "date": "2019-12-24",
                         "chatKey": "61c34247dcf1be30d9aba564a005e77749d1dbaf2019-12-24",
                         "name": "London"
                     },
                     {
                         "id": "9cc5acae16ff76d52d7cb449494976935871df85",
                         "date": "2019-11-13",
                         "chatKey": "9cc5acae16ff76d52d7cb449494976935871df852019-11-13",
                         "name": "Royal Exchange Theatre"
                     }
                 ]
             }},
            {
                "uuid": "BGep2XwyqgYJ9fUwjZX7floy6s33",
                "email": "jgibbs@dummy.com",
                "username": "drunkensailor",
                "Profile": {
                    "firstname": "Joshamee",
                    "lastname": "Gibbs",
                    "img": "https://vignette.wikia.nocookie.net/disney/images/8/82/Gibbs_Headshot.jpg/revision/latest?cb=20151120173344",
                    "user_description": "Joshamee Gibbs was the longtime comrade and devoted First Mate of Captain Jack Sparrow. ... Once a sailor in His Majesty's Royal Navy, later an enthusiastic pirate, Joshamee Gibbs was a man who knew his way across every ocean, and into every pub. Gibbs was Jack Sparrow's most trusted ...",
                    "age": "47",
                    "gender": "m"
                },
                "Agenda": {
                    "history": [],
                    "going": [
                        {
                            "id": "cebbc87f03fecafe1bf3a0cb4a0e2d1f303ff7d2",
                            "date": "2019-12-27",
                            "chatKey": "cebbc87f03fecafe1bf3a0cb4a0e2d1f303ff7d22019-12-27"
                        }
                    ]
                }
            }])

        response = await self.fetch("/api/users/Sdjhjhj123", method="DELETE", body=json.dumps(
            {
                "id": "",
                "date": "2019-11-13",
                "chatKey": "9cc5acae16ff76d52d7cb449494976935871df852019-11-13",
                "name": "Royal Exchange Theatre"
            }
        ))

        self.assertEqual(400, response.code)

    @tornado.testing.gen_test
    async def test_get_locations_returns_number_of_users_going_to_given_location(self):
        await self.mongo_db["users_collection"].insert_many([
            {"uuid": "Sdjhjhj123",
             "email": "c.beckett@dummy.com",
             "username": "lordbecks",
             "Profile": {
                 "firstname": "Cutler",
                 "lastname": "Beckett",
                 "img": "",
                 "user_description": "Top Boy",
                 "age": "45",
                 "gender": "m"
             },
             "Agenda": {
                 "history": [],
                 "going": [
                     {
                         "id": "61c34247dcf1be30d9aba564a005e77749d1dbaf",
                         "date": "2019-12-24",
                         "chatKey": "61c34247dcf1be30d9aba564a005e77749d1dbaf2019-12-24",
                         "name": "London"
                     },
                     {
                         "id": "9cc5acae16ff76d52d7cb449494976935871df85",
                         "date": "2019-11-13",
                         "chatKey": "9cc5acae16ff76d52d7cb449494976935871df852019-11-13",
                         "name": "Royal Exchange Theatre"
                     }
                 ]
             }},
            {
                "uuid": "BGep2XwyqgYJ9fUwjZX7floy6s33",
                "email": "jgibbs@dummy.com",
                "username": "drunkensailor",
                "Profile": {
                    "firstname": "Joshamee",
                    "lastname": "Gibbs",
                    "img": "https://vignette.wikia.nocookie.net/disney/images/8/82/Gibbs_Headshot.jpg/revision/latest?cb=20151120173344",
                    "user_description": "Joshamee Gibbs was the longtime comrade and devoted First Mate of Captain Jack Sparrow. ... Once a sailor in His Majesty's Royal Navy, later an enthusiastic pirate, Joshamee Gibbs was a man who knew his way across every ocean, and into every pub. Gibbs was Jack Sparrow's most trusted ...",
                    "age": "47",
                    "gender": "m"
                },
                "Agenda": {
                    "history": [],
                    "going": [
                        {
                            "id": "9cc5acae16ff76d52d7cb449494976935871df85",
                            "date": "2019-11-13",
                            "chatKey": "9cc5acae16ff76d52d7cb449494976935871df852019-11-13",
                            "name": "Royal Exchange Theatre"
                        },
                        {
                            "id": "cebbc87f03fecafe1bf3a0cb4a0e2d1f303ff7d2",
                            "date": "2019-12-27",
                            "chatKey": "cebbc87f03fecafe1bf3a0cb4a0e2d1f303ff7d22019-12-27"
                        }
                    ]
                }
            }])

        response = await self.fetch("/api/locations/9cc5acae16ff76d52d7cb449494976935871df85")

        self.assertEqual(200, response.code)

        self.assertEqual(b'2', response.body)


if __name__ == '__main__':
    unittest.main()
