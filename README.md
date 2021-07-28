<<<<<<< HEAD
flask db init -d ./app/database/migrations/
flask db migrate -m "" -d ./app/database/migrations
flask db upgrade -d ./app/database/migrations

bash run_tests.sh

psql -h ec2-176-34-222-188.eu-west-1.compute.amazonaws.com -d dv61lv29ehfah -U kwvmjdjhhglxff -W
psql -h ec2-176-34-222-188.eu-west-1.compute.amazonaws.com -d dv61lv29ehfah -U kwvmjdjhhglxff -W -f .tmp/populate_db.sql
91769f00c2e3bb290039f6d82db68653b0f6b02981355dbcfbd2ffbf9becb65f

Motivation for project
Project dependencies, local development and hosting instructions,
Detailed instructions for scripts to install any project dependencies, and to run the development server.
Documentation of API behavior and RBAC controls

# Roles

## Free - Can get specific items or auctions

get:item Allows for creation of a new item.
get:auction Allows viewing of a specific auction.

## Premium - Can get specific items or auctions, and all items or auctions

get:item Allows for creation of a new item.
get:items Allows viewing of all items.
get:auction Allows viewing of a specific auction.
get:auctions Allows viewing of all auctions.

## Admin - Can get specific items or auctions, all items or auctions, and create, update and delete items or auctions

get:item Allows for creation of a new item.
get:items Allows viewing of all items.
post:item Allows for creation of a new item.
patch:item Allows for patching of an existing specific item.
delete:item Allows for deletion of a specific item.

get:auction Allows viewing of a specific auction.
get:auctions Allows viewing of all auctions.
post:auction Allows for creation of a new auction.
patch:auction Allows for patching of an existing specific auction.
delete:auction Allows for deletion of a specific auction.

# Accounts

free_user@email.com
premium_user@email.com
admin_user@email.com
ThisIsATestAccount!

https://fail2reap-prod.eu.auth0.com/authorize?
audience=wow-auctions
&response_type=token
&client_id=jG9MI6jJBWXMzaLsPabzLluOwUlhMQEn
&redirect_uri=http://127.0.0.1:5000

https://fail2reap-prod.eu.auth0.com/v2/logout?
returnTo=http://127.0.0.1:5000
&client_id=jG9MI6jJBWXMzaLsPabzLluOwUlhMQEn

get access tokens for 3 accounts using the above flow

# TODO

- create tests
- add comments everywhere
- remove unnecessary commented code/imports
- ensure all secrets are stored as environment variables
- re-export requirements both conda and pip
- update shell files setup.sh/run_tests.sh
  - Auth0 is set up and running at the time of submission. All required configuration settings are included in a bash file which export:
    - The Auth0 Domain Name
    - The JWT code signing secret
    - The Auth0 Client ID
- write documentation

  - Motivation for project
  - Project dependencies, local development and hosting instructions
    - project tree
    - URL is provided in project README
  - Detailed instructions for scripts to install any project dependencies, and to run the development server.
    - local testing (unittests)
    - production testing (postman)
  - Documentation of API behavior and RBAC controls
    - Description of roles and their permissions
    - APIs and their requiremed permissions
    - Instructions are provided in README for setting up authentication so reviewers can test endpoints at live application endpoint

- update hostname in collection, export and commit with project
- deploy on heroku
- renew tokens
- # run tests and ensure they run

# udacity-fsnd-capstone

> > > > > > > 93155ece4c0432ed6f4eb94116670e3a008c0461
