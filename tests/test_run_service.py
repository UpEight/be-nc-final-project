from unittest import mock

import tornado.testing

import run_service
from tests.helpers import future_returning


class TestRunService(tornado.testing.AsyncTestCase):
    @mock.patch("tornado.ioloop.IOLoop")
    @mock.patch("functools.partial", autospec=True)
    @mock.patch("tornado.platform.asyncio.AsyncIOMainLoop", autospec=True)
    @mock.patch("tornado.httpserver.HTTPServer", autospec=True)
    @mock.patch("tornado.web.Application", autospec=True)
    @mock.patch("motor.motor_tornado.MotorClient", autospec=True)
    def test_main_starts_service(
            self, mock_motorclient_class, mock_application_class, mock_httpserver_class,
            mock_asynciomainloop_class, mock_partial, mock_ioloop_class):

        mock_motorclient = mock_motorclient_class.return_value
        mock_mongo_db = mock_motorclient.get_default_database.return_value
        mock_httpserver = mock_httpserver_class.return_value
        mock_asynciomainloop = mock_asynciomainloop_class.return_value
        mock_ioloop = mock_ioloop_class.current.return_value

        environ = {
            "SERVER_PORT": "8000",
            "MONGODB_URI": "mongodb-uri"
        }

        run_service.main(environ)

        mock_asynciomainloop_class.assert_called_once_with()
        mock_asynciomainloop.install.assert_called_once_with()
        mock_ioloop_class.current.assert_called_once_with()

        mock_motorclient_class.assert_called_once_with("mongodb-uri")

        mock_application_class.assert_called_once_with(
            mock.ANY,
            motor_client=mock_motorclient,
            mongo_db=mock_mongo_db)

        mock_httpserver_class.assert_called_once_with(
            mock_application_class.return_value)
        mock_httpserver.listen.assert_called_once_with(8000, "localhost")

        mock_ioloop.start.assert_called_once_with()
