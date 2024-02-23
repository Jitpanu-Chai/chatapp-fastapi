from fastapi import FastAPI,WebSocket,WebSocketDisconnect,Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.middleware.cors import CORSMiddleware
from datetime import datetime
import json
from typing import List
import uvicorn

app = FastAPI()

origins = [
    "http://localhost.tiangolo.com",
    "https://localhost.tiangolo.com",
    "http://localhost",
    "http://localhost:8080",
    "http://127.0.0.1:8000"
]

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

#connecte user
connected_users = {}

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # can alter with time
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def main():
    return {"message": "Hello World"}

@app.get("/chat")
async def home(request: Request):
    return templates.TemplateResponse(
        request=request, name="index.html"
    )

@app.websocket("/v1/{user_id}")
async def websocket_endpoints(user_id: str, websocket: WebSocket):
    await websocket.accept()

    # Store the WebSocket connection in the dictionary
    connected_users[user_id] = websocket
    try:
        while True:
            data = await websocket.receive_text()
            #send the recive data to other user including self
            for user,user_ws in connected_users.items():
                # if user != user_id:
                await user_ws.send_text(data)
    except:
        # If a user disconnects, remove them from the dictionary
        del connected_users[user_id]
        await websocket.close()

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)