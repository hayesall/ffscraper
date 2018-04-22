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

# Use the analyze_results.py script over a directory.

#\begin{tabular}{ |p|p|p|p|p| }
#\hline
#\multicolumn{4}{|c|}{}

for f in $(ls $1); do
  echo $f;
  python analyze_results.py -f $1/$f
  echo "---"
done
