# WANDR API

A RESTful API for storing and updating user information for the WANDR mobile app. The user data is stored in single document format in a MongoDB database.

The available endpoints are shown [here](https://be-nc-final-project-nomado.herokuapp.com/api)

## Getting started

### Prerequisites

- Requires Python >= 3.7.4

- Requires a local running instance of MongoDB

### Local installation

1. Clone the repository:

```bash
git clone https://github.com/UpEight/be-nc-final-project
cd be-nc-final-project
```

2. Create a virtual environment:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

3. Install the dependencies:

```bash
pip install -r requirements.txt
```

4. Run the web server:

```bash
python3 -m run_service
```

### Running the tests

Run the following to run the unit tests:

```bash
python3 -m tests.handlers.test_users_handler
```

## Built With

- [Tornado](https://www.tornadoweb.org/en/stable/index.html) - Python web framework and asynchronous networking library

- [MongoDB](https://www.mongodb.com/) - NoSQL database

- [Motor](https://motor.readthedocs.io/en/stable/index.html) - Asynchronous Python driver for MongoDB

## Hosted With

- [MongoDB Atlas](https://cloud.mongodb.com)

- [Heroku](https://devcenter.heroku.com/)
