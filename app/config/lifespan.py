import asyncio
import tracemalloc
import linecache
from fastapi import FastAPI
from contextlib import asynccontextmanager

from app.config.logger_setup import logger_manager
from app.config.metrics_setup import mm

logger = logger_manager.get_logger()

tracemalloc.start()


def log_metrics(memory_usage):
    mm.histogram_record(memory_usage)


def display_top(snapshot, key_type='lineno', limit=10):
    snapshot = snapshot.filter_traces((
        tracemalloc.Filter(False, "<frozen importlib._bootstrap>"),
        tracemalloc.Filter(False, "<unknown>"),
    ))
    top_stats = snapshot.statistics(key_type)

    lines = []
    for index, stat in enumerate(top_stats[:limit], 1):
        frame = stat.traceback[0]
        line = linecache.getline(frame.filename, frame.lineno).strip()
        lines.append(f"#{index}: {frame.filename}:{frame.lineno}: {stat.size / 1024:.1f} KiB - {line}")
    return lines


async def log_memory_objects():
    while True:
        snapshot = tracemalloc.take_snapshot()
        top_lines = display_top(snapshot)
        total_memory_usage = sum(stat.size for stat in snapshot.statistics('traceback')) / 1024  # size in KiB
        for line in top_lines:
            logger.info(line)

        # Logging the total memory usage to both logger and metrics
        logger.info(f"Total memory usage: {total_memory_usage:.1f} KiB")
        log_metrics(total_memory_usage)  # Send total memory usage to your metrics

        # Clear the linecache to prevent memory buildup
        linecache.clearcache()
        logger.info("Linecache cleared to free memory.")
        await asyncio.sleep(60)  # every 1 minutes


@asynccontextmanager
async def lifespan(app: FastAPI):
    task = asyncio.create_task(log_memory_objects())
    yield
    task.cancel()  # Signal the task to cancel
    try:
        await task
    except asyncio.CancelledError:
        logger.info("Memory logging task was cancelled")
    except Exception as e:
        logger.error(f"An error occurred while cancelling the task: {str(e)}")
