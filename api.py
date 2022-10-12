from convoy import Convoy
from fastapi import FastAPI

from events import events
from config import Settings
from model import WebhookData

app = FastAPI()
config = Settings()

todos = []

webhook_receiver = config.WEBHOOK_RECEIVER_URL
convoy = Convoy({"api_key": config.CONVOY_API_KEY})
app_id = config.CONVOY_APP_ID

def send_webhook_event(event_type: str):
    
    event = {
        "app_id": app_id,
        "event_type": event_type,
        "data": events[event_type]
    }
    
    (res, err) = convoy.event.create({}, event)
    return res

@app.get("/")
async def ping():
    send_webhook_event("ping")
    return {"message": "Wilkomen!"}

@app.get("/todo", tags=["todos"])
async def get_todos() -> dict:
    send_webhook_event("retrieved")
    return { "data": todos }


@app.post("/todo", tags=["todos"])
async def add_todo(todo: dict) -> dict:
    todos.append(todo)
    send_webhook_event("created")
    return {
        "data": { "Todo added." }
    }


@app.put("/todo/{id}", tags=["todos"])
async def update_todo(id: int, body: dict) -> dict:
    for todo in todos:
        if int(todo["id"]) == id:
            todo["item"] = body["item"]
            send_webhook_event("updated")
            return {
                "data": f"Todo with id {id} has been updated."
            }
    send_webhook_event("failed")
    return {
        "data": f"Todo with id {id} not found."
    }


@app.delete("/todo/{id}", tags=["todos"])
async def delete_todo(id: int) -> dict:
    for todo in todos:
        if int(todo["id"]) == id:
            todos.remove(todo)
            send_webhook_event("deleted")
            return {
                "data": f"Todo with id {id} has been removed."
            }

    send_webhook_event("failed")
    return {
        "data": f"Todo with id {id} not found."
    }
    
# Endpoint for event deliveries.
    
@app.post("/event", response_model=WebhookData)
async def receive_event(event: WebhookData):
    return event
