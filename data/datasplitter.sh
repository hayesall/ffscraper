#!/usr/bin/env bash

#   Copyright (c) 2018 Alexander L. Hayes (@batflyer)
#
#   Licensed under the Apache License, Version 2.0 (the "License");
#   you may not use this file except in compliance with the License.
#   You may obtain a copy of the License at
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS,
#   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#   See the License for the specific language governing permissions and
#   limitations under the License.

# FanfictionScraper.py dumps the contents it scrapes into facts.txt.
# This takes facts.txt and turns it into a dataset with train/test splits.


# Usage:
# $ bash datasplitter.sh

# Put a copy of facts.txt to the side in case something goes wrong.
cp facts.txt facts-orig.txt

# Separate the authors from the facts
grep "author" facts.txt | sort -R > posEx.txt
grep -v "author" facts.txt > temp
mv temp facts.txt

# Create train and test directories, or remove them if they existed.
rm -rf learn; mkdir learn
rm -rf infer; mkdir infer

# Move facts.txt into the learn and infer folders.
cp facts.txt learn/learn_facts.txt
mv facts.txt infer/infer_facts.txt

# Randomly sample a percentage of the data (sorted randomly earlier)
# Split lines in posEx into 10 files
split --number=l/10 posEx.txt

# Put 70% in learn
mv xaa learn/learn_pos.txt
cat xab >> learn/learn_pos.txt
cat xac >> learn/learn_pos.txt
cat xad >> learn/learn_pos.txt
cat xae >> learn/learn_pos.txt
cat xaf >> learn/learn_pos.txt
cat xag >> learn/learn_pos.txt

# Put 30% in infer
mv xah infer/infer_pos.txt
cat xai >> infer/infer_pos.txt
cat xaj >> infer/infer_pos.txt

# Remove backups and the posEx.txt that was split.
rm -f xa*
rm -f posEx.txt

# Generate negative examples based on the contents of the positive examples.
python create_negatives.py -f learn/learn_pos.txt -o learn/learn_neg.txt
python create_negatives.py -f infer/infer_pos.txt -o infer/infer_neg.txt
