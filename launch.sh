#!/bin/bash

cd $(dirname "$0")
source ./.secret-env
/opt/groundlight/gl-py/bin/python ./app.py

