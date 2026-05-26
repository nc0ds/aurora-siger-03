from utils import get_total_energy_consumption, get_total_energy_production, disable_modules, get_section_energy_consumption

def show_info(colony: dict) -> None:
  energy_consumption = get_total_energy_consumption(colony)
  energy_production = get_total_energy_production(colony)
  total_energy = energy_production - energy_consumption

  print("=== Informações Energéticas da Colônia ===")
  print(f"Consumo semanal das seções:")
  print(f"- Residencial: {get_section_energy_consumption(colony['sections'][0])}")
  print(f"- Médica: {get_section_energy_consumption(colony['sections'][1])}")
  print(f"- Científica: {get_section_energy_consumption(colony['sections'][2])}")
  print(f"- Logística: {get_section_energy_consumption(colony['sections'][3])}")
  print(f"Total do consumo semanal: {energy_consumption}")
  print(f"Produção semanal de energia: {energy_production}")
  print(f"Saldo energético: {total_energy}")

  print("\n=== Análise de Sustentabilidade Energética ===")

  if total_energy >= 0:
    print("A colônia tem energia suficiente para a próxima semana.")
    
    if colony["current_energy"] + total_energy > colony["max_energy_capacity"]:
      print("A produção de energia excede a capacidade máxima da colônia. Armazenando o excesso de energia...")
      colony["current_energy"] = colony["max_energy_capacity"]
    else:
      colony["current_energy"] += total_energy

    print(f"Reserva de energia atualizada: {colony['current_energy']} de {colony['max_energy_capacity']}")
    
    return
  
  print("Atenção: energia produzida é insuficiente para atender ao consumo da próxima semana.") 

  if colony["current_energy"] == 0:
    print("A colônia está sem reservas de energia para compensar o déficit.")
  else:
    print("Utilizando reservas de energia para compensar o déficit...")

  total_energy += colony["current_energy"]

  if total_energy >= 0:
    colony["current_energy"] = total_energy
  else:
    colony["current_energy"] = 0

  print(f"Reserva de energia utilizada, reserva restante: {colony['current_energy']}")

  if total_energy >= 0:
    return

  print("Desabilitando módulos de baixa prioridade para compensar o déficit energético...")

  energy_to_compensate = -total_energy
  priority_disabled = disable_modules(colony, energy_to_compensate)

  print(f"Módulos de prioridade {priority_disabled} foram desabilitados para compensar o déficit energético.")
  print("Módulos de prioridade máxima foram mantidos para garantir o funcionamento dos sistemas essenciais da colônia.")
  print("Recomenda-se aumentar a produção de energia ou reduzir o consumo para evitar futuros déficits energéticos.")