#!/bin/bash

# This is a short script for estimating the number of negative examples
# in one of the relational datasets.

# This is done by counting the number of negatives over a series of runs and
# averaging.


# Iterate to get estimates
for i in {1..100}; do

    # Copy facts
    cp Mockingbird/facts.txt .
    
    # Run the datasplitter.
    bash datasplitter.sh

    # wordcount of learning and inference
    wc -l learn/learn_neg.txt >> learn_negcount.txt
    wc -l infer/infer_neg.txt >> infer_negcount.txt

    # rinse and repeat
    rm -rf learn
    rm -rf infer
    
done

# Make sure that the dividend is correct!

awk '{sum += $1} END {print sum / 100}' learn_negcount.txt
awk '{sum += $1} END {print sum / 100}' infer_negcount.txt

rm -f learn_negcount.txt
rm -f infer_negcount.txt
