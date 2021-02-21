#!/bin/bash

declare -a front=(
  'password'
  'p@ssw0rd'
  'secret'
  's3cr3t'
)

declare -a middle=(
  '1234'
  '!@#$'
)

declare -a end=(
  'reddit'
  'r3dd1t'
)

for f in ${front[*]}; do
  echo "${f}"
  for m in ${middle[*]}; do
    echo "${f}${m}"
    for e in ${end[*]}; do
      echo "${f}${m}${e}"
    done
  done
done
