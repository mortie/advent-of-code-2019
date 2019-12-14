#!/bin/sh

fuel() {
	echo $((($1 / 3) - 2))
}

sum=0
for inp in $(cat input); do
	while :; do
		f=$(fuel $inp)
		if [ $f -lt 0 ]; then
			break
		fi
		sum=$((sum + f))
		inp=$f
	done
done
echo "$sum"
