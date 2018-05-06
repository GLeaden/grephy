# grephy
Formal Languages and Computability -- CMPT 440L

## What it Does
Grephy is a project created for my Formal Languages and Computability class. It is a light, homemade verison of grep. The only recognizable RegEx operators are: `( ) * +`. The `+` sign is not used as RegEx uses it (one or more) is used in a formal lanugages context of alternation (or).

This program makes use of Thompons's Construciton / Algorithim to convert from regex -> postfix regex -> NFA.

Grephy then utilizes subset construction to convert the NFA to a DFA. 

And finally, grephy will compute the DFA against each line of input out of a specified input file.

Grephy has the capability to 'pretty print' the resulting NFA and DFA by both outputting a graph to a specified file in DOT language, and rendering the graph to a pdf document.

## How to Use
1. Make sure you have [Python 3.4+][python] and graphviz installed.  
`$ pip install graphviz`
2. Clone the repo and navigate to the proper directory.  
`$ cd grephy`
3. Run the program! An example call is shown below:  
`$ grephy [-n NFA-FILE] [-d DFA-FILE] REGEX FILE`
4. You can use `$ grephy -h` to list some useful help information.


## Acknowledgements
I'd like to thank Marist College and my professor Michael E. Gildein for this course.

Thanks to Russ Cox of https://swtch.com/~rsc/regexp/ his Articles and Notes on regular expressions really helped me finish this project with a complete understanding.

[python]: https://www.python.org/downloads/
