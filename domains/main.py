#!/usr/bin/env python


"""Tool to create and manage domain records in the cloud"""


from __future__ import print_function

from os import environ
from argparse import ArgumentDefaultsHelpFormatter, ArgumentParser


from yaml import load
from pathlib import Path
from attrdict import AttrDict


from .api import Domains
from .version import version


def cmd_list(domains, args):
    domains.list()


def cmd_sync(domains, args):
    domains.sync()


def cmd_status(domains, args):
    domains.status()


def parse_args():
    parser = ArgumentParser(
        description=__doc__,
        version=version,
        formatter_class=ArgumentDefaultsHelpFormatter
    )

    parser.add_argument(
        "-f", "--file", dest="file", metavar="FILE", type=str,
        default=environ.get("DOMAINS_FILE", environ.get("FILE", "domains.yml")),
        help="Specify an alternate domains file"
    )

    parser.add_argument(
        "--verbose", dest="verbose",
        action="store_true", default=False,
        help="Show more output"
    )

    subparsers = parser.add_subparsers(
        title="Commands", metavar="[Command]",
    )

    # list
    list_parser = subparsers.add_parser(
        "list",
        help="List all domains"
    )
    list_parser.set_defaults(func=cmd_list)

    # sync
    sync_parser = subparsers.add_parser(
        "sync",
        help="Synchronize all domains"
    )
    sync_parser.set_defaults(func=cmd_sync)

    # status
    status_parser = subparsers.add_parser(
        "status",
        help="Display status of all domains"
    )
    status_parser.set_defaults(func=cmd_status)

    return parser.parse_args()


def main():
    args = parse_args()

    config = AttrDict(load(Path(args.file).resolve().open("r")))
    domains = Domains(config)

    args.func(domains, args)


if __name__ == "__main__":
    main()
