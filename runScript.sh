#!/bin/bash

stty sane

#python3 -m venv EnvKaleidoscope
#source EnvKaleidoscope/bin/activate
#pip3 install -r requirements.txt
python3 menu2.py

rm ./database/listener.db
#rm ./history/commandHistory
