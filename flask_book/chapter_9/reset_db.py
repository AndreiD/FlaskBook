#!/usr/bin/python
# -*- coding: utf-8 -*-

import subprocess
proc = subprocess.Popen(["rm -rf db.sqlite migrations/"], stdout=subprocess.PIPE, shell=True)
(out, err) = proc.communicate()
proc = subprocess.Popen(["python manage_db.py db init"], stdout=subprocess.PIPE, shell=True)
(out, err) = proc.communicate()
proc = subprocess.Popen(["python manage_db.py db migrate"], stdout=subprocess.PIPE, shell=True)
(out, err) = proc.communicate()
proc = subprocess.Popen(["python manage_db.py db upgrade"], stdout=subprocess.PIPE, shell=True)
(out, err) = proc.communicate()