#!/usr/bin/env bash


dlv facts/problem1-lca.dlv not_for_learner/problem1-lca-queries.dlv -silent -filter=a1 > ./solutions_output/problem1-a1.dlv.out
dlv facts/problem1-lca.dlv not_for_learner/problem1-lca-queries.dlv -silent -filter=a2 > ./solutions_output/problem1-a2.dlv.out
dlv facts/problem1-lca.dlv not_for_learner/problem1-lca-queries.dlv -silent -filter=b > ./solutions_output/problem1-b.dlv.out
dlv facts/problem1-lca.dlv not_for_learner/problem1-lca-queries.dlv -silent -filter=c1 > ./solutions_output/problem1-c1.dlv.out
dlv facts/problem1-lca.dlv not_for_learner/problem1-lca-queries.dlv -silent -filter=c2 > ./solutions_output/problem1-c2.dlv.out



dlv facts/problem2-sail.dlv not_for_learner/problem2-hamming-queries.dlv -silent -filter=a > ./solutions_output/problem2-a-sail.dlv.out
dlv facts/problem2-fish.dlv not_for_learner/problem2-hamming-queries.dlv -silent -filter=a > ./solutions_output/problem2-a-fish.dlv.out

dlv facts/problem2-sail.dlv not_for_learner/problem2-hamming-queries.dlv -silent -filter=b > ./solutions_output/problem2-b-sail.dlv.out
dlv facts/problem2-fish.dlv not_for_learner/problem2-hamming-queries.dlv -silent -filter=b > ./solutions_output/problem2-b-fish.dlv.out
