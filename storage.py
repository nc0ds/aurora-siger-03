"""Persistência do estado da colônia entre execuções.

Cada execução de `main.py` representa uma semana. Este módulo cuida de
ler/gravar o estado em `colony_state.json` para que a reserva energética
e o contador de semanas continuem de onde pararam.
"""

import json
import os

STORAGE_FILE = "colony_state.json"

# Estado da semana 1 antes de qualquer simulação.
INITIAL_STATE = {
    "week": 1,
    "current_energy": 1000,
}


def load_state() -> dict:
    """Carrega o estado salvo do disco.

    Se o arquivo não existir (primeira execução) ou estiver corrompido,
    retorna uma cópia do estado inicial — não levanta exceção, apenas avisa.
    """
    if not os.path.exists(STORAGE_FILE):
        return dict(INITIAL_STATE)

    try:
        with open(STORAGE_FILE, "r", encoding="utf-8") as f:
            state = json.load(f)
    except (json.JSONDecodeError, OSError) as err:
        print(f"Aviso: não foi possível ler '{STORAGE_FILE}' ({err}). "
              "Reiniciando do estado inicial.")
        return dict(INITIAL_STATE)

    # Validação leve: garantir que as chaves esperadas existem
    if "week" not in state or "current_energy" not in state:
        print(f"Aviso: '{STORAGE_FILE}' está incompleto. "
              "Reiniciando do estado inicial.")
        return dict(INITIAL_STATE)

    return state


def save_state(state: dict) -> None:
    """Persiste o estado da colônia em JSON formatado."""
    with open(STORAGE_FILE, "w", encoding="utf-8") as f:
        json.dump(state, f, indent=2, ensure_ascii=False)


def reset_state() -> bool:
    """Apaga o arquivo de estado. Retorna True se havia algo para apagar."""
    if os.path.exists(STORAGE_FILE):
        os.remove(STORAGE_FILE)
        return True
    return False
