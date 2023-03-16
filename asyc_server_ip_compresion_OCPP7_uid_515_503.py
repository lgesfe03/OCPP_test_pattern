import asyncio
import websockets
from datetime import datetime

currentDateAndTime = datetime.now()
print("The current date and time is", currentDateAndTime)
# Output: The current date and time is 2022-03-19 10:05:39.482383

currentTime = currentDateAndTime.strftime("%H:%M:%S")
print("The current time is", currentTime)
# The current time is 10:06:55

###################################Configuration Keys##############################################

Host = "192.168.3.77"
SocketPort = 8080
HeartbeatInterval = 1
TEST_PATTERN_NUM = 7    #1、3、7、15、31、63
###################################Arguments ##############################################
#EVSE > Server
OCPP_CallResult_authorize_old   = "[3,\r\n \"0401\",{\"expiryDate\":\"2022-12-07T20:11:11.111\", \"parentIdTag\":\"11111111\", \"status\":\"Accepted\"}]"
OCPP_CallResult_authorize       = "[3,\"0401\",{\"idTagInfo\":{\"status\":\"Invalid\"}}]"
OCPP_CallResult_boot            = "[3,\r\n \"0402\",{\"status\":\"Accepted\", \"currentTime\":\"2013-02-01T22:22:22.222\", \"interval\":500}]"
OCPP_CallResult_heart           = "[3,\r\n \"0406\",{\"currentTime\":\"2066-06-06T20:66:66.6666\"}]"
OCPP_CallResult_heart_w         = "[3,\r\n \"0406\",{\"currentTime\":\"%s\"}]"
OCPP_CallResult_boot_r          = "[3,\"ocppuid\",{\"status\":\"Accepted\",\"currentTime\":\"ocppcurrentTime\",\"interval\":%d}]" % (HeartbeatInterval)
OCPP_CallResult_heart_r         = "[3,\"ocppuid\",{\"currentTime\":\"ocppcurrentTime\"}]"
#Server > EVSE
OCPP_Call_5_2_ChangeAvailable_old   = "[2,\r\n \"7a7b6330-280e-4ea6-bdab-c237452f3eb7\",\r\n \"ChangeAvailabilityRequest\", \r\n {\"connectorId\":502, \"type\":\"Operative\"}]"
OCPP_Call_5_2_ChangeAvailable       = "[2,\"b6117f0c-cdf1-45aa-bea0-e39a279c0900\",\"ChangeAvailability\",{\"connectorId\":0,\"type\":\"Operative\"}]"
OCPP_Call_5_5_ClearChargingProfile  = "[2,\"4451a27c-2a9c-465d-8320-16da57174f0e\",\"ClearChargingProfile\",{\"connectorId\":9453,\"chargingProfilePurpose\":\"TxDefaultProfile\",\"stackLevel\":4444}]"
OCPP_Call_5_18_UnlockConnector       = "[2,\"c14a5317-f38e-44d7-bbb4-0a260df373bd\",\"UnlockConnector\",{\"connectorId\":13579}]"
OCPP_Call_5_15_SendLocalList_old     =      "[2,\r\n \"Tx_LList_0515\",\r\n \"SendLocalListRequest\", \r\n {\"listVersion\":15151515, \"localAuthorizationList\":\"array\", \"updateType\":\"Differential\"}]"
OCPP_Call_5_15_SendLocalList1         = "[2,\"63f3173e-9a51-4418-a6c7-c9d4159b15b7\",\"SendLocalList\",{\"listVersion\":1,\"localAuthorizationList\":[{\"idTag\":\"1e0A49D265F82946\",\"idTagInfo\":{\"status\":\"Accepted\",\"expiryDate\":\"2022-12-23T12:33:00.000Z\"}}],\"updateType\":\"Full\"}]"
OCPP_Call_5_15_SendLocalList2        = "[2,\"0df084b9-05ed-458a-8f80-946400d2d500\",\"SendLocalList\",{\"listVersion\":2,\"localAuthorizationList\":[{\"idTag\":\"222E49D265F82222\",\"idTagInfo\":{\"status\":\"Accepted\",\"expiryDate\":\"2024-11-11T11:11:00.000Z\"}},{\"idTag\":\"2A3829D76137491D\",\"idTagInfo\":{\"status\":\"Accepted\",\"expiryDate\":\"2033-05-28T22:39:00.000Z\"}},{\"idTag\":\"1C7BFA3V\",\"idTagInfo\":{\"status\":\"Accepted\",\"expiryDate\":\"2024-09-27T13:53:00.000Z\"}},{\"idTag\":\"1A2B3C4D\",\"idTagInfo\":{\"status\":\"Expired\",\"expiryDate\":\"2023-02-17T03:40:00.000Z\"}}],\"updateType\":\"Full\"}]"
OCPP_Call_5_15_SendLocalList3        = "[2,\"fbb22ef8-1a23-44fc-82b7-cf1fb241a09f\",\"SendLocalList\",{\"listVersion\":3,\"localAuthorizationList\":[{\"idTag\":\"3B0A49D265F82946\",\"idTagInfo\":{\"status\":\"Expired\",\"expiryDate\":\"2022-12-23T12:33:00.000Z\"}},{\"idTag\":\"263E49D265F82946\",\"idTagInfo\":{\"status\":\"Expired\",\"expiryDate\":\"2022-12-26T07:28:00.000Z\"}},{\"idTag\":\"222E49D265F82222\",\"idTagInfo\":{\"status\":\"Expired\",\"expiryDate\":\"2022-12-28T08:47:00.000Z\"}},{\"idTag\":\"\",\"idTagInfo\":{\"status\":\"Blocked\"}},{\"idTag\":\"2A3829D76137491D\",\"idTagInfo\":{\"status\":\"Blocked\"}}],\"updateType\":\"Full\"}]"
OCPP_Call_5_3_ChangeConfiguration1   ="[2,\"11cacfc37-af7d-4a50-80a6-7ea762172d8c\",\"ChangeConfiguration\",{\"key\":\"StopTransactionSignatureFormat\",\"value\":\"SSSStopTRANSACTIONSIGNATUREformatSringValue\"}]"
OCPP_Call_5_3_ChangeConfiguration2   ="[2,\"22cacf874-9a48-487b-b037-5551013c37df\",\"ChangeConfiguration\",{\"key\":\"MeterValuesSampledData\",\"value\":\"mMmMmeterVVVSampleDATA\"}]"
OCPP_Call_5_3_ChangeConfiguration3   ="[2,\"33cacfff5-3e1a-4a61-aae8-2acb244d646a\",\"ChangeConfiguration\",{\"key\":\"HeartbeatInterval\",\"value\":\"77\"}]"
OCPP_Call_5_3_ChangeConfiguration200="[2,\"3dddfc37-af7d-4a50-80a6-7ea762172d8c\",\"ChangeConfiguration\",{\"key\":\"kkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkk\",\"value\":\"vvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvv\"}]"
OCPP_Call_5_3_ChangeConfiguration1000="[2,\"3dddfc37-af7d-4a50-80a6-7ea762172d8c\",\"ChangeConfiguration\",{\"key\":\"kkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkk\",\"value\":\"vvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvv\"}]"
OCPP_Call_5_3_ChangeConfiguration1500="[2,\"3dddfc37-af7d-4a50-80a6-7ea762172d8c\",\"ChangeConfiguration\",{\"key\":\"kkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkk\",\"value\":\"vvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvv\"}]"
OCPP_Call_5_3_ChangeConfiguration2000="[2,\"3dddfc37-af7d-4a50-80a6-7ea762172d8c\",\"ChangeConfiguration\",{\"key\":\"kkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkk\",\"value\":\"vvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvv\"}]"
OCPP_Call_5_3_ChangeConfiguration3000="[2,\"3dddfc37-af7d-4a50-80a6-7ea762172d8c\",\"ChangeConfiguration\",{\"key\":\"kkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkk\",\"value\":\"vvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvv\"}]"
OCPP_Call_5_7_GetCompositeSchedule1   = "[2,\"11a420c7-0c4e-4479-a542-324944ec1111\",\"GetCompositeSchedule\",{\"connectorId\":1,\"duration\":1211,\"chargingRateUnit\":\"A\"}]"
OCPP_Call_5_7_GetCompositeSchedule2   = "[2,\"22a420c7-0c4e-4479-a542-324944ec1222\",\"GetCompositeSchedule\",{\"connectorId\":2,\"duration\":2422,\"chargingRateUnit\":\"W\"}]"
OCPP_Call_5_7_GetCompositeSchedule3  = "[2,\"33a420c7-0c4e-4479-a542-324944ec1333\",\"GetCompositeSchedule\",{\"connectorId\":3,\"duration\":3633,\"chargingRateUnit\":\"A\"}]"
OCPP_Call_5_8_GetConfiguration1      = "[2,\"1c78ec00-1aff-4529-a622-557a4eca3911\",\"GetConfiguration\",{\"key\":[\"MeterValuesAlignedData\",\"MeterValuesSampledData\",\"MeterValuesSampledDataMaxLength\",\"MeterValuesSignatureContexts\",\"SupportedFeatureProfiles\",\"SupportedFileTransferProtocols\"]}]"
OCPP_Call_5_8_GetConfiguration2      = "[2,\"2a23ad04-1aff-4529-a622-2dea42863d22\",\"GetConfiguration\",{\"key\":[\"MinimumStatusDuration\",\"StopTxnAlignedData\",\"StopTxnAlignedDataMaxLength\"]}]"
OCPP_Call_5_8_GetConfiguration3      = "[2,\"3a5cc177-1aff-4529-a622-341254c2e696\",\"GetConfiguration\",{\"key\":[\"ChargingScheduleMaxPeriods\",\"ChargeProfileMaxStackLevel\",\"StopTxnSampledData\",\"GetConfigurationMaxKeys\",\"StopTransactionOnInvalidId\"]}]"
OCPP_Call_5_16_SetChargingProfile1   = "[2,\"102d4ad2-e5e3-40eb-b91b-30a2d7ee7b87\",\"SetChargingProfile\",{\"connectorId\":0,\"csChargingProfiles\":{\"chargingProfileId\":1,\"stackLevel\":2,\"chargingProfilePurpose\":\"ChargePointMaxProfile\",\"chargingProfileKind\":\"Absolute\",\"recurrencyKind\":\"Daily\",\"validFrom\":\"2022-12-23T00:00:00.000Z\",\"validTo\":\"2023-01-27T10:34:00.000Z\",\"chargingSchedule\":{\"duration\":3600,\"startSchedule\":\"2022-12-23T06:21:00.000Z\",\"chargingRateUnit\":\"W\",\"chargingSchedulePeriod\":[{\"startPeriod\":7,\"limit\":9,\"numberPhases\":3}],\"minChargingRate\":5}}}]"
OCPP_Call_5_16_SetChargingProfile2   = "[2,\"9f169b53-cd7f-4013-9bd2-072fdac0c1f0\",\"SetChargingProfile\",{\"connectorId\":0,\"csChargingProfiles\":{\"chargingProfileId\":2,\"stackLevel\":22,\"chargingProfilePurpose\":\"TxDefaultProfile\",\"chargingProfileKind\":\"Recurring\",\"recurrencyKind\":\"Weekly\",\"validFrom\":\"2023-01-03T07:45:00.000Z\",\"validTo\":\"2023-05-20T21:55:00.000Z\",\"chargingSchedule\":{\"duration\":2222,\"startSchedule\":\"2023-01-03T12:16:00.000Z\",\"chargingRateUnit\":\"W\",\"chargingSchedulePeriod\":[{\"startPeriod\":222,\"limit\":2222,\"numberPhases\":22222}],\"minChargingRate\":2.2}}}]"
OCPP_Call_5_16_SetChargingProfile3   = "[2,\"bdcc70b1-7595-4c01-bd93-0e139982d05b\",\"SetChargingProfile\",{\"connectorId\":0,\"csChargingProfiles\":{\"chargingProfileId\":3,\"stackLevel\":33,\"chargingProfilePurpose\":\"ChargePointMaxProfile\",\"chargingProfileKind\":\"Relative\",\"recurrencyKind\":\"Weekly\",\"validFrom\":\"2023-01-03T08:50:00.000Z\",\"validTo\":\"2024-04-26T14:48:00.000Z\",\"chargingSchedule\":{\"duration\":3333,\"startSchedule\":\"2023-01-05T18:52:00.000Z\",\"chargingRateUnit\":\"W\",\"chargingSchedulePeriod\":[{\"startPeriod\":11,\"limit\":2.2,\"numberPhases\":33},{\"startPeriod\":44,\"limit\":5.5,\"numberPhases\":66},{\"startPeriod\":77,\"limit\":88.9,\"numberPhases\":99}],\"minChargingRate\":3.3}}}]"
#OCPP_result_UpdateFirmware= "[2,\r\n \"19221119999\",\r\n \"UpdateFirmware\", \r\n {\"connectorId\":\"20221207777\", \"type\":\"Operative\"}]"
COUNT =0
###################################Component Functions##############################################
def find_uid(input):
    target_c = '\"'
    target_pos = []
    for pos,char in enumerate(input):
        if(char == target_c):
            target_pos.append(pos)
            if(len(target_pos) >= 2):
                break
    uid = input[target_pos[0]+1:target_pos[1]]
    return uid
