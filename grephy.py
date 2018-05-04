import argparse
from automata import *

def main():
    args = parse_args()
    alphabet = learn_alphabet(args.input_file)
    postfix = re2post(args.RegEx)
    nfa = post_to_NFA(postfix)
    if args.n:
        pretty_print_nfa(nfa, args.n)
    if args.d:
        pass


def parse_args():
    parser = argparse.ArgumentParser(description='search regex pattern in file.')
    parser.add_argument('RegEx', metavar='REGEX-PATTERN', type=str,
                        help="the regular expression pattern to search"+
                        "input file with")
    parser.add_argument('input_file', metavar='INPUT-FILE', type=argparse.FileType('r'),
                        help="the file to test regex against")
    parser.add_argument("-n",
                        help="enable NFA output to specified file")
    parser.add_argument("-d", type=argparse.FileType('rw'),
                        help="enable DFA output to specified file")
    args = parser.parse_args()
    return args

if __name__ == "__main__":
    main()
    