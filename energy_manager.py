"""Gerenciamento energético da colônia: regras de decisão e simulação semanal.

A função pública `simulate_week` aplica as regras de negócio descritas no
relatório e devolve um dicionário-report que descreve tudo o que aconteceu
na semana, sem imprimir nada. Toda a apresentação fica em `display.py`.
"""

from utils import (
    get_section_energy_consumption,
    get_energy_production,
    disable_modules_by_priority,
)

# Prioridades em ordem decrescente de descarte (3 = baixa primeiro).
# Prioridade 0 é essencial e nunca é desabilitada.
PRIORITY_LEVELS_DESCENDING = [3, 2, 1]


def _build_consumption_breakdown(colony: dict) -> list[dict]:
    """Detalha o consumo por seção (apenas dados, sem rótulos em PT-BR)."""
    return [
        {
            "type": section["type"],
            "value": get_section_energy_consumption(section),
        }
        for section in colony["sections"]
    ]


def _build_production_breakdown(colony: dict) -> list[dict]:
    """Detalha a produção por fonte de energia."""
    return [
        {
            "type": module["type"],
            "value": get_energy_production(
                module["input_history"], module["generation_rate"]
            ),
        }
        for module in colony["energy_generation_modules"]
    ]


def simulate_week(colony: dict) -> dict:
    """Executa o ciclo semanal da colônia e retorna um relatório estruturado.

    Aplica, em ordem, as regras de negócio do relatório:
      1. Se produção ≥ consumo → armazena o excedente (respeitando a capacidade);
      2. Se produção < consumo e reserva cobre o déficit → usa a reserva;
      3. Caso contrário → drena a reserva e desabilita módulos por prioridade
         (3 → 2 → 1), parando assim que o déficit for compensado;
      4. Se mesmo desabilitando todos os módulos não-essenciais ainda restar
         déficit, registra `remaining_deficit` no report.

    A função muta a colônia (atualiza `current_energy` e desabilita módulos).
    """
    consumption_by_section = _build_consumption_breakdown(colony)
    production_by_source = _build_production_breakdown(colony)

    consumption = sum(item["value"] for item in consumption_by_section)
    production = sum(item["value"] for item in production_by_source)
    balance = production - consumption

    reserve_before = colony["current_energy"]
    max_capacity = colony["max_energy_capacity"]

    report = {
        "consumption": {"total": consumption, "by_section": consumption_by_section},
        "production": {"total": production, "by_source": production_by_source},
        "balance": balance,
        "reserve_before": reserve_before,
        "reserve_after": reserve_before,
        "max_capacity": max_capacity,
        "stored": 0,
        "discarded": 0,
        "used_from_reserve": 0,
        "disabled_priorities": [],
        "remaining_deficit": 0,
        "action": None,
    }

    if balance >= 0:
        _handle_surplus(colony, report, balance)
    else:
        _handle_deficit(colony, report, deficit=-balance)

    report["reserve_after"] = colony["current_energy"]
    return report


def _handle_surplus(colony: dict, report: dict, balance: float) -> None:
    """Armazena o excedente na reserva, respeitando a capacidade máxima."""
    reserve_before = report["reserve_before"]
    max_capacity = report["max_capacity"]
    new_reserve = reserve_before + balance

    if new_reserve > max_capacity:
        report["stored"] = max_capacity - reserve_before
        report["discarded"] = new_reserve - max_capacity
        colony["current_energy"] = max_capacity
    else:
        report["stored"] = balance
        colony["current_energy"] = new_reserve

    report["action"] = "surplus_stored"


def _handle_deficit(colony: dict, report: dict, deficit: float) -> None:
    """Cobre o déficit com a reserva e, se necessário, desabilitando módulos."""
    reserve_before = report["reserve_before"]

    # Caso 1: a reserva sozinha cobre o déficit
    if reserve_before >= deficit:
        report["used_from_reserve"] = deficit
        colony["current_energy"] = reserve_before - deficit
        report["action"] = "reserve_used"
        return

    # Caso 2: drena toda a reserva e desabilita módulos por nível de prioridade
    report["used_from_reserve"] = reserve_before
    colony["current_energy"] = 0
    remaining_deficit = deficit - reserve_before

    for priority in PRIORITY_LEVELS_DESCENDING:
        if remaining_deficit <= 0:
            break
        energy_saved = disable_modules_by_priority(colony, priority)
        if energy_saved > 0:
            report["disabled_priorities"].append(priority)
            remaining_deficit -= energy_saved

    if remaining_deficit > 0:
        report["action"] = "deficit_unresolved"
        report["remaining_deficit"] = remaining_deficit
    else:
        report["action"] = "modules_disabled"
