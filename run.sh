#!/bin/sh

forever start -c sudo python 3 run_server.py
source env/bin/activate
python gui/guizero_gui.py
forever stop run_server.py
