""" Quick and dirty wrapper for argparse, with the intent to be less verbose

Meant to be used like this::

    import argp
    s1 = argp.sub("check", do_check)
    s2 = argp.sub("sign", do_sign, help="Sign the delivery")

    s2.arg("signature", metavar="SIGNATURE")

    argp.parse()
"""

import argparse, sys

# yes, 'p' will contain the parser
from typing import Callable, Any

p: argparse.ArgumentParser
subparsers: Any


def init(parser: argparse.ArgumentParser = None):
    """This module needs to be initialized by 'init'.

    Can be called with parser to use a pre-built parser, otherwise
    a simple default parser is created
    """

    global p, subparsers
    if parser is None:
        p = argparse.ArgumentParser()
    else:
        p = parser

    subparsers = p.add_subparsers()


def parse_list(l: list) -> argparse.Namespace:
    """ call if you want to provide the list yourself, instead of defaulting to sys.argv[1:] (as with parse) """
    parsed = p.parse_args(l)
    dispatch_parsed(parsed)
    return parsed


def dispatch_parsed(parse_result: argparse.Namespace):
    """ Call this if you did 'ArgumentParser.parse_arguments' yourself """
    if "func" in parse_result:
        parse_result.func(parse_result)


def parse():
    """Call this after declaring your arguments"""
    parse_list(sys.argv[1:])


def sub(name: str, func: Callable, **kwarg):
    """Add subparser"""
    sp = subparsers.add_parser(name, **kwarg)
    sp.set_defaults(func=func)
    sp.arg = sp.add_argument
    return sp
