import argparse

LETTERS = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
NUMBERS = '0123456789'

def main():
    args = parse_args()
    alphabet = learn_alphabet(args.input_file)
    converted_regex = explicit_concat(args.RegEx)
    postfix = convert_postfix(converted_regex)

    ## testing. . .
    for i in postfix:
        print (i, end="")
    print ( )

def parse_args():
    parser = argparse.ArgumentParser(description='search regex pattern in file.')
    parser.add_argument('RegEx', metavar='REGEX-PATTERN', type=str,
                        help="the regular expression pattern to search"+
                        "input file with")
    parser.add_argument('input_file', metavar='INPUT-FILE', type=argparse.FileType('r'),
                        help="the file to test regex against")
    parser.add_argument("-n", type=argparse.FileType('rw'),
                        help="enable NFA output to specified file")
    parser.add_argument("-d", type=argparse.FileType('rw'),
                        help="enable DFA output to specified file")
    args = parser.parse_args()
    return args

def learn_alphabet(input_file):
    alphabet = set()
    with input_file as file:
        line = file.readlines()
        for i in line:
            i = i.replace("\n", "")
            i = i.replace("\r", "")
            for c in i:
                alphabet.add(c)
    return alphabet

def explicit_concat(regex_pattern):
    """Takes a RegEx pattern ex. "abc" and returns a pattern with '.' between the previously implied concatinations ex. "a.b.c"

            Keyword Arguments:
            regex_pattern -- RegEx pattern to analyze
            """
    result = []
    for i in regex_pattern:
        if result:
            if i.isalpha() and result[-1].isalpha():
                result.append('.')
                result.append(i)
            else:
                result.append(i)
        else:
            result.append(i)
    return result
        

def convert_postfix(infix_pattern):
    """Utilizes Dikstras shunting yard algorithim to convert infix regex to postfix

            Keyword Arguments:
            infix_pattern -- regex pattern with EXPLICIT concatenations (abc = a.b.c)
            """
    tempstack = []
    postfix = []
    precidence = {'(':0, '|':1, '.':2, '*':3, '+':3}
    for i in infix_pattern:
        if i.isalpha():
            postfix.append(i)
        elif i == '(':
            tempstack.append(i)
        elif i == ')':
            top = tempstack.pop()
            while top != '(':
                postfix.append(top)
                top = tempstack.pop()
        else:
            while (tempstack) and (precidence[tempstack[-1]] >= precidence[i]):
                postfix.append(tempstack.pop())
            tempstack.append(i)
    while tempstack:
        postfix.append(tempstack.pop())
    return postfix  

if __name__ == "__main__":
    main()
    