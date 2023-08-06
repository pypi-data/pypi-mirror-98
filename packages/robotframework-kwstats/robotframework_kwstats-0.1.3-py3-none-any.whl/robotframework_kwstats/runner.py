import os
import argparse
from .robotkwstats import generate_report
from .robotkwstats import IGNORE_TYPES
from .robotkwstats import IGNORE_LIBRARIES


def parse_options():
    parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    general = parser.add_argument_group("General")
    
    general.add_argument(
        '--ignorelib',
        dest='ignore',
        default=IGNORE_LIBRARIES,
        nargs="+",
        help="Ignore keywords of specified library in report"
    )

    general.add_argument(
        '--ignoretype',
        dest='ignoretype',
        default=IGNORE_TYPES,
        nargs="+",
        help="Ignore keywords with specified type in report"
    )

    general.add_argument(
        '-I', '--inputpath',
        dest='path',
        default=os.path.curdir,
        help="Path of result files"
    )

    general.add_argument(
        '-M', '--kwstats-report-name',
        dest='kwstats_report_name',
        help="Output name of the generate kwstats report"
    )

    general.add_argument(
        '-O', '--output',
        dest='output',
        default="output.xml",
        help="Name of output.xml"
    )

    args = parser.parse_args()
    return args


def main():
    args = parse_options()
    generate_report(args)