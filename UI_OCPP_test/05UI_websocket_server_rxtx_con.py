import sys
import asyncio
import threading
import websockets
import time
from datetime import datetime

# from PySide6.QtCore import *
# from PySide6.QtGui import *
# from PySide6.QtWidgets import *
from PySide6.QtWidgets import QApplication, QMainWindow, QLineEdit, QPushButton, QLabel,QMessageBox
from PySide6.QtGui import QPixmap
from PySide6.QtCore import Qt, QThread, Signal

IMAGE_PATH = "..\ico\ocpp16.jpg"
# SERVER_IP = "localhost"
SERVER_IP = "192.168.3.171"
SERVER_PORT = 8080
HeartbeatInterval = 60
TEST_PATTERN_NUM = 7    #1、3、7、15、31、63
WS_PING_INTERVAL = 30
TEST_4_INTERVAL = 1
###################################Arguments ##############################################
#EVSE > Server
# OCPP_CallResult_authorize_old   = "[3,\r\n \"0401\",{\"expiryDate\":\"2022-12-07T20:11:11.111\", \"parentIdTag\":\"11111111\", \"status\":\"Accepted\"}]"
OCPP_CallResult_authorize       = "[3,\"0401\",{\"idTagInfo\":{\"status\":\"Invalid\"}}]"
# OCPP_CallResult_boot            = "[3,\r\n \"0402\",{\"status\":\"Accepted\", \"currentTime\":\"2013-02-01T22:22:22.222\", \"interval\":500}]"
# OCPP_CallResult_boot_ev         = "[2, \"20111111T11:11:25-cmd402\", \"BootNotification\", {    \"chargePointVendor\":    \"VendorHH_mark_home\",    \"chargePointModel\":    \"ModelFXN_mark_home\",    \"chargePointSerialNumber\":    \"CPSerialNumber99\",    \"chargeBoxSerialNumber\":    \"CBoxSerialNumber66\",    \"firmwareVersion\":    \"FW_v0.11\",    \"iccid\":    \"iccid44\",    \"imsi\":    \"imsi55\",    \"meterType\":    \"meterType66\",    \"meterSerialNumber\":    \"meterSerialNumber77\"}]"
# OCPP_CallResult_heart_ev        = "[2, \"20230204T07:02:38-cmd406\", \"Heartbeat\", {}]"
# OCPP_CallResult_heart           = "[3,\r\n \"0406\",{\"currentTime\":\"2066-06-06T20:66:66.6666\"}]"
# OCPP_CallResult_heart_w         = "[3,\r\n \"0406\",{\"currentTime\":\"%s\"}]"
OCPP_CallResult_auth_r         = "[3,\"ocppuid\",{}]"
OCPP_CallResult_boot_r          = "[3,\"ocppuid\",{\"status\":\"Accepted\",\"currentTime\":\"ocppcurrentTime\",\"interval\":%d}]" % (HeartbeatInterval)
OCPP_CallResult_data_r         = "[3,\"ocppuid\",{}]"
OCPP_CallResult_diag_r         = "[3,\"ocppuid\",{}]"
OCPP_CallResult_fw_r            = "[3,\"ocppuid\",{}]"
OCPP_CallResult_heart_r         = "[3,\"ocppuid\",{\"currentTime\":\"ocppcurrentTime\"}]"
OCPP_CallResult_meter_r         = "[3,\"ocppuid\",{}]"
OCPP_CallResult_start_r         = "[3,\"ocppuid\",{}]"
OCPP_CallResult_stat_r         = "[3,\"ocppuid\",{}]"
OCPP_CallResult_stop_r         = "[3,\"ocppuid\",{}]"
#Server > EVSE
OCPP_Call_5_1_CancelReservation     = ""
OCPP_Call_5_2_ChangeAvailability    = "[2,\"2c54d865-12da-4fb2-ab4f-d0689a592b3c\",\"ChangeAvailability\",{\"connectorId\":9453,\"type\":\"Inoperative\"}]"
OCPP_Call_5_3_ChangeConfiguration   = "[2,\"32660af5-3e1a-4a61-aae8-2acb244d646a\",\"ChangeConfiguration\",{\"key\":\"HeartbeatInterval\",\"value\":\"77\"}]"
OCPP_Call_5_4_ClearCache            = "[2,\"c1b1bdf4-2db1-4592-9034-db5cb8675ee9\",\"ClearCache\",\{\}]"
OCPP_Call_5_5_ClearChargingProfile  = "[2,\"4451a27c-2a9c-465d-8320-16da57174f0e\",\"ClearChargingProfile\",{\"connectorId\":9453,\"chargingProfilePurpose\":\"TxDefaultProfile\",\"stackLevel\":4444}]"
OCPP_Call_5_6_DataTransfer_Rx       = "[2,\"DataTransfer_RxID\",\"DataTransfer\",{\"vendorId\":\"vID\",\"messageId\":\"msgID\",\"data\":\"replace_sendcmd\"}]"
OCPP_Call_5_6_DataTransfer_Rx_start       = "[2,\"93ee9e4a-fd0f-4d01-945e-45fc4301695a\",\"DataTransfer\",{\"vendorId\":\"StartTransaction\",\"messageId\":\"StartTransaction\",\"data\":\"StartTransaction\"}]"
OCPP_Call_5_6_DataTransfer_Rx_stop       = "[2,\"93ee9e4a-fd0f-4d01-945e-45fc4301695a\",\"DataTransfer\",{\"vendorId\":\"StopTransaction\",\"messageId\":\"StopTransaction\",\"data\":\"StopTransaction\"}]"
OCPP_Call_5_7_GetCompositeSchedule  = "[2,\"7fa420c7-0c4e-4479-a542-324944ec1757\",\"GetCompositeSchedule\",{\"connectorId\":9453,\"duration\":3600,\"chargingRateUnit\":\"A\"}]"
OCPP_Call_5_8_GetConfiguration3     = "[2,\"3a5cc177-1aff-4529-a622-341254c2e696\",\"GetConfiguration\",{\"key\":[\"ChargingScheduleMaxPeriods\",\"ChargeProfileMaxStackLevel\",\"StopTxnSampledData\",\"GetConfigurationMaxKeys\",\"StopTransactionOnInvalidId\"]}]"
OCPP_Call_5_9_GetDiagnostics        = "[2,\"f0508624-2953-4d68-9e79-7dfc52952c05\",\"GetDiagnostics\",{\"location\":\"Location(directoryURI):www.google.com\",\"startTime\":\"2022-02-03T10:35:00.000Z\",\"stopTime\":\"2022-11-16T10:34:00.000Z\",\"retries\":123,\"retryInterval\":6666}]"
OCPP_Call_5_10_GetLocalListVersion  = "[2,\"b1125361-ffc8-42ae-9846-31280bf75489\",\"GetLocalListVersion\",\{\}]"
OCPP_Call_5_11_RemoteStartTransaction   = "[2,\"9e6f4daa-ce67-4350-8741-7c20e487916d\",\"RemoteStartTransaction\",{\"connectorId\":123,\"idTag\":\"222E49D265F82222\"}]"
OCPP_Call_5_12_RemoteStopTransaction    = ""
OCPP_Call_5_13_ReserveNow           = "[2,\"59ac7412-47c7-4c3b-8a2a-045050c67745\",\"ReserveNow\",{\"connectorId\":123,\"expiryDate\":\"2023-02-04T15:38:00.000Z\",\"idTag\":\"222E49D265F82222\",\"reservationId\":11}]"
OCPP_Call_5_14_Reset                = "[2,\"7bb392b3-bf92-4b07-846f-87a6b2e2c2ae\",\"Reset\",{\"type\":\"Hard\"}]"
OCPP_Call_5_15_SendLocalList        = "[2,\"aceda291-eb06-40dd-8908-c8f7c8395f1e\",\"SendLocalList\",{\"listVersion\":123,\"localAuthorizationList\":[{\"idTag\":\"222E49D265F82222\",\"idTagInfo\":{\"status\":\"Accepted\",\"expiryDate\":\"2024-11-11T11:11:00.000Z\"}},{\"idTag\":\"2A3829D76137491D\",\"idTagInfo\":{\"status\":\"Accepted\",\"expiryDate\":\"2033-05-28T22:39:00.000Z\"}}],\"updateType\":\"Full\"}]"
OCPP_Call_5_16_SetChargingProfile1   = "[2,\"102d4ad2-e5e3-40eb-b91b-30a2d7ee7b87\",\"SetChargingProfile\",{\"connectorId\":0,\"csChargingProfiles\":{\"chargingProfileId\":1,\"stackLevel\":2,\"chargingProfilePurpose\":\"ChargePointMaxProfile\",\"chargingProfileKind\":\"Absolute\",\"recurrencyKind\":\"Daily\",\"validFrom\":\"2022-12-23T00:00:00.000Z\",\"validTo\":\"2023-01-27T10:34:00.000Z\",\"chargingSchedule\":{\"duration\":3600,\"startSchedule\":\"2022-12-23T06:21:00.000Z\",\"chargingRateUnit\":\"W\",\"chargingSchedulePeriod\":[{\"startPeriod\":7,\"limit\":9,\"numberPhases\":3}],\"minChargingRate\":5}}}]"
OCPP_Call_5_16_SetChargingProfile2   = "[2,\"9f169b53-cd7f-4013-9bd2-072fdac0c1f0\",\"SetChargingProfile\",{\"connectorId\":0,\"csChargingProfiles\":{\"chargingProfileId\":2,\"stackLevel\":22,\"chargingProfilePurpose\":\"TxDefaultProfile\",\"chargingProfileKind\":\"Recurring\",\"recurrencyKind\":\"Weekly\",\"validFrom\":\"2023-01-03T07:45:00.000Z\",\"validTo\":\"2023-05-20T21:55:00.000Z\",\"chargingSchedule\":{\"duration\":2222,\"startSchedule\":\"2023-01-03T12:16:00.000Z\",\"chargingRateUnit\":\"W\",\"chargingSchedulePeriod\":[{\"startPeriod\":222,\"limit\":2222,\"numberPhases\":22222}],\"minChargingRate\":2.2}}}]"
OCPP_Call_5_16_SetChargingProfile3   = "[2,\"bdcc70b1-7595-4c01-bd93-0e139982d05b\",\"SetChargingProfile\",{\"connectorId\":0,\"csChargingProfiles\":{\"chargingProfileId\":3,\"stackLevel\":33,\"chargingProfilePurpose\":\"ChargePointMaxProfile\",\"chargingProfileKind\":\"Relative\",\"recurrencyKind\":\"Weekly\",\"validFrom\":\"2023-01-03T08:50:00.000Z\",\"validTo\":\"2024-04-26T14:48:00.000Z\",\"chargingSchedule\":{\"duration\":3333,\"startSchedule\":\"2023-01-05T18:52:00.000Z\",\"chargingRateUnit\":\"W\",\"chargingSchedulePeriod\":[{\"startPeriod\":11,\"limit\":2.2,\"numberPhases\":33},{\"startPeriod\":44,\"limit\":5.5,\"numberPhases\":66},{\"startPeriod\":77,\"limit\":88.9,\"numberPhases\":99}],\"minChargingRate\":3.3}}}]"
OCPP_Call_5_17_TriggerMessage        = "[2,\"6bcf0b75-9681-48ce-a1c4-7b6c7cd63c86\",\"TriggerMessage\",{\"requestedMessage\":\"MeterValues\",\"connectorId\":777}]"
OCPP_Call_5_18_UnlockConnector      = "[2,\"c14a5317-f38e-44d7-bbb4-0a260df373bd\",\"UnlockConnector\",{\"connectorId\":13579}]"
OCPP_Call_5_19_UpdateFirmware       = "[2,\"82c4adab-21a3-4afa-bd2c-a4be02084179\",\"UpdateFirmware\",{\"retrieveDate\":\"2023-02-04T11:26:00.000Z\",\"location\":\"Location(directoryURI):www.google.com\",\"retries\":111,\"retryInterval\":6666}]"

