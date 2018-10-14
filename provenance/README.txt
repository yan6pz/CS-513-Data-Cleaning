Programming Assignment #5: Provenance Querying

After unzipping, you should find two subfolders:
- facts/
- solutions_output/

There is also a file "make-solutions.sh" that was used to create the sample solution outputs from the query files (there are not provided, but need to be provided by the student). You can ignore this file. On the other hand, it might help you understand how you can invoke DLV with the facts file and your own solution queries.

For example, the make-solutions.sh has a line:

dlv facts/problem1-lca.dlv not_for_learner/problem1-lca-queries.dlv -silent -filter=a1 > ./solutions_output/problem1-a1.dlv.out

This means DLV is invoked with the facts file "problem1-lca.dlv" and problem1-lca-queries.dlv(provided with solutions ommitted, use it as template) to generate the sample output in the solutions folder, here the file "a1" (with one of the answers to Problem 1).

If you want to test your own solutions, invoke DLV as follows from the command line:

dlv facts/problem1-lca.dlv problem1-lca-queries.dlv

Then you can compare your DLV outputs with those in the solutions subfolder.

The autograder (evaluate.py) automates that comparison. Run autograder like "python evaluate.py"

Hope this helps!

Please post any questions you might have on Piazza under the #hw5 section..

BL

