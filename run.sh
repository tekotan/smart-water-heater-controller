#!/bin/bash

sudo python3 run_server.py >> log.txt & 
source env/bin/activate
cd gui
python guizero_gui.py
