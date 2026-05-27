"""Funções utilitárias puras para cálculo energético da colônia.

Todas as funções aqui são puras (sem efeitos colaterais sobre a colônia),
com exceção de `disable_modules_by_priority`, que muta os módulos da colônia
por design — é a primitiva usada pelo gerenciador de energia.
"""

from random import randrange

# Parâmetros do modelo energético (conforme relatório)
ENERGY_CONST = 50          # constante de conversão histórico → energia
HISTORY_DAYS = 7           # janela semanal
HISTORY_MAX_VALUE = 20     # valor histórico ambiental máximo (intervalo [0, 20])


def format_energy(value: float | int) -> str:
    """Formata valores energéticos para exibição.

    Inteiros e floats que representam inteiros saem sem `.0`; floats reais
    saem com duas casas decimais.
    """
    if isinstance(value, float) and value.is_integer():
        return str(int(value))
    if isinstance(value, float):
        return f"{value:.2f}"
    return str(value)


def get_random_history() -> list[int]:
    """Gera um histórico ambiental aleatório de HISTORY_DAYS dias.

    Retorna a lista de valores brutos (0 a HISTORY_MAX_VALUE), sem aplicar
    a constante de energia — isso é responsabilidade do cálculo de produção.
    """
    return [randrange(0, HISTORY_MAX_VALUE + 1) for _ in range(HISTORY_DAYS)]


def get_daily_energy_production(history: list[int], rate: float) -> list[float]:
    """Calcula a produção energética diária aplicando a fórmula do relatório:
    `(valor_histórico × ENERGY_CONST) × rate` para cada dia.
    """
    return [value * ENERGY_CONST * rate for value in history]


def get_energy_production(history: list[int], rate: float) -> float:
    """Soma a produção semanal de energia para uma fonte (solar, eólica, etc)."""
    return sum(get_daily_energy_production(history, rate))


def get_section_energy_consumption(section: dict) -> int:
    """Soma o consumo de todos os módulos habilitados de uma seção."""
    return sum(
        module["energy_consumption"]
        for module in section["modules"]
        if module["enabled"]
    )


def get_total_energy_consumption(colony: dict) -> int:
    """Soma o consumo total da colônia (todas as seções)."""
    return sum(get_section_energy_consumption(s) for s in colony["sections"])


def get_total_energy_production(colony: dict) -> float:
    """Soma a produção total de energia da colônia (todas as fontes)."""
    return sum(
        get_energy_production(module["input_history"], module["generation_rate"])
        for module in colony["energy_generation_modules"]
    )


def disable_modules_by_priority(colony: dict, priority: int) -> int:
    """Desabilita todos os módulos habilitados de uma dada prioridade.

    Retorna o total de energia compensada (somatório do consumo dos módulos
    desabilitados nesta chamada).
    """
    energy_saved = 0
    for section in colony["sections"]:
        for module in section["modules"]:
            if module["enabled"] and module["priority"] == priority:
                module["enabled"] = False
                energy_saved += module["energy_consumption"]
    return energy_saved
