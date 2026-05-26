# Aurora Siger - Fase 3

**Integrantes do grupo:**

- Nathan Caio da Silva - RM 568750
- Gabrielly Drosda da Silva - RM 571793
- Eduardo Alves da Silva - RM 568601
- Lisandra Jacinto de Araujo - RM 574055

## Pré-requisitos

- Python 3.12+

## Como executar

Após clonar o repositório, apenas rode o comando `python3 main.py` para executar o script.

## Resultado esperado

Ao executar, será exibido um relatório de informações energéticas da colônia, utilizando dados históricos gerados aleatóriamente, podendo um dos caminhos da tomada de decisão:

- Se a produção de energia semanal for **maior que** o consumo semanal:
  - Saldo excedente é adicionado à reserva da colônia;
- Se a produção de energia semanal for **menor que** o consumo semanal:
  - Reserva de energia é utilizada para cobrir o saldo energético devedor;
    - Caso ainda haja saldo devedor, o algoritmo desabilita os módulos baseado em nível de prioridade, do menos prioritário ao mais prioritário.