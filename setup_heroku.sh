#!/bin/bash
# Set up vars in heroku
heroku config:set AUTH_API_AUDIENCE='wow-auctions' AUTH_ALGORITHM='RS256' AUTH_CLIENT_ID='jG9MI6jJBWXMzaLsPabzLluOwUlhMQEn' AUTH_DOMAIN='fail2reap-prod.eu.auth0.com' FLASK_APP=run.py FLASK_SECRET_KEY='prod_1jrwmi(4)5l-2$(p4)_lb*4tq4#51fbd@+6f5mak7g6-fx#25b' FLASK_DATABASE_URL='postgresql://qkaripyzgbnihb:26fb621d97ef3401b1e1005cb997da1ac335161044517608d16205d439000f4f@ec2-54-220-170-192.eu-west-1.compute.amazonaws.com:5432/df5u05mlkjalsf';
heroku run flask db upgrade -d backend/database/migrations;