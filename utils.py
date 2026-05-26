from random import randrange

def get_random_history() -> list[dict]:
    energy_const = 50
    history = []

    for _ in range(0, 7):
        val = randrange(0, 21)
        history.append(val * energy_const)

    return history

def get_energy_production(history: list[int], rate: float) -> dict:
    energy = []
    total = 0

    for i in history:
        energy.append(i * rate)
        total += i * rate

    production = {
        "energy_history": energy,
        "total": total
    }

    return production

def get_total_energy_consumption(colony: dict) -> int:
    total = 0

    for section in colony["sections"]:
        total += get_section_energy_consumption(section)

    return total


def get_total_energy_production(colony: dict) -> int:
    total = 0

    for module in colony["energy_generation_modules"]:
        production = get_energy_production(module["input_history"], module["generation_rate"])
        total += production["total"]

    return total

def get_section_energy_consumption(section: dict) -> int:
    total = 0

    for module in section["modules"]:
        if module["enabled"]:
            total += module["energy_consumption"]

    return total

def disable_modules(colony: dict, energy_to_compensate: int) -> list[int]:
    energy_compensated = 0
    disabled_priorities = []

    for cur_priority in range(3, 0, -1):
        if energy_compensated >= energy_to_compensate:
            return disabled_priorities
        
        disabled_priorities.append(cur_priority)

        for section in colony["sections"]:
            for module in section["modules"]:
                if module["enabled"] and module["priority"] == cur_priority:
                    module["enabled"] = False
                    energy_compensated += module["energy_consumption"]

    return disabled_priorities