#!/bin/bash

stty sane

sudo python3 menu2.py

sudo rm ./database/listener.db
#sudo rm ./history/commandHistory
