from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import random

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

NUM_SATS = 3
CONTROL_GAIN = 0.05
BASE_DISTURBANCE = 0.5

swarm_enabled = True

# CubeSat state (orientation only – idea stage)
sats = [
    {
        "id": i,
        "roll": random.uniform(-40, 40),
        "pitch": random.uniform(-40, 40),
        "yaw": random.uniform(-40, 40)
    }
    for i in range(NUM_SATS)
]

def simulate_step():
    global sats

    if swarm_enabled:
        avg_roll = sum(s["roll"] for s in sats) / NUM_SATS
        avg_pitch = sum(s["pitch"] for s in sats) / NUM_SATS
        avg_yaw = sum(s["yaw"] for s in sats) / NUM_SATS

    for s in sats:
        # disturbance (environmental effects)
        s["roll"] += random.uniform(-BASE_DISTURBANCE, BASE_DISTURBANCE)
        s["pitch"] += random.uniform(-BASE_DISTURBANCE, BASE_DISTURBANCE)
        s["yaw"] += random.uniform(-BASE_DISTURBANCE, BASE_DISTURBANCE)

        # bio-inspired swarm alignment
        if swarm_enabled:
            s["roll"] -= CONTROL_GAIN * (s["roll"] - avg_roll)
            s["pitch"] -= CONTROL_GAIN * (s["pitch"] - avg_pitch)
            s["yaw"] -= CONTROL_GAIN * (s["yaw"] - avg_yaw)

@app.get("/telemetry")
def telemetry():
    simulate_step()
    return sats

@app.post("/toggle-swarm")
def toggle_swarm():
    global swarm_enabled
    swarm_enabled = not swarm_enabled
    return {"swarm_enabled": swarm_enabled}

@app.post("/add-disturbance")
def add_disturbance():
    for s in sats:
        s["roll"] += random.uniform(-30, 30)
        s["pitch"] += random.uniform(-30, 30)
        s["yaw"] += random.uniform(-30, 30)
    return {"status": "disturbance injected"}

