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
    "description": "The URL or resource was not found."
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

> <span style="color:darkseagreen">**GET**</span> /auction/\<id>

Gets a specific auction by id.

- Request Parameters

  - id (int): Id of the auction.

- Example Request

  ```bash
  curl --request GET 'https://powerful-harbor-60014.herokuapp.com/auction/1999415'
  ```

- Example Response

  ```json
  {
    "auction": {
      "bid": 0,
      "buyout": 289119,
      "id": 1999415,
      "item_id": 186364,
      "quantity": 1,
      "time_left": "VERY_LONG",
      "timestamp": "Sun, 18 Jul 2021 22:11:33 GMT",
      "unit_price": 0
    },
    "success": true
  }
  ```

<br>

> <span style="color:darkseagreen">**GET**</span> /auctions

Gets a list of all auctions.

- Example Request

  ```bash
  curl --request GET 'https://powerful-harbor-60014.herokuapp.com/auctions'
  ```

- Example Response

  ```json
  {
    "auctions": [
      {
        "bid": 0,
        "buyout": 198494,
        "id": 1944580,
        "item_id": 186373,
        "quantity": 1,
        "time_left": "SHORT",
        "timestamp": "Sun, 18 Jul 2021 22:11:33 GMT",
        "unit_price": 0
      },
      {
        "bid": 0,
        "buyout": 1989134,
        "id": 1964817,
        "item_id": 186373,
        "quantity": 1,
        "time_left": "SHORT",
        "timestamp": "Sun, 18 Jul 2021 22:11:33 GMT",
        "unit_price": 0
      },
      {
        "bid": 0,
        "buyout": 19894514,
        "id": 1968541,
        "item_id": 186358,
        "quantity": 1,
        "time_left": "SHORT",
        "timestamp": "Sun, 18 Jul 2021 22:11:33 GMT",
        "unit_price": 0
      },
      {
        "bid": 0,
        "buyout": 0,
        "id": 1960044,
        "item_id": 173204,
        "quantity": 589,
        "time_left": "VERY_LONG",
        "timestamp": "Sun, 18 Jul 2021 22:11:33 GMT",
        "unit_price": 3311
      },
      {
        "bid": 0,
        "buyout": 0,
        "id": 1951355,
        "item_id": 172097,
        "quantity": 32,
        "time_left": "LONG",
        "timestamp": "Sun, 18 Jul 2021 22:11:33 GMT",
        "unit_price": 39321
      }
    ],
    "success": true
  }
  ```

<br>

> <span style="color:gold">**POST**</span> /auctions

Creates a new auction.

- Request Body

  - id (int): Id of the auction.
  - timestamp (datetime): Datetime of when the auction was last refreshed.
  - bid (int): Bid on the auction in copper.
  - buyout (int): Buyout on the auction in copper.
  - unit_price (int): Unit Price on the auction in copper.
  - quantity (int): Number of items in this auction.
  - time_left (str): Time left for the auction.
  - item_id (int): Id of the item being auctioned.

- Example Request

  ```bash
  curl --request POST 'https://powerful-harbor-60014.herokuapp.com/auctions' \
       --header "Content-Type: application/json" \
       --data '{ "id": 123144511, "timestamp": "2021-07-18 22:11:33.433027", "bid": 0, "buyout": 123144, "unit_price": 0, "quantity": 23, "time_left": "SHORT", "item_id": 186358 }'
  ```

- Example Response
  ```json
  {
    "success": true,
    "created": 123551
  }
  ```

<br>

> <span style="color:#2E8BC0">**PATCH**</span> /auction/\<id>

Updates an auction with a given id.

- Request Body

  - name (type): Description

- Example Request

  ```bash
  curl --request PATCH 'https://powerful-harbor-60014.herokuapp.com/auction/123551' \
       --header "Content-Type: application/json" \
       --data '{"timestamp": "2021-07-18 22:11:33.433027", "quantity": 2, "time_left": "SHORT"}'
  ```

- Example Response
  ```json
  {
    "success": true,
    "updated": 123551
  }
  ```

<br>

> <span style="color:lightcoral">**DELETE**</span> /auction/\<id>

Deletes an auction with a given id.

- Request Parameters
  - id (int): Id of the auction.

* Example Request

  ```bash
  curl --request DELETE 'https://powerful-harbor-60014.herokuapp.com/auction/123551'
  ```

* Example Response
  ```json
  {
    "success": true,
    "deleted": 123551
  }
  ```
  <br>

#### **Items**

> <span style="color:darkseagreen">**GET**</span> /item/\<id>

Gets a specific item by id.

- Request Parameters

  - id (int): Id of the item.

- Example Request

  ```bash
  curl --request GET 'https://powerful-harbor-60014.herokuapp.com/item/173204'
  ```

- Example Response

  ```json
  {
    "item": {
      "id": 173204,
      "name": "Lightless Silk"
    },
    "success": true
  }
  ```

<br>

> <span style="color:darkseagreen">**GET**</span> /items

Gets a list of all items.

- Example Request

  ```bash
  curl --request GET 'https://powerful-harbor-60014.herokuapp.com/items'
  ```

- Example Response

  ```json
  {
    "items": [
      {
        "id": 186359,
        "name": "Scoundrel's Harrowed Leggings"
      },
      {
        "id": 186362,
        "name": "Bindings of the Subjugated"
      },
      {
        "id": 184807,
        "name": "Relic of the First Ones"
      },
      {
        "id": 186358,
        "name": "Soulcaster's Woven Grips"
      },
      {
        "id": 186364,
        "name": "Cord of Coerced Spirits"
      }
    ],
    "success": true
  }
  ```

<br>

> <span style="color:gold">**POST**</span> /items

Creates a new item with a given id and name.

- Request Body

  - id (int): Id of the item.
  - name (str): Name of the item.

- Example Request

  ```bash
  curl --request PATCH 'https://powerful-harbor-60014.herokuapp.com/items' \
       --header "Content-Type: application/json" \
       --data '{"id": 0225,"name": "Sword of a Thousand Truths"}'
  ```

- Example Response
  ```json
  {
    "success": true,
    "created": 123551
  }
  ```

<br>

> <span style="color:#2E8BC0">**PATCH**</span> /item/\<id>

Updates an item with a given id.

- Request Body

  - id (int): Item id to update.

- Example Request

  ```bash
  curl --request PATCH 'https://powerful-harbor-60014.herokuapp.com/item/123551' \
       --header "Content-Type: application/json" \
       --data '{"name": "My Super Cool Cloak"}'
  ```

- Example Response
  ```json
  {
    "success": true,
    "updated": 123551
  }
  ```

<br>

> <span style="color:lightcoral">**DELETE**</span> /item/\<id>

Deletes an item with a given id.

- Request Parameters

  - id (int): Item id to delete.

* Example Request

  ```bash
  curl --request DELETE 'https://powerful-harbor-60014.herokuapp.com/item/123551'
  ```

* Example Response
  ```json
  {
    "success": true,
    "deleted": 123551
  }
  ```
  <br>
