from fastapi import FastAPI
import requests
import json

from config import Settings

app = FastAPI()

todos = []
webhook_receiver = Settings().WEBHOOK_RECEIVER_URL


def send_webhook_event(event_type: str):
    events = {
        "ping": {
            "event": "ping",
            "description": "Webhook test from application."
        },
        "created": {
            "event": "todo.created",
            "description": "Todo created successfully"
        },
        "retrieved": {
            "event": "todo.retrieved",
            "description": "Todo retrieved successfully"
        },
        "updated": {
            "event": "todo.updated",
            "description": "Todo updated successfully"
        },
        "deleted": {
            "event": "todo.deleted",
            "description": "Todo deleted successfully"
        },
        "failed": {
            "event": "todo.failure",
            "description": "Todo not found."
        }
    }
    
    event = {
        "event_type": event_type,
        "data": events[event_type]
    }
    
    request = requests.post(webhook_receiver, data=json.dumps(event), headers={
        "Content-type": "application/json"
    })
    return

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