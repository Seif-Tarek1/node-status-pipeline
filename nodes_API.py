from fastapi import FastAPI
from random import randint, uniform, choice
from datetime import datetime, timedelta
import uvicorn

app = FastAPI()

NODES = [f"Node-{i}" for i in range(1, 1001)]

LOCATIONS = ["cairo", "alexandria", "dubai"]
TYPES = ["router", "switch"]

# Cache latency per node so status stays consistent
LATENCY_CACHE = {}


@app.get("/nodes")
def get_nodes():
    return [
        {
            "node_id": node,
            "location": choice(LOCATIONS),
            "type": choice(TYPES),
        }
        for node in NODES
    ]


@app.get("/latency")
def get_latency():
    global LATENCY_CACHE
    LATENCY_CACHE = {
        node: round(uniform(10, 400), 2) for node in NODES
    }
    return [
        {
            "node_id": node,
            "latency_mn": LATENCY_CACHE[node]
        }
        for node in NODES
    ]


@app.get("/status")
def get_status():
    def status_from_latency(latency):
        if latency < 100:
            return "up"
        elif latency < 250:
            return "degraded"
        else:
            return "down"

    if not LATENCY_CACHE:
        # Ensure latency values exist
        for node in NODES:
            LATENCY_CACHE[node] = round(uniform(10, 400), 2)

    return [
        {
            "node_id": node,
            "status": status_from_latency(LATENCY_CACHE[node]),
            "last_checked": (datetime.now() - timedelta(minutes=randint(0, 60))).isoformat(),
        }
        for node in NODES
    ]


if __name__ == "__main__":
    uvicorn.run("nodes_API:app", host="0.0.0.0", port=4039, reload=True)
