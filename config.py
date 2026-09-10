"""Application configuration."""

import os


class Config:
    """Central configuration loaded from environment variables."""

    SECRET_KEY = os.environ.get("SECRET_KEY", "algobench-dev-key-change-in-production")
    DEBUG = os.environ.get("FLASK_DEBUG", "false").lower() == "true"
    MIN_ARRAY_SIZE = 1
    MAX_ARRAY_SIZE = int(os.environ.get("MAX_ARRAY_SIZE", "150"))
    MAX_ANIMATION_STEPS = int(os.environ.get("MAX_ANIMATION_STEPS", "2500"))
    BENCHMARK_TIMED_RUNS = int(os.environ.get("BENCHMARK_TIMED_RUNS", "3"))
    JSON_SORT_KEYS = False
