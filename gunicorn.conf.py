# gunicorn.conf.py
import os
import multiprocessing

# Bind to the platform-provided port, fallback to 8080
port = os.environ.get("PORT", "8080")
bind = f"0.0.0.0:{port}"

# Workers
num_cpus = multiprocessing.cpu_count()
workers = (num_cpus * 2) + 1

# Use Uvicorn worker for ASGI apps
worker_class = "uvicorn.workers.UvicornWorker"

# Timeouts and request handling
timeout = 230
max_requests = 1000
max_requests_jitter = 50

# Logging to stdout/stderr
log_file = "-"
accesslog = "-"
errorlog = "-"

# Optional: tune keepalive if behind a load balancer
keepalive = 2