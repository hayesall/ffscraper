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

while getopts "h" o; do
  case ${o} in
    h)
      # Show help information and exit.
      head -n 33 $0 | tail -n +3 | sed 's/#//'
      exit 0
      ;;
  esac
done

# Data should be in one of the respective directories in ../data/
# ../data/Hitchhikers/facts.txt
# ../data/Mockingbird/facts.txt
# ../data/Dragonriders/facts.txt
# ../data/Coraline/facts.txt

function runBoostingJob() {
  exit 0
}

(
  cd ../data/

  cp Hitchhikers/facts.txt .
  bash datasplitter.sh

  mv learn ../boosting/
  mv infer ../boosting/
)

if [[ ! -d learn ]]; then exit 1; fi
if [[ ! -d infer ]]; then exit 1; fi

exit 0
