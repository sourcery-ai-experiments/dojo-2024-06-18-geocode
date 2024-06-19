# from https://replit.com/@ControlAltPete/Hacker-Dojo-Python-Meetup#speed-compare.py
import asyncio
import time
from collections.abc import Callable
from concurrent.futures import ProcessPoolExecutor, ThreadPoolExecutor
from typing import Any

import aiohttp
import requests
from aiohttp import ClientSession

URL = "https://jsonplaceholder.typicode.com/posts"

NUM_REQUESTS = 100


# Synchronous function to make a request
def fetch_sync(url: str) -> list[dict[str, str | int]]:
    response = requests.get(url)
    json = list(response.json())
    for d in json:
        assert ["userId", "id", "title", "body"] == list(d.keys())
        for v in d.values():
            assert isinstance(v, (str, int))
        assert d["userId"] <= 10, d
        assert d["id"] <= 100, d
    return json


# Asynchronous function to make a request
async def fetch_async(session: ClientSession, url: str) -> Any:
    async with session.get(url) as response:
        return await response.json()


# Function to make requests using asyncio
async def fetch_all_async() -> Any:
    async with aiohttp.ClientSession() as session:
        tasks = [fetch_async(session, URL) for _ in range(NUM_REQUESTS)]
        return await asyncio.gather(*tasks)


# Function to make requests using threading
def fetch_all_threading() -> list[list[dict[str, str | int]]]:
    with ThreadPoolExecutor() as executor:
        futures = [executor.submit(fetch_sync, URL) for _ in range(NUM_REQUESTS)]
        return [future.result() for future in futures]


# Function to make requests using multiprocessing
def fetch_all_multiprocessing() -> list[list[dict[str, str | int]]]:
    with ProcessPoolExecutor() as executor:
        futures = [executor.submit(fetch_sync, URL) for _ in range(NUM_REQUESTS)]
        return [future.result() for future in futures]


def measure_time(
    func: Callable[[], list[list[dict[str, str | int]]]]
) -> tuple[float, Any]:
    start_time = time.time()
    result = func()
    duration = time.time() - start_time
    tot = total(result)
    assert 1_055_000 == tot, tot
    return duration, result


def total(responses: list[list[dict[str, str | int]]]) -> float:
    acc = 0.0
    assert NUM_REQUESTS == len(responses)
    for response in responses:
        assert 100 == len(response), len(response)
        for d in response:
            acc += int(d["userId"]) / 0.1
            acc += int(d["id"])
    return acc


def main() -> None:
    print("Starting synchronous requests...")
    duration_sync, _ = measure_time(
        lambda: [fetch_sync(URL) for _ in range(NUM_REQUESTS)]
    )
    print(f"Synchronous: {duration_sync:.2f} seconds")

    print("Starting asyncio requests...")
    duration_async, _ = measure_time(lambda: asyncio.run(fetch_all_async()))
    print(f"Asyncio: {duration_async:.2f} seconds")

    print("Starting threading requests...")
    duration_threading, _ = measure_time(fetch_all_threading)
    print(f"Threading: {duration_threading:.2f} seconds")

    print("Starting multiprocessing requests...")
    duration_multiprocessing, _ = measure_time(fetch_all_multiprocessing)
    print(f"Multiprocessing: {duration_multiprocessing:.2f} seconds")


if __name__ == "__main__":
    main()
