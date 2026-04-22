#!/usr/bin/env python3
"""Parse the nlpm-metadata block from a PR body on stdin.

Prints the parsed JSON to stdout, or `{}` if no block is present or the
block's JSON payload is malformed. The regex mirrors SCHEMAS.md
§PR metadata block so there is one authoritative parser.
"""

import json
import re
import sys


def main() -> int:
    body = sys.stdin.read()
    match = re.search(
        r"<!-- nlpm-metadata-begin\s*(\{.*?\})\s*nlpm-metadata-end -->",
        body,
        re.DOTALL,
    )
    if not match:
        print("{}")
        return 0
    try:
        print(json.dumps(json.loads(match.group(1))))
    except json.JSONDecodeError:
        print("{}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
