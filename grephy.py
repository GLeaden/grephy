import argparse
from automata import post_to_NFA, NFA_to_DFA, learn_alphabet, pretty_print_DFA, pretty_print_NFA, re_to_post, compute_DFA

def main():
    args = parse_args()
    alphabet = learn_alphabet(args.input_file)
    postfix = re_to_post(args.RegEx, alphabet)
    nfa = post_to_NFA(postfix)
    dfa = NFA_to_DFA(nfa, alphabet)
    compute_DFA(dfa, args.input_file)
    if args.n:
        pretty_print_NFA(nfa, args.n)
    if args.d:
        pretty_print_DFA(dfa, args.d)


def parse_args():
    parser = argparse.ArgumentParser(description='search regex pattern in file.')
    parser.add_argument('RegEx', metavar='REGEX-PATTERN', type=str,
                        help="the regular expression pattern to search"+
                        "input file with")
    parser.add_argument('input_file', metavar='INPUT-FILE',
                        help="the file to test regex against")
    parser.add_argument("-n",
                        help="enable NFA output to specified file")
    parser.add_argument("-d",
                        help="enable DFA output to specified file")
    args = parser.parse_args()
    return args

if __name__ == "__main__":
    main()
    