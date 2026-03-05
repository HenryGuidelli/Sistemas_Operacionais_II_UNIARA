#!/bin/bash

echo -n "Deseja a tabuada de qual número? "
read num
i=1

echo "Tabuada do $num:"
while [ $i -le 10 ]; do
    resultado=$((num * i))
    echo "$num x $i = $resultado"
    i=$((i + 1))
done
