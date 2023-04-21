import asyncio
import websockets
import sys
from PySide6.QtCore import QThread, QObject, Signal, Slot
from PySide6.QtWidgets import QApplication, QMainWindow, QTextEdit, QPushButton, QVBoxLayout, QWidget


class WebSocketServer(QObject):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.running = False
        self.connections = set()

    async def handle_websocket(self, websocket, path):
        self.connections.add(websocket)
        try:
            async for message in websocket:
                print(f"Received message from {websocket.remote_address[0]}: {message}")
        except websockets.exceptions.ConnectionClosedError:
            pass
        self.connections.remove(websocket)

    async def start_server(self):
        self.running = True
        async with websockets.serve(self.handle_websocket, "192.168.3.171", 8080):
            await asyncio.Future()

    async def stop_server(self):
        self.running = False
        tasks = [connection.close() for connection in self.connections]
        await asyncio.gather(*tasks)


class ServerThread(QThread):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.websocket_server = WebSocketServer()

    def run(self):
        asyncio.run(self.websocket_server.start_server())

    async def stop(self):
        await self.websocket_server.stop_server()


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.text_edit = QTextEdit(self)
        self.text_edit.setReadOnly(True)
        self.start_button = QPushButton("Start WebSocket Server", self)
        self.stop_button = QPushButton("Stop WebSocket Server", self)
        # self.stop_button.setEnabled(False)

        self.server_thread = ServerThread()
        self.start_button.clicked.connect(self.server_thread.start)
        self.stop_button.clicked.connect(self.stop_server)

        central_widget = QWidget()
        layout = QVBoxLayout(central_widget)
        layout.addWidget(self.text_edit)
        layout.addWidget(self.start_button)
        layout.addWidget(self.stop_button)
        self.setCentralWidget(central_widget)

    @Slot()
    async def stop_server(self):
        await self.server_thread.stop()
        await self.btn_disconnect()
        self.display_message("Stopped WebSocket server.")

    @Slot(str)
    def display_message(self, message):
        self.text_edit.append(message)

    async def btn_disconnect(self):
        self.server_thread.terminate()


if __name__ == "__main__":
    app = QApplication()
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
