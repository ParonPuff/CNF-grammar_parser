#!/bin/bash
smallest=$1
step=$2
largest=$3

#should be accepted
#ccc ... cccabccc ... ccc 
cd "$(dirname "$0")" # don't change this

for i in $(seq $smallest $step $largest); do
	echo -n "a"
	for j in $(seq 1 $((i/2))); do
		echo -n "c"
	done
	echo -n "ab"
	for j in $(seq 1 $((i/2))); do
		echo -n "c"
	done
	echo "b"
done