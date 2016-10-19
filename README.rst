====================
Django Pycql
====================

This is a demo Django application using Cassandra (non-relational) database. It includes a custom database backend to abstract the model layer.

=====================
Requirements
=====================
This application requires Python 2.7 or later, libev, pyev, Django 1.5
and DataStax Python Driver version 1.0.0 for Apache Cassandra.

You can download the Python Driver from <https://github.com/datastax/python-driver/releases/tag/1.0.0>



=====================
Quick start
=====================

1. Run `python manage.py sync_cass` to create node's models.

2. Access http://127.0.0.1:8000/node/index to view a list of most recent posts.
