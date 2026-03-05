#!/bin/bash
arquivo="numeros.txt"

contador=0
while IFS= read -r linha; do
	if [ "$linha" -gt 20 ]; then

		contador=$((contador + 1))
		echo "Linha $contador: $linha"
		
	fi

done < "$arquivo"

echo "Total de linhas: $contador"
