
import logging
from pathlib import Path

LOG_DIR = Path(__file__).resolve().parent / "logs"
LOG_DIR.mkdir(exist_ok=True)

logger = logging.getLogger("authorization_audit")
logger.setLevel(logging.INFO)
logger.propagate = False

if not logger.handlers:
    handler = logging.FileHandler(
        LOG_DIR / "authorization.log",
        encoding="utf-8",
    )

    handler.setFormatter(
        logging.Formatter("%(asctime)s %(message)s")
    )

    logger.addHandler(handler)


def log_access(user_id, role, action, resource, decision):
    logger.info(
        "user_id=%s role=%s action=%s resource=%s decision=%s",
        user_id,
        role,
        action,
        resource,
        decision,
    )
