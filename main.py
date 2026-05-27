"""Ponto de entrada da simulação energética da colônia Aurora Sieger.

Cada execução simula UMA semana. O estado da reserva e o contador de semanas
são persistidos em `colony_state.json` — assim, rodar várias vezes simula
semanas consecutivas.

Uso:
    python3 main.py           # simula a próxima semana
    python3 main.py --reset   # apaga o estado e recomeça da semana 1
"""

import sys

from utils import get_random_history, format_energy
from energy_manager import simulate_week
from display import show_report
from storage import load_state, save_state, reset_state, STORAGE_FILE

MAX_ENERGY_CAPACITY = 5000


def build_colony(initial_energy: float) -> dict:
    """Constrói a colônia com a reserva inicial vinda do estado persistido."""
    return {
        "max_energy_capacity": MAX_ENERGY_CAPACITY,
        "current_energy": initial_energy,
        "sections": [
            {
                "id": 1,
                "type": "residential",
                "modules": [
                    {"enabled": True, "type": "life_support",   "energy_consumption": 400, "priority": 0},
                    {"enabled": True, "type": "hygiene",        "energy_consumption": 300, "priority": 2},
                    {"enabled": True, "type": "entertainment",  "energy_consumption": 600, "priority": 3},
                ],
            },
            {
                "id": 2,
                "type": "medical",
                "modules": [
                    {"enabled": True, "type": "surgery",   "energy_consumption": 500, "priority": 0},
                    {"enabled": True, "type": "pharmacy",  "energy_consumption": 200, "priority": 1},
                    {"enabled": True, "type": "emergency", "energy_consumption": 300, "priority": 0},
                ],
            },
            {
                "id": 3,
                "type": "science",
                "modules": [
                    {"enabled": True, "type": "research_lab",   "energy_consumption": 700, "priority": 1},
                    {"enabled": True, "type": "data_analysis",  "energy_consumption": 400, "priority": 2},
                    {"enabled": True, "type": "experiments",    "energy_consumption": 500, "priority": 3},
                ],
            },
            {
                "id": 4,
                "type": "logistics",
                "modules": [
                    {"enabled": True, "type": "storage",     "energy_consumption": 300, "priority": 1},
                    {"enabled": True, "type": "transport",   "energy_consumption": 400, "priority": 2},
                    {"enabled": True, "type": "maintenance", "energy_consumption": 200, "priority": 3},
                ],
            },
        ],
        "energy_generation_modules": [
            {"type": "solar",  "input_history": get_random_history(), "generation_rate": 0.6},
            {"type": "eolian", "input_history": get_random_history(), "generation_rate": 0.8},
        ],
    }


def main() -> None:
    if "--reset" in sys.argv:
        had_state = reset_state()
        msg = "Estado anterior apagado." if had_state else "Não havia estado salvo."
        print(f"[reset] {msg} Recomeçando da semana 1.\n")

    state = load_state()

    print(f"=== Semana {state['week']} ===")
    print(f"Reserva energética no início da semana: "
          f"{format_energy(state['current_energy'])} de {MAX_ENERGY_CAPACITY} kWh\n")

    colony = build_colony(initial_energy=state["current_energy"])
    report = simulate_week(colony)
    show_report(report)

    final_energy = report["reserve_after"]
    if isinstance(final_energy, float) and final_energy.is_integer():
        final_energy = int(final_energy)

    next_state = {
        "week": state["week"] + 1,
        "current_energy": final_energy,
    }
    save_state(next_state)

    print(
        f"\n[estado salvo em '{STORAGE_FILE}'] "
        f"Próxima execução: semana {next_state['week']} com "
        f"{format_energy(next_state['current_energy'])} kWh em reserva."
    )


if __name__ == "__main__":
    main()
