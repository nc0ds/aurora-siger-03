# Aurora SIGER — Sistema Inteligente de Gerenciamento Energético

Sistema desenvolvido em Python para simular o gerenciamento energético da colônia Aurora SIGER em Marte.

O sistema organiza os dados da colônia, analisa geração e consumo de energia e toma decisões automáticas para manter os sistemas essenciais funcionando.

---

# Funcionamento do Sistema

O sistema:

- Organiza dados utilizando listas e dicionários;
- Calcula produção de energia solar e eólica;
- Analisa consumo energético da colônia;
- Utiliza reserva energética quando necessário;
- Desliga módulos menos prioritários em situações críticas;
- Mantém módulos essenciais sempre ativos;
- Salva o estado da colônia entre execuções.

---

# Estrutura do Projeto

```text
main.py
energy_manager.py
utils.py
display.py
storage.py
```

---

# Como Executar

## Executar a simulação

```bash
python main.py
```

ou

```bash
python3 main.py
```

---

## Reiniciar a simulação

```bash
python main.py --reset
```

---

# Exemplo de Entrada e Saída

## Entrada

```text
Reserva inicial: 1000 kWh
Produção total: 5000 kWh
Consumo total: 4800 kWh
```

## Saída

```text
A colônia tem energia suficiente para a próxima semana.

Excedente armazenado: 200

Reserva de energia atualizada: 1200 de 5000
```

---

# Repositório

https://github.com/nc0ds/aurora-siger-03.git
