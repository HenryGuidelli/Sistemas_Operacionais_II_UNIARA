#!/bin/bash
arquivo="frutas.txt"
if [ ! -f "$arquivo" ]; then
echo "Arquivo não encontrado!"
exit 1
fi
while IFS= read -r linha
do
echo "Linha: $linha"
done < "$arquivo"
