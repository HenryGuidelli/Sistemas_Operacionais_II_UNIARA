#!/bin/bash

pasta="backup";
teste="teste.txt";

if [ ! -d $pasta ]; then
    mkdir $pasta
    echo "Pasta $pasta criada!"
else
    echo "Pasta $pasta já existe!"
fi

echo "Criando arquivo teste!";

touch $teste; 

echo "Arquivo criado automaticamente pelo script" >> $teste;


echo "Movendo Arquivo";
mv $teste $pasta;
echo "Arquivo movido com sucesso!";

ls $pasta;