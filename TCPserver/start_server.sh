#!/bin/bash
echo "Starting the service for DTU"
python3 TCPserver_DTU.py & > DTU_server.log
sleep 1
echo "starting the service for Phone APP"
python3 TCPserver_phone.py & > Phone_server.log
echo "started"