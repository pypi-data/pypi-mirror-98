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

    if args.bool or args.bool_rc:
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
    p.add_argument(
        "--bool-rc",
        action="store_true",
        default=False,
        help="Cast the value to a boolean and exit with code 1 if False, 0 if True",
    )
    p.add_argument(
        "-q", action="store_true", default=False, help="Don't output anything to stdout."
    )
    args = p.parse_args()
    evald = literalenv(args)

    if not args.q:
        print(evald)

    if args.bool_rc:
        sys.exit(1 - int(evald))


if __name__ == "__main__":
    main()
