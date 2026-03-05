#!/bin/bash
arquivo="dados.txt"

contador=0
while IFS= read -r linha
do
contador=$((contador + 1))
echo "Linha $contador: $linha"
done < "$arquivo"
echo "Total de linhas: $contador"
