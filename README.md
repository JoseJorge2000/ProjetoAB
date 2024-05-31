# Análise de Algoritmos de Alinhamento de Sequência

## Autores

- [José Jorge](https://github.com/JoseJorge2000)
- [António Goulão](https://github.com/Agoulao)

## Efetuar alinhamento
Cada um dos ficheiros `kalign.py`, `tcoffee.py`, `clustalw.py` e `muscle.py` gera, na sua respetiva pasta, o resultado de todos os ficheiros presentes na pasta `/Datasets` em formato FASTA.
Para cada ficheiro será necessário mudar a diretoria na função `run_docker_for_files`, na variável `dir`.

Para kalign:
```
python kalign.py
```
Para T-Coffee:
```
python tcoffee.py
```
Para ClustalW:
```
python clustalw.py
```
Para MUSCLE;
```
python muscle.py
```
## Fazer avaliação dos alinhamentos
Após gerar os ficheiros com todas as ferramentas, corra o ficheiro score.py para fazer a avaliação dos alinhamentos com a matriz BLOSUM62 e guardar os resultados num ficheiro CSV.

Comando para executar a avaliação:
```
python score.py
```
O ficheiro `Resultado.csv` apresentará os dados após correr este código.

## Adicionar as médias ao ficheiro csv
O ficheiro `averages.py` adiciona as médias por ferramenta, alinhamento e número de linhas.

Comando para adicionar as médias:
```
python averages.py
```

## Resumo dos passos:
Para cada ficheiro será necessário mudar a diretoria na função run_docker_for_files, na variável dir.
Gerar alinhamentos:
```
python kalign.py
python tcoffee.py
python clustalw.py
python muscle.py
```
Avaliar alinhamentos:
```
python score.py
```

Adicionar médias:
```
python averages.py
```

Os resultados encontram-se no ficheiro `Resultados.csv`.
