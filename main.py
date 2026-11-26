"""FastAPI application for the DevOps TP3 project."""
import socket

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()


@app.get("/")
def read_root():
    """Return the welcome message."""
    return {"message": "it works!"}


@app.get("/addition")
def addition(a: float, b: float):
    """Add two numbers."""
    return {"result": a + b}


def home():
    """Return the home message."""
    return {"message": "it works!"}


@app.get("/greeting")
def greeting(name: str):
    """Return a greeting with the computer hostname and IP address."""
    hostname = socket.gethostname()

    ip = "Unavailable"
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    try:
        sock.connect(("8.8.8.8", 80))
        ip = sock.getsockname()[0]
    except OSError:
        pass
    finally:
        sock.close()

    return {
        "message": f"Hello, {name}",
        "developer": "Dev2",
        "hostname": hostname,
        "IP": ip
    }


class Numbers(BaseModel):
    """Represent two numbers for multiplication."""
    a: float
    b: float


@app.post("/multiply")
def multiply(numbers: Numbers):
    """Multiply two numbers."""
    return {
        "result": numbers.a * numbers.b,
        "developper": "Dev1"
    }


class DivideRequest(BaseModel):
    """Represent two numbers for division."""
    a: float
    b: float


@app.post("/divide")
def divide(payload: DivideRequest):
    """Divide two numbers and prevent division by zero."""
    if payload.b == 0:
        raise HTTPException(
            status_code=400,
            detail="Division by zero is not allowed"
        )

    return {"result": payload.a / payload.b}


@app.delete("/remove/{item_id}")
def remove_item(item_id: int):
    """Remove an item using its ID."""
    return {"message": f"Item {item_id} removed"}


@app.get("/soustraction")
def soustraction(a: float, b: float):
    """Subtract the second number from the first."""
    return {"result": a - b}


class UpdateRequest(BaseModel):
    """Represent the data required to update an item."""
    name: str
    value: float


# Simulated in-memory database
items_db: dict[int, dict] = {
    1: {"name": "item1", "value": 10.0},
    2: {"name": "item2", "value": 20.0},
}


@app.put("/update/{item_id}")
def update_item(item_id: int, payload: UpdateRequest):
    """Update an existing item."""
    if item_id not in items_db:
        raise HTTPException(status_code=404, detail="Item not found")

    items_db[item_id] = {
        "name": payload.name,
        "value": payload.value
    }

    return {"id": item_id, "item": items_db[item_id]}
