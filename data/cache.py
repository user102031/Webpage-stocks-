"""
Simple in-memory + file-backed cache to avoid hammering yfinance.
TTL-based: each entry expires after a configurable number of seconds.
"""

import json
import os
import time
import hashlib
import logging

logger = logging.getLogger(__name__)

# Directory for persisting cache between restarts
CACHE_DIR = os.path.join(os.path.dirname(__file__), "..", ".cache")
os.makedirs(CACHE_DIR, exist_ok=True)

# In-memory store: {key: {"data": ..., "expires": timestamp}}
_mem_cache: dict = {}

# Default TTLs (seconds)
TTL_QUOTE      = 300        # 5 min  — live price data
TTL_FINANCIALS = 3600 * 6   # 6 hrs  — income statement / balance sheet
TTL_HISTORY    = 3600 * 2   # 2 hrs  — price history
TTL_SCREENER   = 600        # 10 min — screener list
TTL_CALENDAR   = 3600       # 1 hr   — dividend calendar


def _key_to_path(key: str) -> str:
    """Convert cache key to a filesystem-safe path."""
    safe = hashlib.md5(key.encode()).hexdigest()
    return os.path.join(CACHE_DIR, f"{safe}.json")


def get(key: str):
    """Return cached value if it exists and has not expired, else None."""
    # Check memory first
    entry = _mem_cache.get(key)
    if entry and entry["expires"] > time.time():
        return entry["data"]

    # Fall back to disk
    path = _key_to_path(key)
    if os.path.exists(path):
        try:
            with open(path, "r", encoding="utf-8") as f:
                entry = json.load(f)
            if entry["expires"] > time.time():
                # Warm memory cache
                _mem_cache[key] = entry
                return entry["data"]
        except Exception as exc:
            logger.warning("Cache read error for %s: %s", key, exc)

    return None


def set(key: str, data, ttl: int = TTL_QUOTE):
    """Store data in memory and on disk with an expiry timestamp."""
    expires = time.time() + ttl
    entry = {"data": data, "expires": expires}

    # Memory
    _mem_cache[key] = entry

    # Disk
    path = _key_to_path(key)
    try:
        with open(path, "w", encoding="utf-8") as f:
            json.dump(entry, f)
    except Exception as exc:
        logger.warning("Cache write error for %s: %s", key, exc)


def invalidate(key: str):
    """Remove a cache entry."""
    _mem_cache.pop(key, None)
    path = _key_to_path(key)
    if os.path.exists(path):
        try:
            os.remove(path)
        except OSError:
            pass


def clear_expired():
    """Purge all expired entries from memory and disk."""
    now = time.time()
    expired_keys = [k for k, v in _mem_cache.items() if v["expires"] <= now]
    for k in expired_keys:
        del _mem_cache[k]

    for fname in os.listdir(CACHE_DIR):
        fpath = os.path.join(CACHE_DIR, fname)
        try:
            with open(fpath, "r", encoding="utf-8") as f:
                entry = json.load(f)
            if entry["expires"] <= now:
                os.remove(fpath)
        except Exception:
            pass
