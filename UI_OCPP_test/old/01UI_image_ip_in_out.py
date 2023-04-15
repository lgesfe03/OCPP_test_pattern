import sys
from PySide6.QtWidgets import QApplication, QMainWindow, QLineEdit, QPushButton, QLabel
from PySide6.QtGui import QPixmap
from PySide6.QtCore import Qt, QThread, Signal
from websockets import serve
import threading
import asyncio

IMAGE_PATH = "..\..\ico\ocpp16.jpg"

class CounterThread(QThread):
    countChanged = Signal(int)

    def run(self):
        for i in range(1, 101):
            self.countChanged.emit(i)
            self.msleep(1000)

class WebSocketServerThread(QThread):
    messageReceived = Signal(str)
    async def start_server(self,host, port):
        async with serve(self.handle_connection, host, port):
            await asyncio.Future()  # Keep the server running indefinitely

    async def handle_connection(self, websocket, path):
        async for message in websocket:
            print(f"Received message: {message}")
            # Update the UI with the received message
            self.message_textarea.append(f"Received message: {message}")
            # When a message is received, emit a signal with the message data
            self.messageReceived.emit(message)
    
    def run(self):
        asyncio.run(self.start_server())

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("OCPP 1.6 Test Tool")
        self.current_height = 0
        # Create a label to display the background image
        self.backgroundLabel = QLabel(self)
        self.backgroundLabel.setScaledContents(True)
        self.backgroundLabel.setGeometry(10, self.current_height, 200, self.height_arranger(150)) 

        # Create a label for the welcome message
        self.welcomeLabel = QLabel("Type IPv4 below and click \"Start Server\"", self)
        # self.welcomeLabel.setAlignment(Qt.AlignCenter)
        self.welcomeLabel.setGeometry(10, self.current_height, 800, self.height_arranger(25))

        # Create a QLineEdit for the user to enter an IPv4 address
        self.ipLineEdit = QLineEdit(self)
        self.ipLineEdit.setGeometry(10, self.current_height, 200, self.height_arranger(25)) 

        # Create a button to read the entered IPv4 data and print it out
        self.printIpButton = QPushButton("Print IPv4", self)
        self.printIpButton.setGeometry(10, self.current_height, 100, self.height_arranger(25))
        self.printIpButton.clicked.connect(self.printIpv4)
        # Create a label to display the entered IPv4 data
        self.ipLabel = QLabel(self)
        self.ipLabel.setGeometry(10, self.current_height, 100, self.height_arranger(25))

        # Create a button to start the counting thread
        self.countButton = QPushButton("Start Serverold", self)
        self.countButton.setGeometry(10, self.current_height, 100, self.height_arranger(25))
        self.countButton.clicked.connect(self.startServer)


    def height_arranger(self, height):
        self.current_height += height + 10
        return height

    def printIpv4(self):
        # Read the entered IPv4 data and display it on the UI
        ipv4 = self.ipLineEdit.text()
        self.ipLabel.setText(ipv4)

    def startServer(self):
        # Create a thread to count from 1 to 100
        self.thread = CounterThread()
        self.thread.countChanged.connect(self.updateCount)
        # Start the thread
        self.thread.start()

    def updateCount(self, count):
        # Update the button text with the current count
        self.countButton.setText(str(count))



    def setBackgroundImage(self, imagePath):
        # Set the background image of the UI
        pixmap = QPixmap(imagePath)
        self.backgroundLabel.setPixmap(pixmap)


if __name__ == '__main__':
    app = QApplication(sys.argv)

    # Create the main window
    mainWindow = MainWindow()
    mainWindow.setGeometry(100, 100, 800, 600)

    # Set the background image of the UI
    mainWindow.setBackgroundImage(IMAGE_PATH)

    # Show the main window
    mainWindow.show()

    sys.exit(app.exec())
