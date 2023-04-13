import sys
from PySide6.QtWidgets import QApplication, QMainWindow, QLineEdit, QPushButton, QLabel
from PySide6.QtGui import QPixmap
from PySide6.QtCore import Qt, QThread, Signal


class CounterThread(QThread):
    countChanged = Signal(int)

    def run(self):
        for i in range(1, 101):
            self.countChanged.emit(i)
            self.msleep(1000)


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("IPv4 and Counting Thread")

        # Create a label for the welcome message
        self.welcomeLabel = QLabel("Welcome to the IPv4 and Counting Thread UI!", self)
        self.welcomeLabel.setAlignment(Qt.AlignCenter)
        self.welcomeLabel.setGeometry(0, 0, 800, 50)

        # Create a label to display the background image
        self.backgroundLabel = QLabel(self)
        self.backgroundLabel.setScaledContents(True)
        self.backgroundLabel.setGeometry(0, 0, 800, 600)

        # Create a QLineEdit for the user to enter an IPv4 address
        self.ipLineEdit = QLineEdit(self)
        self.ipLineEdit.setGeometry(300, 150, 200, 25)

        # Create a button to read the entered IPv4 data and print it out
        self.printIpButton = QPushButton("Print IPv4", self)
        self.printIpButton.setGeometry(325, 200, 150, 25)
        self.printIpButton.clicked.connect(self.printIpv4)

        # Create a label to display the entered IPv4 data
        self.ipLabel = QLabel(self)
        self.ipLabel.setGeometry(350, 240, 100, 25)

        # Create a button to start the counting thread
        self.countButton = QPushButton("Start Counting", self)
        self.countButton.setGeometry(350, 300, 100, 50)
        self.countButton.clicked.connect(self.startCounting)

    def printIpv4(self):
        # Read the entered IPv4 data and display it on the UI
        ipv4 = self.ipLineEdit.text()
        self.ipLabel.setText(ipv4)

    def startCounting(self):
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
    mainWindow.setBackgroundImage("path/to/your/image.jpg")

    # Show the main window
    mainWindow.show()

    sys.exit(app.exec())
