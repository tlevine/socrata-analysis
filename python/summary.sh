#!/bin/sh
set -e

n=$(ls data/*/views|grep -v :|wc -l) # 58097
echo There are $n total datasets in all of the Socrata portals.

n_nonempty=0
n_nonempty_increment() {
  if test -s $1; then
    n_nonempty=$(($n_nonempty + 1))
  fi
}
for path in $(find data -name *-* -type f); do
  n_nonempty_increment $path
done
echo Of those, $n_nonempty contain metadata\; the others are empty files.
