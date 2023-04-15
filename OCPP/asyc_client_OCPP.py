import asyncio
import websockets
from datetime import datetime
# from websocket import enableTrace, WebSocketApp

currentDateAndTime = datetime.now()
print("The current date and time is", currentDateAndTime)
# Output: The current date and time is 2022-03-19 10:05:39.482383

currentTime = currentDateAndTime.strftime("%H:%M:%S")
print("The current time is", currentTime)
# The current time is 10:06:55

###################################Configuration Keys##############################################
#server use
Host = "192.168.3.77"
SocketPort = 8080
HeartbeatInterval = 1
TEST_PATTERN_NUM = 7    #1、3、7、15、31、63
#client use
SERVER_IP   = "localhost"
SERVER_PORT	= 8080
GET		    ="/steve/websocket/CentralSystemService/1"	
###################################Arguments ##############################################
#EVSE > Server
OCPP_CallResult_authorize_old   = "[3,\r\n \"0401\",{\"expiryDate\":\"2022-12-07T20:11:11.111\", \"parentIdTag\":\"11111111\", \"status\":\"Accepted\"}]"
OCPP_CallResult_authorize       = "[3,\"0401\",{\"idTagInfo\":{\"status\":\"Invalid\"}}]"
OCPP_CallResult_boot            = "[3,\r\n \"0402\",{\"status\":\"Accepted\", \"currentTime\":\"2013-02-01T22:22:22.222\", \"interval\":500}]"
OCPP_CallResult_boot_ev         = "[2, \"20111111T11:11:25-cmd402\", \"BootNotification\", {    \"chargePointVendor\":    \"VendorHH_mark_home\",    \"chargePointModel\":    \"ModelFXN_mark_home\",    \"chargePointSerialNumber\":    \"CPSerialNumber99\",    \"chargeBoxSerialNumber\":    \"CBoxSerialNumber66\",    \"firmwareVersion\":    \"FW_v0.11\",    \"iccid\":    \"iccid44\",    \"imsi\":    \"imsi55\",    \"meterType\":    \"meterType66\",    \"meterSerialNumber\":    \"meterSerialNumber77\"}]"
OCPP_CallResult_heart_ev        = "[2, \"20230204T07:02:38-cmd406\", \"Heartbeat\", {}]"
OCPP_CallResult_heart           = "[3,\r\n \"0406\",{\"currentTime\":\"2066-06-06T20:66:66.6666\"}]"
OCPP_CallResult_heart_w         = "[3,\r\n \"0406\",{\"currentTime\":\"%s\"}]"
OCPP_CallResult_boot_r          = "[3,\"ocppuid\",{\"status\":\"Accepted\",\"currentTime\":\"ocppcurrentTime\",\"interval\":%d}]" % (HeartbeatInterval)
OCPP_CallResult_heart_r         = "[3,\"ocppuid\",{\"currentTime\":\"ocppcurrentTime\"}]"
#Server > EVSE
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

# start_server = websockets.serve(WebSocketserver_ChangeConfiguration, Host, SocketPort,compression=None,ping_interval=5)

# asyncio.get_event_loop().run_until_complete(start_server)
# asyncio.get_event_loop().run_forever()

#!/usr/bin/env python
async def ws_client():
    # SERVER_IP   = "192.168.3.171"
    # SERVER_PORT	= 8080
    # GET		    ="/steve/websocket/CentralSystemService/1"	
    # "GET /steve/websocket/CentralSystemService/1 HTTP/1.1"
    # "Host: 192.168.3.171:8080"
    
    target_uri = "ws://192.168.3.171:8080"
    target_uri_wwww = "ws://111.184.133.63:8080"
    header = " /steve/websocket/CentralSystemService/1"
    # print(target_uri)
    async with websockets.connect(f"ws://{SERVER_IP}:{SERVER_PORT}"  ,origin=None, extensions=None, compression=None ,subprotocols=["ocpp1.6"] ) as websocket:
        await websocket.send(OCPP_CallResult_boot_ev)
        Rxdata = await websocket.recv()
        print(Rxdata)
        while (1):
            await asyncio.sleep(3)
            await websocket.send(OCPP_CallResult_heart_ev)
            Rxdata = await websocket.recv()
            print(Rxdata)
            # Rxdata = await websocket.recv()
            # #print(f" Rx from EVSE:\r\n {Rxdata}\r\n")
            # # await websocket.send("88:8088 get!")
            # if "Authorize" in Rxdata:
            #     await websocket.send(OCPP_CallResult_authorize)
            

asyncio.get_event_loop().run_until_complete(ws_client())

