"""TODO:
create main function with argument parsing capabilities
"""
def main():
  pass

def learnAlphabet(fileName):
  alphabet = set()
  inputFile = open(fileName, "r")
  line = inputFile.readlines()
  for i in line:
    for c in i:
      alphabet.add(c)
  return alphabet