class MainWindow(QMainWindow):
    client_connected = Signal(str)
    client_disconnected = Signal()
    #UI initialize
    def __init__(self):
        super().__init__()
        self.toggle = False
        # Set the window title and size
        self.setWindowTitle("OCPP 1.6 Test Tool")
        self.current_height = 0
        # self.resize(400, 300)
        # Create a label to display the background image
        self.backgroundLabel = QLabel(self)
        self.backgroundLabel.setScaledContents(True)
        self.backgroundLabel.setGeometry(10, self.current_height, 200, self.height_arranger(150)) 
        # Create a label for the welcome message
        self.welcomeLabel = QLabel("1.Type IPv4 below and click \"Start Server\"", self)
        # self.welcomeLabel.setAlignment(Qt.AlignCenter)
        self.welcomeLabel.setGeometry(10, self.current_height, 800, self.height_arranger(25))
        # Create a line edit for entering the IP address of the WebSocket server
        self.host_edit = QLineEdit(SERVER_IP, self)
        self.host_edit.setGeometry(10, self.current_height, 200, self.height_arranger(25)) 
        
        # Create a button for starting the WebSocket server
        self.button_start_server = QPushButton("Start server", self)
        self.button_start_server.setGeometry(10, self.current_height, 200, self.height_arranger(25)) 
        self.button_start_server.clicked.connect(self.start_server)
        
        # Create a button for sending a WebSocket message
        self.button_disconnect = QPushButton("Disconnect", self)
        self.button_disconnect.setEnabled(False)
        self.button_disconnect.setGeometry(10, self.current_height, 200, self.height_arranger(25)) 
        self.button_disconnect.clicked.connect(self.btn_disconnect)
        ###############################OCPP-5-cmd########################################
        # Create a button for sending a OCPP message
        self.button_send_message_501 = QPushButton("Send OCPP 5-1", self)
        self.button_send_message_501.setGeometry(10, self.current_height, 100, 25)
        self.button_send_message_501.clicked.connect(self.btn_send_message501)
        self.button_send_message_501.setEnabled(False)
        # Create a button for sending a OCPP message
        self.button_send_message_502 = QPushButton("Send OCPP 5-2", self)
        self.button_send_message_502.setGeometry(110, self.current_height, 100, 25)
        self.button_send_message_502.clicked.connect(self.btn_send_message502)
        # Create a button for sending a OCPP message
        self.button_send_message_503 = QPushButton("Send OCPP 5-3", self)
        self.button_send_message_503.setGeometry(210, self.current_height, 100, self.height_arranger(25)) 
        self.button_send_message_503.clicked.connect(self.btn_send_message503)
        # Create a button for sending a OCPP message
        self.button_send_message_504 = QPushButton("Send OCPP 5-4", self)
        self.button_send_message_504.setGeometry(10, self.current_height, 100, 25)
        self.button_send_message_504.clicked.connect(self.btn_send_message504)
        # Create a button for sending a OCPP message
        self.button_send_message_505 = QPushButton("Send OCPP 5-5", self)
        self.button_send_message_505.setGeometry(110, self.current_height, 100, 25)
        self.button_send_message_505.clicked.connect(self.btn_send_message505)
        # # Create a button for sending a OCPP message
        self.button_send_message_506 = QPushButton("Send OCPP 5-6", self)
        self.button_send_message_506.setGeometry(410, self.current_height, 100, 25) 
        self.button_send_message_506.clicked.connect(self.btn_send_message506)
        # Create a button for sending a OCPP message
        self.button_send_message_506start = QPushButton("Send OCPP 5-6-start", self)
        self.button_send_message_506start.setGeometry(210, self.current_height, 100, 25) 
        self.button_send_message_506start.clicked.connect(self.btn_send_message506_1)
        # Create a button for sending a OCPP message
        self.button_send_message_506stop = QPushButton("Send OCPP 5-6-stop", self)
        self.button_send_message_506stop.setGeometry(310, self.current_height, 100, self.height_arranger(25)) 
        self.button_send_message_506stop.clicked.connect(self.btn_send_message506_2)
        # Create a button for sending a OCPP message
        self.button_send_message_507 = QPushButton("Send OCPP 5-7", self)
        self.button_send_message_507.setGeometry(10, self.current_height, 100, 25)
        self.button_send_message_507.clicked.connect(self.btn_send_message507)
        # Create a button for sending a OCPP message
        self.button_send_message_508 = QPushButton("Send OCPP 5-8", self)
        self.button_send_message_508.setGeometry(110, self.current_height, 100, 25)
        self.button_send_message_508.clicked.connect(self.btn_send_message508)
        # Create a button for sending a OCPP message
        self.button_send_message_509 = QPushButton("Send OCPP 5-9", self)
        self.button_send_message_509.setGeometry(210, self.current_height, 100, self.height_arranger(25)) 
        self.button_send_message_509.clicked.connect(self.btn_send_message509)
        # Create a button for sending a OCPP message
        self.button_send_message_510 = QPushButton("Send OCPP 5-10", self)
        self.button_send_message_510.setGeometry(10, self.current_height, 100, 25)
        self.button_send_message_510.clicked.connect(self.btn_send_message510)
        # Create a button for sending a OCPP message
        self.button_send_message_511 = QPushButton("Send OCPP 5-11", self)
        self.button_send_message_511.setGeometry(110, self.current_height, 100, 25)
        self.button_send_message_511.clicked.connect(self.btn_send_message511)
        # Create a button for sending a OCPP message
        self.button_send_message_512 = QPushButton("Send OCPP 5-12", self)
        self.button_send_message_512.setGeometry(210, self.current_height, 100, self.height_arranger(25)) 
        self.button_send_message_512.clicked.connect(self.btn_send_message512)
        self.button_send_message_512.setEnabled(False)
        # Create a button for sending a OCPP message
        self.button_send_message_513 = QPushButton("Send OCPP 5-13", self)
        self.button_send_message_513.setGeometry(10, self.current_height, 100, 25)
        self.button_send_message_513.clicked.connect(self.btn_send_message513)
        # Create a button for sending a OCPP message
        self.button_send_message_514 = QPushButton("Send OCPP 5-14", self)
        self.button_send_message_514.setGeometry(110, self.current_height, 100, 25)
        self.button_send_message_514.clicked.connect(self.btn_send_message514)
        # Create a button for sending a OCPP message
        self.button_send_message_515 = QPushButton("Send OCPP 5-15", self)
        self.button_send_message_515.setGeometry(210, self.current_height, 100, self.height_arranger(25)) 
        self.button_send_message_515.clicked.connect(self.btn_send_message515)
        # Create a button for sending a OCPP message
        self.button_send_message_516 = QPushButton("Send OCPP 5-16", self)
        self.button_send_message_516.setGeometry(10, self.current_height, 100, 25)
        self.button_send_message_516.clicked.connect(self.btn_send_message516)
        # Create a button for sending a OCPP message
        self.button_send_message_517 = QPushButton("Send OCPP 5-17", self)
        self.button_send_message_517.setGeometry(110, self.current_height, 100, 25)
        self.button_send_message_517.clicked.connect(self.btn_send_message517)
        # Create a button for sending a OCPP message
        self.button_send_message_518 = QPushButton("Send OCPP 5-18", self)
        self.button_send_message_518.setGeometry(210, self.current_height, 100, self.height_arranger(25)) 
        self.button_send_message_518.clicked.connect(self.btn_send_message518)
        # Create a button for sending a OCPP message
        self.button_send_message_519 = QPushButton("Send OCPP 5-19", self)
        self.button_send_message_519.setGeometry(10, self.current_height, 100, self.height_arranger(25)) 
        self.button_send_message_519.clicked.connect(self.btn_send_message519)

        # Create a label to display the server status
        #status: server
        self.statuslabel_head         = QLabel("Server Status:  ", self)
        self.statuslabel_head.setGeometry(10, self.current_height, 100, 25)
        self.statuslabel = QLabel("Not Start", self)
        self.statuslabel.setGeometry(110, self.current_height, 200, self.height_arranger(25))
        #Show connection from sample
        self.connected_label = QLabel("WebSocket server not started", self)
        self.client_label = QLabel("No client connected", self)
        self.connected_label.setGeometry(10, self.current_height, 600, self.height_arranger(25))
        self.client_label.setGeometry(10, self.current_height,    300, self.height_arranger(25))
        
        # Create a label to display the server rx
        self.msglabel_head = QLabel("Rx:", self)
        self.msglabel_head.setGeometry(10, self.current_height, 100, self.height_arranger(25))
        # Create a label to display the server rx
        self.msglabel = QLabel("info", self)
        self.msglabel.setGeometry(10, self.current_height, 600, self.height_arranger(100))
        

    
    def setBackgroundImage(self, imagePath):
        # Set the background image of the UI
        pixmap = QPixmap(imagePath)
        self.backgroundLabel.setPixmap(pixmap)

    def height_arranger(self, height):
        self.current_height += height + 10
        return height

    #************************Websocket related************************
    def start_server(self):
        # Create a new thread for the WebSocket server and start it
        self.server_thread = threading.Thread(target=self.start_server_thread)
        self.server_thread.start()
        self.client_connected.connect(self.update_connected_label)
        self.client_disconnected.connect(self.update_disconnected_label)
        self.button_start_server.setEnabled(False)
    def start_server_thread(self):
        self.host = self.host_edit.text()
        self.port = SERVER_PORT  # Change this to the port you want to use
        self.statuslabel.setText("Started ✓")
        asyncio.run(self.websocket_server(self.host, self.port))

    async def websocket_server(self, host, port):
        try:
            async with websockets.serve(self.websocket_handler_rx, host, port, ping_interval=30):
                await asyncio.Future()  # Keep the server running indefinitely
        except OSError:
            self.alert_window("Only 1 server at once!")

    def update_connected_label(self, message):
        self.connected_label.setText(f"WebSocket server running on {message}")
        self.client_label.setText(f"Client connected: {message.split(': ')[1]}")
        self.button_disconnect.setEnabled(True)
    def update_disconnected_label(self):
        self.connected_label.setText("WebSocket server not started")
        self.client_label.setText("No client connected")
        self.button_disconnect.setEnabled(False)

    async def websocket_handler_rx(self, websocket, path):
        self.connected_clients = set()  # Keep track of connected clients
        self.connected_clients.add(websocket)
        self.client_connected.emit(f"Client connected: {websocket.remote_address[0]}")
        try:
            async for Rxdata in websocket:
                print(f"Received message from {websocket.remote_address[0]}: {Rxdata}")
                self.msglabel.setText(Rxdata)
                if "Authorize" in Rxdata:
                    tx = self.replace_uid_time(Rxdata,OCPP_CallResult_auth_r)
                    await websocket.send(tx)
                if "BootNotification" in Rxdata:
                    print("rx=",Rxdata)
                    tx = self.replace_uid_time(Rxdata,OCPP_CallResult_boot_r)
                    print("tx=",tx)
                    await websocket.send(tx)
                if "DataTransfer" in Rxdata:
                    tx = self.replace_uid_time(Rxdata,OCPP_CallResult_data_r)
                    await websocket.send(tx)
                if "DiagnosticsStatusNotification" in Rxdata:
                    tx = self.replace_uid_time(Rxdata,OCPP_CallResult_diag_r)
                    await websocket.send(tx)
                if "FirmwareStatusNotification" in Rxdata:
                    tx = self.replace_uid_time(Rxdata,OCPP_CallResult_fw_r)
                    await websocket.send(tx)
                if "Heartbeat" in Rxdata:
                    tx = self.replace_uid_time(Rxdata,OCPP_CallResult_heart_r)
                    await websocket.send(tx)
                if "MeterValues" in Rxdata:
                    tx = self.replace_uid_time(Rxdata,OCPP_CallResult_meter_r)
                    await websocket.send(tx)
                if "StartTransaction" in Rxdata:
                    tx = self.replace_uid_time(Rxdata,OCPP_CallResult_start_r)
                    await websocket.send(tx)
                if "StatusNotification" in Rxdata:
                    tx = self.replace_uid_time(Rxdata,OCPP_CallResult_stat_r)
                    await websocket.send(tx)
                if "StopTransaction" in Rxdata:
                    tx = self.replace_uid_time(Rxdata,OCPP_CallResult_stop_r)
                    await websocket.send(tx)
        except websockets.exceptions.ConnectionClosedError:
            pass
        finally:
            self.client_disconnected.emit()

    async def websocket_handler_tx(self, message):
        try:
            for websocket in self.connected_clients:
                print("connected_clients=",self.connected_clients)
                print("websocket=",websocket)
                await websocket.send(message)
                self.msglabel.setText(message)
        except AttributeError:
            self.alert_window("None connected client")
            self.toggle = False
            # dlg = QMessageBox(self)
            # dlg.setWindowTitle("Alert")
            # dlg.setText("None connected client")
            # dlg.exec_()

    async def btn_disconnect(self):
        print("connected_clients=",self.connected_clients)
        self.client_disconnected.emit()
    
    def btn_send_message501(self):
        asyncio.run(self.websocket_handler_tx(OCPP_Call_5_1_CancelReservation))
    def btn_send_message502(self):
        asyncio.run(self.websocket_handler_tx(OCPP_Call_5_2_ChangeAvailability))
    def btn_send_message503(self):
        asyncio.run(self.websocket_handler_tx(OCPP_Call_5_3_ChangeConfiguration))
    def btn_send_message504(self):
        asyncio.run(self.websocket_handler_tx(OCPP_Call_5_4_ClearCache))
    def btn_send_message505(self):
        asyncio.run(self.websocket_handler_tx(OCPP_Call_5_5_ClearChargingProfile))
    def btn_send_message506(self):
        if(self.toggle): 
            self.toggle = False
        else:
            self.toggle = True
        
        while(self.toggle):
            try:
                # print("Auto run 4-1 ~ 4-6 + 4-9")
                # asyncio.run(self.websocket_handler_tx(self.replace_sendcmd("Authorize")))
                # time.sleep(TEST_4_INTERVAL)
                # asyncio.run(self.websocket_handler_tx(self.replace_sendcmd("BootNotification")))
                # time.sleep(TEST_4_INTERVAL)
                # asyncio.run(self.websocket_handler_tx(self.replace_sendcmd("DataTransfer_Tx")))
                # time.sleep(TEST_4_INTERVAL)
                # asyncio.run(self.websocket_handler_tx(self.replace_sendcmd("DiagnosticsStatusNotification")))
                # time.sleep(TEST_4_INTERVAL)
                # asyncio.run(self.websocket_handler_tx(self.replace_sendcmd("FirmwareStatusNotification")))
                # time.sleep(TEST_4_INTERVAL)
                # asyncio.run(self.websocket_handler_tx(self.replace_sendcmd("Heartbeat")))
                # time.sleep(TEST_4_INTERVAL)
                # asyncio.run(self.websocket_handler_tx(self.replace_sendcmd("StatusNotification")))
                # time.sleep(TEST_4_INTERVAL)  

                print("Auto run 4-7、4-8、4-10")
                #4-8
                # asyncio.run(self.websocket_handler_tx(self.replace_sendcmd("StartTransaction")))
                # time.sleep(60)  
                asyncio.run(self.websocket_handler_tx(self.replace_sendcmd("MeterValues")))
                time.sleep(0.1)  
                # #4-10
                # asyncio.run(self.websocket_handler_tx(self.replace_sendcmd("StopTransaction")))
                # time.sleep(TEST_4_INTERVAL)  

            except:
                return 1
        
    def btn_send_message506_1(self):
        asyncio.run(self.websocket_handler_tx(OCPP_Call_5_6_DataTransfer_Rx_start))
    def btn_send_message506_2(self):
        asyncio.run(self.websocket_handler_tx(OCPP_Call_5_6_DataTransfer_Rx_stop))
        


    def btn_send_message507(self):
        asyncio.run(self.websocket_handler_tx(OCPP_Call_5_7_GetCompositeSchedule))
    def btn_send_message508(self):
        asyncio.run(self.websocket_handler_tx(OCPP_Call_5_8_GetConfiguration3))
    def btn_send_message509(self):
        asyncio.run(self.websocket_handler_tx(OCPP_Call_5_9_GetDiagnostics))
    def btn_send_message510(self):
        asyncio.run(self.websocket_handler_tx(OCPP_Call_5_10_GetLocalListVersion))
    def btn_send_message511(self):
        asyncio.run(self.websocket_handler_tx(OCPP_Call_5_11_RemoteStartTransaction))
    def btn_send_message512(self):
        asyncio.run(self.websocket_handler_tx(OCPP_Call_5_12_RemoteStopTransaction))
    def btn_send_message513(self):
        asyncio.run(self.websocket_handler_tx(OCPP_Call_5_13_ReserveNow))
    def btn_send_message514(self):
        asyncio.run(self.websocket_handler_tx(OCPP_Call_5_14_Reset))
    def btn_send_message515(self):
        asyncio.run(self.websocket_handler_tx(OCPP_Call_5_15_SendLocalList))
    def btn_send_message516(self):
        asyncio.run(self.websocket_handler_tx(OCPP_Call_5_16_SetChargingProfile1))
    def btn_send_message517(self):
        asyncio.run(self.websocket_handler_tx(OCPP_Call_5_17_TriggerMessage))
    def btn_send_message518(self):
        asyncio.run(self.websocket_handler_tx(OCPP_Call_5_18_UnlockConnector))
    def btn_send_message519(self):
        asyncio.run(self.websocket_handler_tx(OCPP_Call_5_19_UpdateFirmware))
    def alert_window(self,message):
        dlg = QMessageBox(self)
        dlg.setWindowTitle("Alert")
        dlg.setText(message)
        dlg.exec_()
    
    ###################################Component Functions##############################################
    def find_uid(self, input):
        target_c = '\"'
        target_pos = []
        for pos,char in enumerate(input):
            if(char == target_c):
                target_pos.append(pos)
                if(len(target_pos) >= 2):
                    break
        uid = input[target_pos[0]+1:target_pos[1]]
        return uid
    def get_current_time(self):
        currentDateAndTime = datetime.now()
        t = str(currentDateAndTime)
        t = t.replace(' ','T')
        t = t[0:-3]
        t = t + 'Z'
        return t
    def replace_sendcmd(self, sendcmd):
        output = OCPP_Call_5_6_DataTransfer_Rx.replace('replace_sendcmd',sendcmd)
        t = self.get_current_time()
        output = output.replace('DataTransfer_RxID',t)
        return output
    def replace_uid_time(self, input,output):
        uid = self.find_uid(input)
        output = output.replace('ocppuid',uid)
        t = self.get_current_time()
        output = output.replace('ocppcurrentTime',t)
        return output
    def count_time(self):
        global COUNT
        COUNT +=1
        #1、3、7、15、31、63
        COUNT &= TEST_PATTERN_NUM
        return COUNT
    
if __name__ == "__main__":
    app = QApplication(sys.argv)

    # Create the main window
    mainWindow = MainWindow()
    mainWindow.setGeometry(100, 100, 800, 1000)
    # Set the background image of the UI
    mainWindow.setBackgroundImage(IMAGE_PATH)

    mainWindow.show()
    sys.exit(app.exec())
    # app.exec()
