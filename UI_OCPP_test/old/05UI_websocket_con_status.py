import asyncio
import websockets
from PySide6.QtCore import QThread, QObject, Signal, Slot
from PySide6.QtGui import QTextCursor
from PySide6.QtWidgets import QApplication, QMainWindow, QTextEdit, QPushButton, QLabel


class WebSocketServer(QObject):
    client_connected = Signal(str)
    client_disconnected = Signal()

    async def handle_websocket(self, websocket, path):
        self.client_connected.emit(f"Client connected: {websocket.remote_address[0]}")
        try:
            async for message in websocket:
                print(f"Received message from {websocket.remote_address[0]}: {message}")
        except websockets.exceptions.ConnectionClosedError:
            pass
        finally:
            self.client_disconnected.emit()

    async def start_server(self):
        async with websockets.serve(self.handle_websocket, "localhost", 8765):
            await asyncio.Future()


class ServerThread(QThread):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.websocket_server = WebSocketServer()

    def run(self):
        asyncio.run(self.websocket_server.start_server())


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.connected_label = QLabel("WebSocket server not started", self)
        self.client_label = QLabel("No client connected", self)
        self.text_edit = QTextEdit(self)
        self.text_edit.setReadOnly(True)
        self.start_button = QPushButton("Start WebSocket Server", self)
        self.disconnect_button = QPushButton("Disconnect Client", self)
        self.disconnect_button.setEnabled(False)

        self.server_thread = ServerThread()
        self.server_thread.websocket_server.client_connected.connect(self.update_connected_label)
        self.server_thread.websocket_server.client_disconnected.connect(self.update_disconnected_label)

        self.start_button.clicked.connect(self.server_thread.start)
        self.disconnect_button.clicked.connect(self.disconnect_client)

        central_widget = self.text_edit.parentWidget()
        central_widget.layout().addWidget(self.start_button)
        central_widget.layout().addWidget(self.disconnect_button)
        central_widget.layout().addWidget(self.connected_label)
        central_widget.layout().addWidget(self.client_label)

    @Slot(str)
    def update_connected_label(self, message):
        self.connected_label.setText(f"WebSocket server running on {message}")
        self.client_label.setText(f"Client connected: {message.split(': ')[1]}")
        self.disconnect_button.setEnabled(True)

    @Slot()
    def update_disconnected_label(self):
        self.connected_label.setText("WebSocket server not started")
        self.client_label.setText("No client connected")
        self.disconnect_button.setEnabled(False)

    @Slot()
    def disconnect_client(self):
        # You can modify this code to disconnect a specific client
        for task in asyncio.all_tasks():
            if "handle_websocket" in str(task):
                task.cancel()
                break

    @Slot(str)
    def display_message(self, message):
        cursor = self.text_edit.textCursor()
        cursor.movePosition(QTextCursor.End)
        cursor.insertText(message + "\n")
        self.text_edit.setTextCursor(cursor)


if __name__ == "__main__":
    app = QApplication()
    window = MainWindow()
    window.show()
    app.exec_()
