#!/bin/bash

soma=0
contador=0

echo "Digite os números (digite 0 para sair):"

while true; do
    read num
    
    if [ "$num" -eq 0 ]; then
        break
    fi
    
    soma=$((soma + num))
    contador=$((contador + 1))
done

if [ $contador -gt 0 ]; then
    media=$(echo "scale=2; $soma / $contador" | bc)
    echo "---------------------------"
    echo "Quantidade de números: $contador"
    echo "Soma total: $soma"
    echo "Média: $media"
else
    echo "Nenhum número foi digitado além do zero."
fi
