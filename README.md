# World of Warcraft Auctions API

## Table of Contents

- [Project Overview](#project-overview)
  - [Directory Structure](#directory-structure)
- [Getting Started](#getting-started)
  - [Overview of Key Dependencies](#overview-of-key-dependencies)
  - [Installing Dependencies](#installing-dependencies)
  - [Configuring Environment Variables](#configuring-environment-variables)
  - [Running the Backend Server](#running-the-backend-server)
- [Testing](#testing)
  - [Local](#local)
  - [Remote](#remote)
- [RBAC](#rbac)
  - [Roles](#roles)
- [API Reference](#api-reference)
  - [Getting Started](#getting-started)
  - [Error Handling](#error-handling)
  - [Endpoints](#endpoints)

## Project Overview

I created this API as a base for some personal projects that require historical auction data. Currently the API provided by Blizzard does not include historical data but rather just a snapshot of auction data at a particular point in time with no history.

Because of this, I decided to create my own API. The next step would be building a data service that polls Blizzard's API and then ingests any new data into the database for further consumption.

### Directory Structure

```
.
├── Procfile
├── README.md
├── awdaada.txt
├── requirements.txt
├── run.py
├── run_tests.sh
├── runtime.txt
├── setup.sh
├── backend
│   ├── __init__.py
│   ├── blueprints
│   │   ├── __init__.py
│   │   ├── auctions.py
│   │   ├── auth.py
│   │   ├── home.py
│   │   └── items.py
│   ├── config
│   │   ├── production.py
│   │   └── testing.py
│   ├── database
│   │   ├── __init__.py
│   │   ├── migrations
│   │   │   ├── README
│   │   │   ├── alembic.ini
│   │   │   ├── env.py
│   │   │   ├── script.py.mako
│   │   │   └── versions
│   │   │       └── 8a3a4eba6d09_initial_migration.py
│   │   └── models
│   │       ├── __init__.py
│   │       ├── auction.py
│   │       └── item.py
│   ├── services
│   │   └── auth
│   │       ├── __init__.py
│   │       └── auth.py
│   └── static
│       └── favicon.ico
└── test
    ├── __init__.py
    ├── test_routes.py
    ├── data
    │   ├── auctions.json
    │   └── items.json
    ├── utils
    │   ├── __init__.py
    │   └── auth.py
    └── udacity-fsnd-capstone.postman_collection.json
```

## Getting Started

### Overview of Key Dependencies

Here we have a quick overview of the key dependencies used in the creation of this web app project.

- [Python](https://www.python.org/) is a programming language that lets you work quickly and integrate systems more effectively.

- [Flask](https://flask.palletsprojects.com/en/2.0.x/) is a lightweight backend microservices framework for Python. Flask is required to handle requests and responses.

- [Flask-Migrate](https://flask-migrate.readthedocs.io/en/latest/) is an extension that handles SQLAlchemy database migrations for Flask applications using Alembic.

- [python-jose](https://python-jose.readthedocs.io/en/latest/) a JOSE implementation in Python

- [gunicorn](https://gunicorn.org/) 'Green Unicorn' is a Python WSGI HTTP Server for UNIX.

### Installing Dependencies

Before we can run our Flask app, we need to ensure our environment is set up correctly.

1. **Python 3.9**<br>
   Follow instructions to install the latest version of python for your platform in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python).

2. **Virtual Environment**<br>
   It's recommended to work within a virtual environment whenever using Python for projects. This keeps your dependencies for each project separate and organaized. Instructions for setting up a virual enviornment for your platform can be found in the [python docs](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/). [Conda](https://docs.conda.io/en/latest/) is another great alternative for managing virtual environments.

3. **Project Dependencies**<br>
   Once you have your virtual environment setup and running, install the required ependencies by naviging to the project root directory and running:
   ```bash
   pip install -r requirements.txt;
   ```
   This will install all of the required packages within the [requirements.txt](requirements.txt) file including our key dependencies.

### Configuring Environment Variables

Once dependencies have been installed, we need to configure environment variables for our Flask app.

This can be done by running the `setup_local.sh` file:

```bash
bash setup_local.sh;
```

### Running the backend server

To run the server, navigate to the root directory and run:

```bash
flask run;
```

The API will be available under [http://localhost:5000](http://localhost:5000) by default.

> _note:_ Ensure the virtual environment you created earlier is currently active or dependency errors may occur.

## Testing

### Local

To run the unittests locally, simply run the [run_tests.sh](run_tests.sh) file using the command below:

```bash
bash run_tests.sh;
```

> _note:_ This is a self-contained file and includes all setup and execution variables and data so no additional steps are required.

### Remote

Testing the API remotely can be done using [Postman](https://www.postman.com/). Once the app is installed, simply import the [udacity-fsnd-capstone.postman_collection.json](./test/udacity-fsnd-capstone.postman_collection.json) collection.

Here you will be presented with 4 sub-folders; `Public`, `Free`, `Premium` and `Admin` users. These have their relevant tokens already pre-populated and can be used to run queries against the API immediately.

## RBAC

### Free (free_user(at)email(dot)com)

Can get specific items or auctions

- `get:item` Allows for creation of a new item.
- `get:auction` Allows viewing of a specific auction.

### Premium (premium_user(at)email(dot)com)

Can get specific items or auctions, and all items or auctions

- `get:item` Allows for creation of a new item.
- `get:items` Allows viewing of all items.
- `get:auction` Allows viewing of a specific auction.
- `get:auctions` Allows viewing of all auctions.

### Admin (admin_user(at)email(dot)com)

Can get specific items or auctions, all items or auctions, and create, update and delete items or auctions

- `get:item` Allows for creation of a new item.
- `get:items` Allows viewing of all items.
- `post:items` Allows for creation of a new item.
- `patch:item` Allows for patching of an existing specific item.
- `delete:item` Allows for deletion of a specific item.
- `get:auction` Allows viewing of a specific auction.
- `get:auctions` Allows viewing of all auctions.
- `post:auctions` Allows for creation of a new auction.
- `patch:auction` Allows for patching of an existing specific auction.
- `delete:auction` Allows for deletion of a specific auction.

<details>
  <summary>Click me for secrets!</summary>
  ThisIsATestAccount!
</details></br>

### Getting New Tokens
In the event the tokens provided in the Postman collection expire, click [refresh tokens](https://fail2reap-prod.eu.auth0.com/authorize?audience=wow-auctions&response_type=token&client_id=jG9MI6jJBWXMzaLsPabzLluOwUlhMQEn&redirect_uri=https://powerful-harbor-60014.herokuapp.com/) and sign in using one of the email accounts above.

You may need to [logout](https://fail2reap-prod.eu.auth0.com/v2/logout?returnTo=https://powerful-harbor-60014.herokuapp.com/&client_id=jG9MI6jJBWXMzaLsPabzLluOwUlhMQEn) before a new token can be issued for a different user.

## API Reference

### Getting Started

- All responses and request bodies from and to this API are using `JSON`.
- The API base URI is https://powerful-harbor-60014.herokuapp.com/

### Error Handling

Errors are returned as JSON objects in the following format:

```json
{
  "success": false,
  "error": 404,
  "message": {
    "code": "not_found",
    "description": "The URL or resource was not found.",
  }
}
```

The following error codes are returned by this API:

- **400**: Bad Request - If the request body could not be parsed.
- **401**: Unauthorized - If the user is not authenticated.
- **403**: Forbidden - If the user is not allowed to access the resource.
- **404**: Not Found - If the requested resource could not be found.
- **422**: Unprocessable - If the request body could be parsed, but its contents are semantically incorrect.

### Endpoints

#### **Auctions**



#### **Items**

> <span style="color:darkseagreen">**GET**</span> /item/<item_id>

Description

- Request Parameters
  - name (type): Description

- Example Request
  ```bash
  curl --request GET ''
  ```

- Example Response
  ```json

  ```

<br>

> <span style="color:darkseagreen">**GET**</span> /items

Description

- Request Parameters
  - name (type): Description

- Example Request
  ```bash
  curl --request GET ''
  ```

- Example Response
  ```json

  ```

<br>


> <span style="color:gold">**POST**</span> /items

Description

- Request Body
  - name (type): Description

- Example Request
  ```bash
  curl --request POST '' \
       --header "Content-Type: application/json" \
       --data '{}'
  ```

- Example Response
  ```json
  {
    "success": true,
    "created": 123551
  }
  ```

<br>


> <span style="color:#2E8BC0">**PATCH**</span> /

Description

- Request Body
  - name (type): Description

- Example Request
  ```bash
  curl --request PATCH '' \
       --header "Content-Type: application/json" \
       --data '{}'
  ```

- Example Response
  ```json
  {
    "success": true,
    "updated": 123551
  }
  ```

<br>


><span style="color:lightcoral">**DELETE**</span> /

Description

- Request Parameters
  - name (type): Description

* Example Request
    ```bash
    curl --request DELETE ''
    ```

* Example Response
  ```json
  {
    "success": true,
    "deleted": 123551
  }
  ```
<br>


