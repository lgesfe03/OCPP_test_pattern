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
        self.send_message_button.clicked.connect(self.send_message)
        # Create a label to display the entered IPv4 data
        self.msglabel = QLabel(self)
        self.msglabel.setGeometry(10, self.current_height, 100, self.height_arranger(25))

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
        host = self.host_edit.text()
        port = 8080  # Change this to the port you want to use
        asyncio.run(self.websocket_server(host, port))

    async def websocket_server(self, host, port):
        async with websockets.serve(self.websocket_handler, host, port):
            await asyncio.Future()  # Keep the server running indefinitely

    async def websocket_handler(self, websocket, path):
        async for message in websocket:
            print(f"Received message: {message}")
            # Update the UI with the received message
            # self.message_textarea.append(f"Received message: {message}")
            # Read the entered IPv4 data and display it on the UI
            ws_rx = self.msglabel.text()
            self.msglabel.setText(ws_rx)

    def send_message(self):
        # Create a new thread for sending the message and start it
        message_thread = threading.Thread(target=self.send_message_thread)
        message_thread.start()

    def send_message_thread(self):
        host = self.host_edit.text()
        port = 8765  # Change this to the port you want to use
        asyncio.run(self.send_websocket_message(host, port))

    async def send_websocket_message(self, host, port):
        async with websockets.connect(f"ws://{host}:{port}") as websocket:
            message = "Hello, world!"
            await websocket.send(message)
            print(f"Sent message: {message}")
            # Update the UI with the sent message
            self.message_textarea.append(f"Sent message: {message}")

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
