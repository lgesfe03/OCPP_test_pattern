import sys
import asyncio
import threading
import websockets
# from PySide6.QtCore import *
# from PySide6.QtGui import *
# from PySide6.QtWidgets import *
from PySide6.QtWidgets import QApplication, QMainWindow, QLineEdit, QPushButton, QLabel
from PySide6.QtGui import QPixmap
from PySide6.QtCore import Qt, QThread, Signal

IMAGE_PATH = "..\ico\ocpp16.jpg"
SERVER_IP = "localhost"
# SERVER_IP = "192.168.3.171"
SERVER_PORT = 8080
HeartbeatInterval = 1

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


class MainWindow(QMainWindow):
    #UI initialize
    def __init__(self):
        super().__init__()

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
        self.start_server_button = QPushButton("Start server", self)
        self.start_server_button.setGeometry(10, self.current_height, 200, self.height_arranger(25)) 
        self.start_server_button.clicked.connect(self.start_server)
        # Create a button for sending a WebSocket message
        self.send_message_button = QPushButton("Send message", self)
        self.send_message_button.setGeometry(10, self.current_height, 200, self.height_arranger(25)) 
        self.send_message_button.clicked.connect(self.btn_send_message)
        # Create a label to display the server status
        # Create a label for the welcome message
        self.statuslabel_head = QLabel("Server Status:", self)
        self.statuslabel_head.setGeometry(10, self.current_height, 100, 25)
        self.statuslabel = QLabel("?", self)
        self.statuslabel.setGeometry(110, self.current_height, 200, self.height_arranger(25))
        # Create a label to display the server rx
        self.msglabel = QLabel("info", self)
        self.msglabel.setGeometry(10, self.current_height, 300, self.height_arranger(100))
        # # Create a layout for the address edit and buttons
        # button_layout = QHBoxLayout()
        # button_layout.addWidget(self.host_edit)
        # button_layout.addWidget(self.start_server_button)
        # button_layout.addWidget(self.send_message_button)
        # # Create a widget to hold the address edit and buttons and set it as the central widget of the main window
        # button_widget = QWidget()
        # button_widget.setLayout(button_layout)
        # self.setCentralWidget(button_widget)

        # # Create a text area for displaying messages received from the WebSocket
        # self.message_textarea = QTextEdit()
        # self.message_textarea.setReadOnly(True)
        # self.message_textarea.ensureCursorVisible()
        # # Add the text area to the main window
        # self.addDockWidget(Qt.BottomDockWidgetArea, QDockWidget("Messages", self))
        # # self.findChild(QDockWidget, "Messages").setWidget(self.message_textarea)

    
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
        server_thread = threading.Thread(target=self.start_server_thread)
        server_thread.start()

    def start_server_thread(self):
        self.host = self.host_edit.text()
        self.port = SERVER_PORT  # Change this to the port you want to use
        self.statuslabel.setText("Start Websocket server...")
        asyncio.run(self.websocket_server(self.host, self.port))

    async def websocket_server(self, host, port):
        async with websockets.serve(self.websocket_handler_rx, host, port):
            await asyncio.Future()  # Keep the server running indefinitely

    async def websocket_handler_rx(self, websocket, path):
        self.connected_clients = set()  # Keep track of connected clients
        self.connected_clients.add(websocket)
        async for message in websocket:
            print(f"Received message: {message}")
            # Update the UI with the received message
            # self.message_textarea.append(f"Received message: {message}")
            # display it on the UI
            self.msglabel.setText(message)

    async def websocket_handler_tx(self, message):
        for websocket in self.connected_clients:
            print("connected_clients=",self.connected_clients)
            print("websocket=",websocket)
            await websocket.send(message)
            self.msglabel.setText(message)

    def btn_send_message(self):
        asyncio.run(self.websocket_handler_tx("Hello, clients! from server"))

    # def send_message(self):
    #     # Create a new thread for sending the message and start it
    #     message_thread = threading.Thread(target=self.send_message_thread)
    #     message_thread.start()

    # def send_message_thread(self):
    #     host = self.host_edit.text()
    #     port = SERVER_PORT  # Change this to the port you want to use
    #     asyncio.run(self.send_websocket_message(host, port))

    # async def send_websocket_message(self, host, port):
    #     async with websockets.connect(f"ws://{host}:{port}") as websocket:
    #         message = "Hello, world!"
    #         await websocket.send(message)
    #         print(f"Sent message: {message}")
    #         # Update the UI with the sent message
    #         # self.message_textarea.append(f"Sent message: {message}")

if __name__ == "__main__":
    app = QApplication(sys.argv)

    # Create the main window
    mainWindow = MainWindow()
    mainWindow.setGeometry(100, 100, 800, 600)
    # Set the background image of the UI
    mainWindow.setBackgroundImage(IMAGE_PATH)

    mainWindow.show()
    sys.exit(app.exec())
    # app.exec()
