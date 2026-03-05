#!/bin/bash
echo -n "Digite um número: "
read num

if [ $((num % 2)) -eq 0 ]; then
    echo "O número $num é PAR."
else
    echo "O número $num é ÍMPAR."
fi
