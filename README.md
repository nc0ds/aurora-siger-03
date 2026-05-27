# Aurora SIGER — Sistema Inteligente de Gerenciamento Energético

Sistema desenvolvido em Python para simular o gerenciamento energético da colônia Aurora SIGER em Marte.

O projeto organiza dados da colônia, analisa geração e consumo de energia, toma decisões automáticas e controla reservas energéticas de forma autônoma.

---

# Como o Sistema Funciona

O sistema representa a colônia utilizando estruturas de dados como:

- Dicionários;
- Listas;
- Organização hierárquica.

A colônia possui:

- Seções operacionais;
- Módulos com consumo energético;
- Fontes de geração de energia;
- Reserva energética.

---

## Regras do Sistema

A cada semana o sistema:

1. Calcula o consumo total da colônia;
2. Calcula a produção de energia solar e eólica;
3. Compara produção e consumo;
4. Toma decisões automáticas.

---

## Possíveis Decisões

### Se houver energia suficiente
- O excedente é armazenado na reserva.

### Se faltar energia
- O sistema utiliza a reserva energética.

### Se a reserva não for suficiente
- Módulos menos importantes são desligados automaticamente.

### Em caso crítico
- O sistema mantém apenas módulos essenciais ativos.

---

# Estrutura do Projeto

```text
main.py                -> Execução principal
energy_manager.py      -> Regras de decisão
utils.py               -> Funções auxiliares
display.py             -> Exibição dos relatórios
storage.py             -> Persistência de estado