def get_current_time():
    currentDateAndTime = datetime.now()
    t = str(currentDateAndTime)
    t = t.replace(' ','T')
    t = t[0:-3]
    t = t + 'Z'
    return t
def replace_uid_time(input,output):
    uid = find_uid(input)
    output = output.replace('ocppuid',uid)
    t = get_current_time()
    output = output.replace('ocppcurrentTime',t)
    return output
def count_time():
    global COUNT
    COUNT +=1
    #1、3、7、15、31、63
    COUNT &= TEST_PATTERN_NUM
    return COUNT
###################################Test Pattern##############################################

#5-0
async def WebSocketserver_send(websocket, path):
    while (1):
        # Rxdata = await websocket.recv()
        # if "BootNotification" in Rxdata:
        #     tx = replace_uid_time(Rxdata,OCPP_CallResult_boot_r)
        #     await websocket.send(tx)
        # if "Heartbeat" in Rxdata:
        #     tx = replace_uid_time(Rxdata,OCPP_CallResult_heart_r)
        #     await websocket.send(tx)
        await asyncio.sleep(0.05)
        count = count_time()
        if count == 8:
            await websocket.send(OCPP_Call_5_15_SendLocalList1)
        elif count == 5:
            await websocket.send(OCPP_Call_5_15_SendLocalList2)
        elif count == 2:
            await websocket.send(OCPP_Call_5_3_ChangeConfiguration1)
        elif count == 7:
            await websocket.send(OCPP_Call_5_3_ChangeConfiguration2)
        elif count == 4:
            await websocket.send(OCPP_Call_5_16_SetChargingProfile2)
        elif count == 1:
            await websocket.send(OCPP_Call_5_16_SetChargingProfile3)
        elif count == 6:
            await websocket.send(OCPP_Call_5_8_GetConfiguration1)
        elif count == 3:
            await websocket.send(OCPP_Call_5_8_GetConfiguration2)
        else:
            await websocket.send(OCPP_Call_5_3_ChangeConfiguration3)
        Rxdata = await websocket.recv()
        if "Authorize" in Rxdata:
            await websocket.send(OCPP_CallResult_authorize)
        if "BootNotification" in Rxdata:
            tx = replace_uid_time(Rxdata,OCPP_CallResult_boot_r)
            await websocket.send(tx)
        if "Heartbeat" in Rxdata:
            tx = replace_uid_time(Rxdata,OCPP_CallResult_heart_r)
            await websocket.send(tx)
        if "[3," in Rxdata:
            print(Rxdata)
        # else:
        #     print("=========skip========")
