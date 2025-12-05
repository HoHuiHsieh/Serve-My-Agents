"""Hypercorn configuration file."""

# Server socket
bind = ["0.0.0.0:8000"]

# Worker processes
workers = 4

# Logging
accesslog = "-"
errorlog = "-"
loglevel = "info"

# Performance
worker_class = "asyncio"
keepalive_timeout = 5

# Development settings
# For production, set reload to False
reload = False
