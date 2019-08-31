#!/usr/bin/env bash

#   Copyright (c) 2018-2019 Alexander L. Hayes (@hayesall)
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

echo "Downloading v1-0.jar and auc.jar"

curl -k -L https://github.com/boost-starai/BoostSRL-Misc/blob/master/VersionHistory/Version1.0/v1-0.jar?raw=true > v1-0.jar
curl -k -L https://github.com/boost-starai/BoostSRL-Misc/blob/master/VersionHistory/Version1.0/auc.jar?raw=true > auc.jar
