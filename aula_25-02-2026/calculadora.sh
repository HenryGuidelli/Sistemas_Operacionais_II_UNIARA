#!/bin/bash

calculadora() {
    local n1=$1
    local op=$2
    local n2=$3
    
    case $op in
        +) echo "Resultado: $((n1 + n2))" ;;
        -) echo "Resultado: $((n1 - n2))" ;;
        x|*) echo "Resultado: $((n1 * n2))" ;;
    esac
}

echo "Digite o primeiro número:"
read num1
echo "Digite a operação (+, -, x):"
read operacao
echo "Digite o segundo número:"
read num2

calculadora $num1 "$operacao" $num2
