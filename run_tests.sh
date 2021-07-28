#!/bin/bash
# Set up vars
export SIGNING_PRIV_KEY=$(openssl genrsa 4096 2>/dev/null | sed 's/\n//g');
export SIGNING_PUB_KEY=$(echo "$SIGNING_PRIV_KEY" | openssl rsa -in /dev/stdin -pubout 2>/dev/null);
export FLASK_APP=run.py;
export FLASK_ENV='development';
export FLASK_TESTING=True;
export FLASK_DEBUG=True;
export FLASK_SECRET_KEY='testing_1jrwmi(4)5l-2$(p4)_lb*4tq4#51fbd@+6f5mak7g6-fx#25b';
export FLASK_DATABASE_URL='postgresql://qkaripyzgbnihb:26fb621d97ef3401b1e1005cb997da1ac335161044517608d16205d439000f4f@ec2-54-220-170-192.eu-west-1.compute.amazonaws.com:5432/df5u05mlkjalsf';
export AUTH_DOMAIN='fail2reap-prod.eu.auth0.com';
export AUTH_CLIENT_ID='jG9MI6jJBWXMzaLsPabzLluOwUlhMQEn';
export AUTH_ALGORITHM='RS256';
export AUTH_API_AUDIENCE='wow-auctions';

# Run tests
python3 -m unittest;

# Cleanup
unset SIGNING_PRIV_KEY
unset SIGNING_PUB_KEY
unset FLASK_APP
unset FLASK_ENV
unset FLASK_TESTING
unset FLASK_DEBUG
unset FLASK_SECRET_KEY
unset FLASK_DATABASE_URL
unset AUTH_DOMAIN
unset AUTH_ALGORITHM
unset AUTH_API_AUDIENCE