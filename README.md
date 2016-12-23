# Machine Learning: Think and Speak
## 2016Fall Capstone Group 4
----
* TCPclient

This part contains all local TCP clients like data generators.

* TCPserver

This part contains all server communications parts like server-DTU, server-Brain, server-Phone. Two key scripts are `TCPserver_DTU.py` and `TCPserver_phone.py`.

* think

Thinks part contains all algorithms and clients in thinking part. Execute `main.py` to start the thinking algortihms. 

* motor

An open-source G-code interperator for Arduino. 

* AndroidAPP

Source code of the Android phone application.

For more details, refer to the sepecifc README file in each part.

----
## How to set up the whole system

- Make sure the target server is running on an operating system with Linux kernel. `Ubuntu 14.04` is take as a an example.
- Copy this code to your target cloud server, write down the public IP address of the server.
- Install PostgreSQL and related Python3 libraries. Refer to `/TCPserver/README.md`.
- Install libraries for fast computation. Refer to `/think/README.md`.
- Write your server IP to the configuration `/TCPserver/TCPconfig.py`.
- Start server scripts

In one terminal, type:
```
cd TCPserver
python3 TCPserver_DTU.py
```

In another terminal, type:
```
cd TCPserver
python3 TCPserver_phone.py
```
Keep these two terminals live, otherwise the services will be terminated.

- Start thinking algorithms
Open yet another terminal, type:
```
cd think
python3 main.py
```
keep the terminal live.

- Power up the machine. The machine will autonomously initiate a TCP connection with the server.
- Select a job on the touch screen, press `Execute` button to start. If authentication is required, the passphrase is a single digit `1`.
- Done.