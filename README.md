
Author : Mark Lin YL

Date: 2022/11

# Introduction
This repository is used to act as an OCPP server, sending certain message to OCPP client.
Server wlll keep waiting for client to shakehand once startup.
Client will need to connect to server and sending ceratin shakehand message by HTTP, then upgrade into OCPP.

# Reference Documents:
* OCPP-J 1.6 Specification
* RFC6455 : The WebSocket Protocol

1.Python-3.11.9	
Download from web Python 3.11.9
2.Python-Websockets	
  ````
  pip install websockets==12
  ````
3.Python-Selenium
  ````
  pip install selenium==4.27.1
  ````
