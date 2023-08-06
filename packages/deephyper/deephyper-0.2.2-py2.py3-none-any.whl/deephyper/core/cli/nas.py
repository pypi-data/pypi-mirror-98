import argparse
import os
import sys
import signal

from deephyper.search.util import load_attr_from

HPS_SEARCHES = {
    "ambs": "deephyper.search.nas.ambs.AMBNeuralArchitectureSearch",
    "random": "deephyper.search.nas.random.Random",
    "regevo": "deephyper.search.nas.regevo.RegularizedEvolution",
    "agebo": "deephyper.search.nas.agebo.AgEBO",
}


def add_subparser(parsers):
    parser_name = "nas"

    parser = parsers.add_parser(
        parser_name, help="Command line to run neural architecture search."
    )

    subparsers = parser.add_subparsers()

    for name, module_attr in HPS_SEARCHES.items():
        search_cls = load_attr_from(module_attr)

        subparser = subparsers.add_parser(name=name, conflict_handler="resolve")
        subparser = search_cls.get_parser(subparser)

        subparser.set_defaults(func=main)


def main(**kwargs):
    search_name = sys.argv[2]
    search_cls = load_attr_from(HPS_SEARCHES[search_name])
    search_obj = search_cls(**kwargs)
    try:
        on_exit = load_attr_from(f"{search_obj.__module__}.on_exit")
        signal.signal(signal.SIGINT, on_exit)
        signal.signal(signal.SIGTERM, on_exit)
    except AttributeError:  # on_exit is not defined
        print("This search doesn't have an exiting procedure...")
    search_obj.main()
