#!/usr/bin/env python

import logging

from argparse import ArgumentParser
from store import ObjectStore
from backends.mock import MockBackend
from agent import Agent


def parse_options():
    parser = ArgumentParser("pyofagent - Python-based Open Flow Agent")
    parser.add_argument("-c", "--controller", #dest="controller",
                        help="Controller host:port to connect to", metavar="HOST:PORT",
                        default="localhost:6633")
    parser.add_argument("-d", "--devid", dest="datapath_id",
                        help="Device identified", metavar="DEVID",
                        default=42)
    parser.add_argument("-v", "--verbose", action='store_true', #dest=verbose,
                        default="enable verbose logging (log-level is DEBUG)")
    parser.add_argument("-I", "--in-out-iface", metavar="IN-OUT-IFACE",
                        help="Local interface to receve/send in-out frames",)
    parser.add_argument("-S", "--in-out-stag", metavar="IN-OUT-STAG",
                        help="Expect/Apply given s-tag when receiving/sending frames"+
                             "at the in-out interface")
    return parser.parse_args()


def main():

    args = parse_options()

    logging.basicConfig(level=logging.DEBUG if args.verbose else logging.INFO)

    store = ObjectStore()
    backend = MockBackend(store, in_out_iface=args.in_out_iface,
                                 in_out_stag=None if args.in_out_stag is None else int(args.in_out_stag))
    agent = Agent(args.controller, int(args.datapath_id), store, backend)
    store.set_agent(agent)
    backend.set_agent(agent)

    try:
        agent.run()
    except KeyboardInterrupt:
        logging.info("Ctrl-c received! Shutting down connection and exiting...")
        agent.stop()
        backend.stop()


if __name__ == '__main__':
    main()
