from __future__ import print_function

import sys
from argparse import ArgumentParser
from ast import literal_eval
from os import environ as env


def literalenv(args):
    try:
        val = env[args.env_var]
    except KeyError:
        if not args.none:
            sys.exit(1)
        return None

    try:
        evald = literal_eval(val)
    except Exception as exc:
        sys.stderr.write(str(exc))
        sys.exit(1)

    if args.bool:
        return bool(evald)
    return evald


def main():
    p = ArgumentParser()
    p.add_argument("env_var")
    p.add_argument(
        "--bool", action="store_true", default=False, help="Cast the value to a boolean."
    )
    p.add_argument(
        "--none",
        action="store_true",
        default=False,
        help="Output 'None' if the env var doesn't exist.",
    )
    args = p.parse_args()
    print(literalenv(args))


if __name__ == "__main__":
    main()
