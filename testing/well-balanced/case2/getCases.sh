#!/bin/bash
smallest=$1
step=$2
largest=$3


#should be accepted

cd "$(dirname "$0")" # don't change this

for i in $(seq $smallest $step $largest); do
	for j in $(seq 1 $i); do
		if [ $((j%2)) -eq 1 ]; then
			echo -n "(" 
		else
			echo -n ")" 
		fi
	done
	echo "" 
done