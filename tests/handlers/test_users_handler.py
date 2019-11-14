import json
import os
import unittest
from unittest import mock

import motor.motor_tornado
import tornado.testing

from run_service import make_app
from tests.handlers.handler_test_case import HandlerTestCase


class TestUsersHandler(HandlerTestCase):
    # def tearDown(self):
    #     self.io_loop.run_sync(
    #         lambda: self.motor_client.drop_database(self.mongo_db))

    #     super().tearDown()

    def get_app(self):
        self.motor_client = motor.motor_tornado.MotorClient(
            os.environ["MONGODB_URI"])
        self.mongo_db = self.motor_client["novado_test"]

        return make_app({
            "motor_client": self.motor_client,
            "mongo_db": self.mongo_db
        })

    @tornado.testing.gen_test
    async def test_get_returns_404_when_document_does_not_exist_in_database(self):
        response = await self.fetch("/api/users/missing")

        self.assertEqual(404, response.code)

    @tornado.testing.gen_test
    async def test_get_returns_200_when_Bob_does_exist_in_database(self):
        response = await self.fetch("/api/users/Bob")

        self.assertEqual(200, response.code)


if __name__ == '__main__':
    unittest.main()
