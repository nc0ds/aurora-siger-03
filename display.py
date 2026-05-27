"""Apresentação do relatório energético. Sem lógica de decisão.

Recebe o dicionário-report produzido por `energy_manager.simulate_week`
e o formata para exibição em console.
"""

from utils import format_energy as _fmt

# Tradução do `type` técnico para rótulo em PT-BR no relatório final.
# Manter a separação dados↔apresentação: a colônia armazena `type` em inglês,
# a tradução vive aqui.
SECTION_LABELS = {
    "residential": "Residencial",
    "medical": "Médica",
    "science": "Científica",
    "logistics": "Logística",
}

SOURCE_LABELS = {
    "solar": "Solar",
    "eolian": "Eólica",
}

PRIORITY_LABELS = {
    1: "alta",
    2: "média",
    3: "baixa",
}


def show_report(report: dict) -> None:
    """Imprime o relatório energético semanal completo."""
    _show_overview(report)
    _show_decision(report)


# --- Internos ----------------------------------------------------------------


def _label(mapping: dict, key: str) -> str:
    """Retorna o rótulo PT-BR; em fallback, devolve o próprio `type`."""
    return mapping.get(key, key)


def _show_overview(report: dict) -> None:
    print("=== Informações Energéticas da Colônia ===")

    print("Consumo semanal por seção:")
    for item in report["consumption"]["by_section"]:
        print(f"- {_label(SECTION_LABELS, item['type'])}: {_fmt(item['value'])}")
    print(f"Total do consumo semanal: {_fmt(report['consumption']['total'])}")

    print("Produção semanal por fonte:")
    for item in report["production"]["by_source"]:
        print(f"- {_label(SOURCE_LABELS, item['type'])}: {_fmt(item['value'])}")
    print(f"Produção semanal total: {_fmt(report['production']['total'])}")

    print(f"Saldo energético: {_fmt(report['balance'])}")


def _show_decision(report: dict) -> None:
    print("\n=== Análise de Sustentabilidade Energética ===")
    action = report["action"]

    if action == "surplus_stored":
        _show_surplus(report)
        return

    print("Atenção: energia produzida é insuficiente para atender ao consumo da próxima semana.")

    if action == "reserve_used":
        _show_reserve_used(report)
        return

    # action ∈ {"modules_disabled", "deficit_unresolved"}
    _show_modules_disabled(report)
    if action == "deficit_unresolved":
        print(
            f"ATENÇÃO: déficit de {_fmt(report['remaining_deficit'])} kWh permanece "
            "mesmo após desabilitar todos os módulos não-essenciais."
        )
    print(
        "Recomenda-se aumentar a produção de energia ou reduzir o consumo "
        "para evitar futuros déficits energéticos."
    )


def _show_surplus(report: dict) -> None:
    print("A colônia tem energia suficiente para a próxima semana.")
    if report["discarded"] > 0:
        print(
            "A produção de energia excede a capacidade máxima da colônia. "
            "Armazenando o máximo possível e descartando o excesso..."
        )
        print(f"Energia armazenada: {_fmt(report['stored'])}")
        print(f"Energia descartada (capacidade máxima atingida): {_fmt(report['discarded'])}")
    else:
        print(f"Excedente armazenado: {_fmt(report['stored'])}")
    print(
        f"Reserva de energia atualizada: {_fmt(report['reserve_after'])} "
        f"de {_fmt(report['max_capacity'])}"
    )


def _show_reserve_used(report: dict) -> None:
    print("Utilizando reservas de energia para compensar o déficit...")
    print(f"Energia retirada da reserva: {_fmt(report['used_from_reserve'])}")
    print(
        f"Reserva restante: {_fmt(report['reserve_after'])} "
        f"de {_fmt(report['max_capacity'])}"
    )


def _show_modules_disabled(report: dict) -> None:
    if report["reserve_before"] == 0:
        print("A colônia está sem reservas de energia para compensar o déficit.")
    else:
        print(
            f"Utilizando toda a reserva ({_fmt(report['used_from_reserve'])}) — "
            "ainda insuficiente."
        )
        print(f"Reserva restante: 0 de {_fmt(report['max_capacity'])}")

    if not report["disabled_priorities"]:
        print("Nenhum módulo pôde ser desabilitado para compensar o déficit.")
        return

    priorities_str = ", ".join(PRIORITY_LABELS[p] for p in report["disabled_priorities"])
    print("Desabilitando módulos de baixa prioridade para compensar o déficit energético...")
    print(f"Módulos de prioridade {priorities_str} foram desabilitados.")
    print(
        "Módulos de prioridade máxima foram mantidos para garantir o funcionamento "
        "dos sistemas essenciais da colônia."
    )
