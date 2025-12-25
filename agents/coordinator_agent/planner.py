def plan(task: str):
    return [
        {"agent": "research", "task": task},
        {"agent": "automation", "task": task}
    ]
