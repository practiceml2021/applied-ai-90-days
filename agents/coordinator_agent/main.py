from planner import plan
from executor import execute

if __name__ == "__main__":
    task = input("Enter task: ")

    steps = plan(task)
    results = execute(steps)

    print("\n--- Final Results ---")
    for r in results:
        print(r)
