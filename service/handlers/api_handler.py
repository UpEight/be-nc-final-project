import json

import tornado.web


class ApiHandler(tornado.web.RequestHandler):
    async def get(self):
        endpoints_json = {
            "GET /api": {
                "description": "serves up a json representation of all the available endpoints of the api"
            },
            "POST /api/users": {
                "description": "adds the user object sent on the request body as a new user record",
                "queries": [],
                "exampleRequestBody": {
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
                                "date": "2219-12-24",
                                "chatKey": "61c34247dcf1be30d9aba564a005e77749d1dbaf2019-12-24",
                                "name": "Bridgewater Hall"
                            },
                            {
                                "id": "9cc5acae16ff76d52d7cb449494976935871df85",
                                "date": "2219-11-13",
                                "chatKey": "9cc5acae16ff76d52d7cb449494976935871df852019-11-13",
                                "name": "Royal Exchange Theatre"
                            }
                        ]
                    }
                },
                "exampleResponse": {
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
                                "date": "2219-12-24",
                                "chatKey": "61c34247dcf1be30d9aba564a005e77749d1dbaf2019-12-24",
                                "name": "Bridgewater Hall"
                            },
                            {
                                "id": "9cc5acae16ff76d52d7cb449494976935871df85",
                                "date": "2219-11-13",
                                "chatKey": "9cc5acae16ff76d52d7cb449494976935871df852019-11-13",
                                "name": "Royal Exchange Theatre"
                            }
                        ]
                    }
                }
            },
            "GET /api/users/:uuid": {
                "description": "serves an object containing the user information for the requested uuid",
                "queries": [],
                "exampleResponse": {
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
                                "date": "2219-12-24",
                                "chatKey": "61c34247dcf1be30d9aba564a005e77749d1dbaf2019-12-24",
                                "name": "Bridgewater Hall"
                            },
                            {
                                "id": "9cc5acae16ff76d52d7cb449494976935871df85",
                                "date": "2219-11-13",
                                "chatKey": "9cc5acae16ff76d52d7cb449494976935871df852019-11-13",
                                "name": "Royal Exchange Theatre"
                            }
                        ]
                    }
                }
            },
            "PATCH /api/users/:uuid": {
                "description": "adds the object sent on the request body to the Agenda.going list",
                "queries": [],
                "exampleRequestBody": {
                    "id": "779c0d02a3081a20b6a847fc2966989cf576a00b",
                    "date": "2019-12-20",
                    "chatKey": "779c0d02a3081a20b6a847fc2966989cf576a00b2019-12-20",
                    "name": "Grace Cathedral"
                },
                "exampleResponse": {
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
                                "date": "2219-12-24",
                                "chatKey": "61c34247dcf1be30d9aba564a005e77749d1dbaf2019-12-24",
                                "name": "Bridgewater Hall"
                            },
                            {
                                "id": "9cc5acae16ff76d52d7cb449494976935871df85",
                                "date": "2219-11-13",
                                "chatKey": "9cc5acae16ff76d52d7cb449494976935871df852019-11-13",
                                "name": "Royal Exchange Theatre"
                            },
                            {
                                "id": "779c0d02a3081a20b6a847fc2966989cf576a00b",
                                "date": "2019-12-20",
                                "chatKey": "779c0d02a3081a20b6a847fc2966989cf576a00b2019-12-20",
                                "name": "Grace Cathedral"
                            }
                        ]
                    }
                }
            },
            "DELETE /api/users/:uuid": {
                "description": "removes the object sent on the request body from the Agenda.going list",
                "queries": [],
                "exampleRequestBody": {
                    "id": "779c0d02a3081a20b6a847fc2966989cf576a00b"
                },
                "exampleResponse": {
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
                                "date": "2219-12-24",
                                "chatKey": "61c34247dcf1be30d9aba564a005e77749d1dbaf2019-12-24",
                                "name": "Bridgewater Hall"
                            },
                            {
                                "id": "9cc5acae16ff76d52d7cb449494976935871df85",
                                "date": "2219-11-13",
                                "chatKey": "9cc5acae16ff76d52d7cb449494976935871df852019-11-13",
                                "name": "Royal Exchange Theatre"
                            }
                        ]
                    }
                }
            },
            "GET /api/locations/:location_id": {
                "decription": "serves up the number of users going to the requested location_id",
                "queries": [],
                "exampleResponse": "2"
            }
        }

        self.set_status(200)
        self.finish(json.dumps(endpoints_json))
