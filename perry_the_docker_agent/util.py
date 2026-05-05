import logging
import os
import socket
import time

import colorlog

log_level = os.environ.get("PERRY_LOG_LEVEL", "INFO")
logger = logging.getLogger("perry")
logger.setLevel(getattr(logging, log_level))
logFormatter = colorlog.ColoredFormatter(
    fmt="%(log_color)s%(name)s :: %(levelname)-8s :: %(message)s"
)
handler = logging.StreamHandler()
handler.setFormatter(logFormatter)
logger.addHandler(handler)


def is_port_open(ip, port, timeout=2):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(timeout)
    result = sock.connect_ex((ip, port))
    return result == 0


def wait_until_port_is_open(ip, port, sleep_time=3, max_attempts=10):
    attempts = 0
    while not is_port_open(ip, port):
        attempts += 1
        if attempts >= max_attempts:
            raise RuntimeError(f"{ip}:{port} has not opened")
        time.sleep(sleep_time)
