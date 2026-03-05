#!/bin/bash

echo -n "Iniciar contagem regressiva de quanto? "
read inicio

echo "Iniciando..."
for (( i=$inicio; i>=0; i-- )); do
    echo "$i..."
    sleep 1
done
