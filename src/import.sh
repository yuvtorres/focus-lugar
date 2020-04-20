#!/bin/bash
#
# Script for import the json package in MongoDB

mongoimport --db companies --collection design --jsonArray design.json

mongoimport --db companies --collection old --jsonArray old.json

mongoimport --db companies --collection success --jsonArray success.json

