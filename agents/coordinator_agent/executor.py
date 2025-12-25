def execute(plan_steps):
    results = []

    for step in plan_steps:
        agent = step["agent"]
        task = step["task"]

        try:
            if agent == "research":
                result = f"Research result for: {task}"
            elif agent == "automation":
                result = f"Automation decision for: {task}"
            else:
                result = "Unknown agent"

            results.append({
                "agent": agent,
                "status": "success",
                "output": result
            })

        except Exception as e:
            results.append({
                "agent": agent,
                "status": "failed",
                "error": str(e)
            })

    return results
