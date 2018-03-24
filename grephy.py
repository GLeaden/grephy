import argparse

"""TODO:
create main function with argument parsing capabilities
"""

def main():
  args = parseArgs()
  alphabet = learnAlphabet(args.inputFile)
  for i in alphabet:
    print i,
    print ord(i)



def parseArgs():
  parser = argparse.ArgumentParser(description='search regex pattern in file.')
  parser.add_argument('RegEx', metavar='REGEX-PATTERN', type=str,
                    help="the regular expression pattern to search"+
                    "input file with")
  parser.add_argument('inputFile', metavar='INPUT-FILE', type=argparse.FileType('r'),
                    help="the file to test regex against")
  parser.add_argument("-n", type=argparse.FileType('rw'),
                    help="enable NFA output to specified file")
  parser.add_argument("-d", type=argparse.FileType('rw'),
                    help="enable DFA output to specified file")
  args = parser.parse_args()
  return args;


def learnAlphabet(inputFile):
  alphabet = set()
  with inputFile as file:
    line = inputFile.readlines()
    for i in line:
      i = i.replace("\n", "")
      i = i.replace("\r", "")
      for c in i:
        alphabet.add(c)
    return alphabet

if __name__ == "__main__":
  main()