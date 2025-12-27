from worker import worker_loop
import asyncio

if __name__ == "__main__":
    asyncio.run(worker_loop())
