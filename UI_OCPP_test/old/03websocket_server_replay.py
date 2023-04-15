import asyncio
import threading
import websockets

connected_clients = set()  # Keep track of connected clients

# Start a WebSocket server on the specified host and port
async def websocket_server(host, port):
    async with websockets.serve(websocket_handler, host, port):
        await asyncio.Future()  # Keep the server running indefinitely

# Handle incoming WebSocket messages
async def websocket_handler(websocket, path):
    connected_clients.add(websocket)
    async for message in websocket:
        print(f"Received message: {message}")
        # Send a reply to the client
        await websocket.send("Received message: " + message)

# Send a WebSocket message to all connected clients
async def send_websocket_message(message):
    for websocket in connected_clients:
        await websocket.send(message)
        print(f"Sent message: {message}")

# Create a new thread for the WebSocket server and start it
server_thread = threading.Thread(target=asyncio.run, args=(websocket_server("localhost", 8080),))
server_thread.start()

# Create a window with a button for sending a message
import tkinter as tk

def send_message():
    asyncio.run(send_websocket_message("Hello, clients!"))

root = tk.Tk()
button = tk.Button(root, text="Send message", command=send_message)
button.pack()
root.mainloop()
