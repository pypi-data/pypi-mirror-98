import os
import signal
import sys
from argparse import ArgumentParser
from .libs.setuptools import get_file_content
from .libs.json_filter import JsonFilter, JsonFilterException


def _handle_exit(sig, frame):
    print('Terminated.')
    sys.exit(0)


def _handle_args() -> tuple:
    version = get_file_content(os.path.join(os.path.dirname(__file__), "VERSION"))
    parser = ArgumentParser(description="JSON GREP v{version} is utility for filtering selected keys from json string piped from STDOUT".format(version=version))
    parser.add_argument("filter_keys", type=str, nargs="+", help="List of keys which you want to filter from json dict. \
                    You can also specify value of item which you want to pass only by operator = or ~. '~' means \
                    that value is in item on any string position. If key is in deeper level of tree structure use '.' separator \
                    to specify how deep is key in dict tree structure.")
    parser.add_argument("-m", "--multiline-output", dest="multiline_output", default=False, action="store_true", help="Use multiline output for filtered result")
    parser.add_argument("-v", "--values_only", dest="values_only", default=False, action="store_true", help="Show only values without keys description")
    parser.add_argument("-i", "--ignore-errors", dest="ignore_errors", default=False, action="store_true", help="Ignore errors caused by json decode")

    args = parser.parse_args()
    return args


def main():
    signal.signal(signal.SIGINT, _handle_exit)
    args = _handle_args()

    is_value_operator_used = any([True for key in args.filter_keys if JsonFilter.parse_key(key)[2]])

    for line in sys.stdin:
        try:
            results_data = JsonFilter.filter_keys_and_values(line, args.filter_keys, is_value_operator_used)
            if results_data:
                result = JsonFilter.format_result(results_data, multiline_output=args.multiline_output, values_only=args.values_only)
                sys.stdout.write(result)
        except JsonFilterException as ex:
            if not args.ignore_errors:
                sys.stderr.write("\33[31mJsonFilterException\33[0m: {}\n".format(ex))
    print("DONE.")


if __name__ == '__main__':
    main()
