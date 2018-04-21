#!/usr/bin/env bash

# Overview:
#   Name: run_boosting_jobs.sh
#   Summary: A script for running BoostSRL jobs and recording results.
#   Author: Alexander L. Hayes (@batflyer)
#   Email: alexander.hayes@utdallas.edu
#   Copyright: 2018 (c) Alexander L. Hayes
#   License: Apache License Version 2.0

# Description:
#   A script for running BoostSRL jobs and recording results for reporting.

# Simple Usage:
#   $ bash run_boosting_jobs.sh

# Options:
#   -h      Display this help information and exit.
#   -a      Set the number of runs to average over (Default: 10)
#   -o      Set the output file location (Default: performance.txt)

# License:
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

averageover=10
outputfile="performance.txt"

while getopts "a:ho:" o; do
  case ${o} in
    a)
      # Set the number of runs to average over (default: 10)
      averageover=$OPTARG
      ;;
    h)
      # Show help information and exit.
      head -n 35 $0 | tail -n +3 | sed 's/#//'
      exit 0
      ;;
    o)
      # Set the output file to a custom location. Default performance.txt
      outputfile=$OPTARG
      ;;
  esac
done

# Data should be in one of the respective directories in ../data/
# ../data/Hitchhikers/facts.txt
# ../data/Mockingbird/facts.txt
# ../data/Dragonriders/facts.txt
# ../data/Coraline/facts.txt

function runBoostingJob() {
  # Run BoostSRL and record performance a given number of times.

  # Positional Arguments
  # $1 --> jobID
  # $2 --> trigger softmax boosting instead of normal RDN Learning
  jobID=$1$outputfile
  softm=False

  echo "$jobID----------" >> $jobID

  for _ in $(seq $averageover); do

    # Run Learning and Inference
    echo "    Started BoostSRL"
    java -jar v1-0.jar -l -train learn/ -target author -trees 15 > learnout.log
    echo "    Learning complete."
    java -jar v1-0.jar -i -model learn/models/ -test infer/ -target author -trees 15 -aucJarPath . > inferout.log
    echo "    Inference complete."

    # Record the results to the outputfile.
    tail -n 21 inferout.log >> $jobID
    echo "----------" >> $jobID

    # Cleanup
    rm -f inferout.log
    rm -f learnout.log
    rm -rf infer/
    rm -rf learn/

  done
}

function setData() {

  # Positional Arguments
  # $1 --> Row (Learn set)
  # $2 --> Col (Infer set)

  # e.g.
  # setData Coraline Coraline
  # setData Hitchhikers Mockingbird

  row=$1
  col=$2

  if [[ $row = $col ]]; then
    (
      # Learning and Inference are from the same set.
      cd ../data/
      cp $row/facts.txt .
      bash datasplitter.sh

      mv learn ../boosting/
      mv infer ../boosting/
    )
  else
    # Learning and inference are from different sets.
    (
      cd ../data/
      cp $row/facts.txt .
      bash datasplitter.sh

      mv learn ../boosting/
      rm -rf infer/
    )
    (
      cd ../data/
      cp $col/facts.txt .
      bash datasplitter.sh

      rm -rf learn/
      mv infere ../boosting/
    )
  fi
}

function Main() {
  ROWS=( Coraline Dragonriders ) #Hitchhikers Mockingbird )
  COLS=( Coraline Dragonriders ) #Hitchhikers Mockingbird )

  for r in "${ROWS[@]}"; do
    for c in "${COLS[@]}"; do
      echo "Currently on: $r-$c"
      setData $r $c
      runBoostingJob "$r-$c"
    done
  done
}

Main
exit 0
