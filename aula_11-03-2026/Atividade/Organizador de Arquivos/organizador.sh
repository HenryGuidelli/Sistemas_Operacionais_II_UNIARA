#!/bin/bash

PASTA_ORG="Organização";
PASTA_textos="$PASTA_ORG/textos";
PASTA_imagens="$PASTA_ORG/imagens";
PASTA_codigos="$PASTA_ORG/codigos";
PASTA_outros="$PASTA_ORG/outros";

for i in {1..10}; do
    touch "arquivo$i.txt" "arquivo$i.jpg" "arquivo$i.pdf" "arquivo$i.png" "arquivo$i.c" "arquivo$i.sh" "arquivo$i.zip";
done

if [ ! -d $PASTA_ORG ]; then
    mkdir -p $PASTA_textos $PASTA_imagens $PASTA_codigos $PASTA_outros;
fi

count=0

for arquivo in *; do
    if [ -f "$arquivo" ] && [ $arquivo != $(basename "$0") ]; then
       
        case $arquivo in
            *.txt | *.pdf)
                mv $arquivo $PASTA_textos
            ;;

            *.jpg | *.png)
                    mv $arquivo $PASTA_imagens
            ;;
            
            *.c | *.sh)
                mv $arquivo $PASTA_codigos
            ;;

            *)
                mv $arquivo $PASTA_outros
        esac

        ((count++));
    fi
done

echo "Organização concluída com sucesso!";
echo "Total de arquivos movidos: $count"