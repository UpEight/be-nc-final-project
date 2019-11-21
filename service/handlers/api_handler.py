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
                "description": "Adds item to or removes item from Agenda.going list depending on request body format. To add an item, request body must contain keys 'id' and 'date' as a minimum. To remove an item, request body must contain key 'id' only",
                "queries": [],
                "exampleRequestBodyAddItem": {
                    "id": "779c0d02a3081a20b6a847fc2966989cf576a00b",
                    "date": "2019-12-20",
                    "chatKey": "779c0d02a3081a20b6a847fc2966989cf576a00b2019-12-20",
                    "name": "Grace Cathedral"
                },
                "exampleResponseAddItem": {
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
                },
                "exampleRequestBodyRemoveItem": {
                    "id": "779c0d02a3081a20b6a847fc2966989cf576a00b"
                },
                "exampleResponseRemoveItem": {
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
            },
            "PATCH /api/personality/:uuid": {
                "description": "sets the user 'personality' attribute to the object sent on the request body",
                "queries": [],
                "exampleRequestBody": {
                    "word_count": 1375,
                    "processed_language": "en",
                    "personality": [
                        {
                            "trait_id": "big5_openness",
                            "name": "Openness",
                            "category": "personality",
                            "percentile": 0.843172828824265,
                            "significant": "true",
                            "children": [
                                {
                                    "trait_id": "facet_adventurousness",
                                    "name": "Adventurousness",
                                    "category": "personality",
                                    "percentile": 0.7437159899414063,
                                    "significant": "true"
                                }
                            ]
                        }
                    ]
                },
                "exampleResponse": {
                    "Agenda": {
                        "going": [
                            {
                                "id": "dba505d1dbaf",
                                "date": "2019-12-24",
                                "chatKey": "61c34247dcf1be30d9aba564a005e77749d1dbaf2019-12-24",
                                "name": "Lon"
                            },
                            {
                                "id": "dbaf7rwewrwr878",
                                "date": "2019-11-21",
                                "chatKey": "61c34247dcf1be30d9aba564a005e77749d1dbaf2019-12-24",
                                "name": "Lon"
                            }
                        ],
                        "history": []
                    },
                    "Profile": {
                        "age": "",
                        "firstname": "Test",
                        "gender": "",
                        "img": "",
                        "lastname": "Signup3",
                        "user_description": ""
                    },
                    "email": "test119@live.com",
                    "username": "Test119",
                    "uuid": "BAqzaYsDymMKemORNPTaG9Zli2D3",
                    "personality": {
                        "word_count": 1375,
                        "processed_language": "en",
                        "personality": [
                            {
                                "trait_id": "big5_openness",
                                "name": "Openness",
                                "category": "personality",
                                "percentile": 0.843172828824265,
                                "significant": "true",
                                "children": [
                                    {
                                        "trait_id": "facet_adventurousness",
                                        "name": "Adventurousness",
                                        "category": "personality",
                                        "percentile": 0.7437159899414063,
                                        "significant": "true"
                                    }
                                ]
                            }
                        ]
                    }
                }
            }
        }

        self.set_status(200)
        self.finish(json.dumps(endpoints_json))
