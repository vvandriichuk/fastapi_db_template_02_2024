import os
import asyncio
from typing import List
import tracemalloc
import linecache
from fastapi import FastAPI
from contextlib import asynccontextmanager

from app.config.logger_setup import logger_manager
from app.config.metrics_setup import mm

interval = int(os.getenv("LOG_INTERVAL", "60"))
limit = int(os.getenv("LOG_LIMIT", "10"))
key_type = os.getenv("LOG_KEY_TYPE", "lineno")

logger = logger_manager.get_logger()

tracemalloc.start()


def log_metrics(memory_usage):
    mm.histogram_record(memory_usage)


def display_top(snapshot: tracemalloc.Snapshot, key_type: str = 'lineno', limit: int = 10) -> List[str]:
    snapshot = snapshot.filter_traces((
        tracemalloc.Filter(False, "<frozen importlib._bootstrap>"),
        tracemalloc.Filter(False, "<unknown>"),
    ))
    top_stats = snapshot.statistics(key_type)

    lines: List[str] = []
    for index, stat in enumerate(top_stats[:limit], 1):
        frame = stat.traceback[0]
        line = linecache.getline(frame.filename, frame.lineno).strip()
        lines.append(f"#{index}: {frame.filename}:{frame.lineno}: {stat.size / 1024:.1f} KiB - {line}")
    return lines


async def log_memory_objects(interval: int = 60, limit: int = 10, key_type: str = 'lineno'):
    while True:
        snapshot = tracemalloc.take_snapshot()
        top_lines = display_top(snapshot, key_type=key_type, limit=limit)
        statistics = snapshot.statistics('traceback')
        total_memory_usage = sum(stat.size for stat in statistics) / 1024 if statistics else 0  # size in KiB
        for line in top_lines:
            logger.info(line)

        # Logging the total memory usage to both logger and metrics
        logger.info(f"Total memory usage: {total_memory_usage:.1f} KiB")
        log_metrics(total_memory_usage)

        # Clear the linecache to prevent memory buildup
        linecache.clearcache()
        logger.info("Linecache cleared to free memory.")
        await asyncio.sleep(interval)  # Pause execution for 60 seconds


@asynccontextmanager
async def lifespan(app: FastAPI):
    task = asyncio.create_task(log_memory_objects(interval=interval, limit=limit, key_type=key_type))
    yield
    task.cancel()
    try:
        await task
    except asyncio.CancelledError:
        logger.info("Memory logging task was cancelled")
    except Exception as e:
        logger.error(f"An error occurred while cancelling the task: {str(e)}")

