# EfficientAlgorithms_step1


## Running the program

In order to run an algorithim launch main.py with a json file as input, the json file should be of the format:

```
    {
        "BU:well-balanced:case1":{
        "algorithm":"ParseBU",
        "grammar_path":"./testing/well-balanced/Well-Balanced_Parantheses.txt",
        "test_cases":"./testing/well-balanced/case1/getCases.sh 10 10 100"
        },
        "BU:well-balanced:case2":{
        "algorithm":"ParseBU",
        "grammar_path":"./testing/well-balanced/Well-Balanced_Parantheses.txt",
        "test_cases":"./testing/well-balanced/case2/getCases.sh 10 10 100"
        }
    }
```

Here algorithm is the name of the class that should be tested in an experiment, grammar_path should be a path to the grammar that should be used
and test_cases should be a shell command that generates the tests cases

The name of the experiment used will be the name of the csv file saved in the data folder when using the -l flag. The naming convention allows r scirpts to match csv files based on tags such as "BU" or "well-balanced"

## File formats

The file format for grammars are every rule written on a unique line and every rule is written as the nonterminal (written as capital letter) followed

by the product on one line meaning that the following:

S -> AB | q

becomes:

SAB
Sq

Whereas the test cases are simply written on new lines meaning that

```
()()()()()
((((()))))
```
is interpreted as two test cases.

## What happens
The program then runs all of the test cases against instances of all algorithims using the grammar denoted in the json file

10 then removes the 2 most extreme results and averages the rest
