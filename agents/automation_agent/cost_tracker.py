import json

COST_FILE = "state/costs.json"

def record_cost(service: str, amount: float):
    with open(COST_FILE, "r") as f:
        data = json.load(f)

    data[service] = round(data.get(service, 0) + amount, 4)

    with open(COST_FILE, "w") as f:
        json.dump(data, f, indent=2)
