import asyncio
import websockets
import json
import ssl

async def test_websocket():
    uri = "wss://localhost:65535/ws/general/"
    ssl_context = ssl._create_unverified_context()  # Disable SSL verification

    async with websockets.connect(uri, ssl=ssl_context) as websocket:
        print("WebSocket connection opened")

        async def send_ping():
            while True:
                await websocket.send(json.dumps({"type": "ping"}))
                print("Ping sent")
                await asyncio.sleep(1)

        async def receive_messages():
            async for message in websocket:
                print(f"Message received: {message}")

        await asyncio.gather(send_ping(), receive_messages())

if __name__ == "__main__":
    asyncio.run(test_websocket())