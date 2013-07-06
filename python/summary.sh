#!/bin/sh
set -e

n_nonempty_increment() {
  if test -s "$1"; then
    n_nonempty=$(($n_nonempty + 1))
  fi
}

n=0
n_nonempty=0
for path in $(find data/ -wholename '*views/*' -type f); do
  n=$(($n + 1))
  n_nonempty_increment "$path"
done

echo There are $n total datasets in all of the Socrata portals.
echo Of those, $n_nonempty contain metadata\; the others are empty files.
