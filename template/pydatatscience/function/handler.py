import json
import os

# from .core import utils


function_root = os.environ.get("function_root")


def handle(req: bytes) -> str:
    """handle a request to the function
    Args:
        req (bytes): request body
    """

    return json.dumps({"echo": req.decode('utf-8')})
