#!/usr/bin/env bash

# Apache License 2.0
#
# Copyright (c) 2018 Alexander L. Hayes (@batflyer)

BASE="https://www.fanfiction.net/book/Hitchhiker-s-Guide-to-the-Galaxy/?&srt=1&r=10&p="

for i in {1..25}; do
  URL=$BASE$i
  echo "$URL"
  PAGE="`wget --no-check-certificate -q -O - $URL`"
  echo "$PAGE" | grep "class=stitle" | cut -c117-137 | cut -d'/' -f 3 >> data/Hitchhikers/sids.txt
  sleep 3
done
