import json
from agents import AGENTS
from llm import call_llm

MEMORY_FILE = "memory.json"

def load_memory():
    try:
        with open(MEMORY_FILE, "r") as f:
            return json.load(f)
    except:
        return {}

def save_memory(data):
    with open(MEMORY_FILE, "w") as f:
        json.dump(data, f, indent=2)


AGENT_PROMPTS = {
    "research_agent": "Collect factual information and bullet points.",
    "analysis_agent": "Analyze information and extract insights.",
    "writer_agent": "Write a clear, structured response.",
    "review_agent": "Improve clarity, correctness, and tone."
}

def run_pipeline(topic):
    memory = load_memory()
    memory["topic"] = topic

    for agent_name, meta in AGENTS.items():
        input_data = memory.get(meta["input"], topic)

        output = call_llm(
            system_prompt=AGENT_PROMPTS[agent_name],
            user_prompt=str(input_data)
        )

        memory[meta["output"]] = output
        save_memory(memory)

    return memory


if __name__ == "__main__":
    run_pipeline("agentic AI fundamentals")