#5-03
async def WebSocketserver_ChangeConfiguration(websocket, path):
     while (1):
        await asyncio.sleep(0.05)
        count = count_time()
        if count == 2:
            await websocket.send(OCPP_Call_5_3_ChangeConfiguration1)
        elif count == 1:
            await websocket.send(OCPP_Call_5_3_ChangeConfiguration2)
        else:
            await websocket.send(OCPP_Call_5_3_ChangeConfiguration3)
        Rxdata = await websocket.recv()
        if "Authorize" in Rxdata:
            await websocket.send(OCPP_CallResult_authorize)
        if "BootNotification" in Rxdata:
            tx = replace_uid_time(Rxdata,OCPP_CallResult_boot_r)
            await websocket.send(tx)
        if "Heartbeat" in Rxdata:
            tx = replace_uid_time(Rxdata,OCPP_CallResult_heart_r)
            await websocket.send(tx)
        if "[3," in Rxdata:
            print(Rxdata)
        # else:
        #     print("=========skip========")
#5-07
async def WebSocketserver_GetCompositeSchedule(websocket, path):
    while (1):
        Rxdata = await websocket.recv()
        if "Authorize" in Rxdata:
            await websocket.send(OCPP_CallResult_authorize)
#5-08
async def WebSocketserver_GetConfiguration(websocket, path):
    while (1):
        await asyncio.sleep(0.05)
        count = count_time()
        if count == 2:
            await websocket.send(OCPP_Call_5_8_GetConfiguration1)
        elif count == 1:
            await websocket.send(OCPP_Call_5_8_GetConfiguration2)
        else:
            await websocket.send(OCPP_Call_5_8_GetConfiguration3)
        Rxdata = await websocket.recv()
        if "Authorize" in Rxdata:
            await websocket.send(OCPP_CallResult_authorize)
        if "BootNotification" in Rxdata:
            tx = replace_uid_time(Rxdata,OCPP_CallResult_boot_r)
            await websocket.send(tx)
        if "Heartbeat" in Rxdata:
            tx = replace_uid_time(Rxdata,OCPP_CallResult_heart_r)
            await websocket.send(tx)
        if "[3," in Rxdata:
            print(Rxdata)
#5-15
async def WebSocketserver_SendLocalList(websocket, path):
    while (1):
        Rxdata = await websocket.recv()
        if "Authorize" in Rxdata:
            await websocket.send(OCPP_CallResult_authorize)
#5-16
async def WebSocketserver_SetChargingProfile(websocket, path):
    while (1):
        #await websocket.send(OCPP_Call_5__ChangeAvailable)
        Rxdata = await websocket.recv()
        #print(f" Rx from EVSE:\r\n {Rxdata}\r\n")
        # await websocket.send("88:8088 get!")
        if "Authorize" in Rxdata:
            await websocket.send(OCPP_CallResult_authorize)

start_server = websockets.serve(WebSocketserver_ChangeConfiguration, Host, SocketPort,compression=None,ping_interval=5)

asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()

