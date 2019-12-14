#!/bin/sh
sum=0
for l in $(cat input); do
	sum=$((sum + ((l / 3) - 2)))
done
echo "$sum"
