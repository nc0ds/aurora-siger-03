from utils import get_random_history
from display import show_info

MAX_ENERGY_CAPACITY = 5000

colony = {
  "max_energy_capacity": MAX_ENERGY_CAPACITY,
  "current_energy": 1000,
  "sections": [
    {
      "id": 1,
      "type": "residential",
      "modules": [
        {
          "enabled": True,
          "type": "life_support",
          "energy_consumption": 400,
          "priority": 0,
        },
        {
          "enabled": True,
          "type": "hygiene",
          "energy_consumption": 300,
          "priority": 2,
        },
        {
          "enabled": True,
          "type": "entertainment",
          "energy_consumption": 600,
          "priority": 3,
        },
      ]
    },
    {
      "id": 2,
      "type": "medical",
      "modules": [
        {
          "enabled": True,
          "type": "surgery",
          "energy_consumption": 500,
          "priority": 0,
        },
        {
          "enabled": True,
          "type": "pharmacy",
          "energy_consumption": 200,
          "priority": 1,
        },
        {
          "enabled": True,
          "type": "emergency",
          "energy_consumption": 300,
          "priority": 0,
        }
      ]
    },
    {
      "id": 3,
      "type": "science",
      "modules": [
        {
          "enabled": True,
          "type": "research_lab",
          "energy_consumption": 700,
          "priority": 1,
        },
        {
          "enabled": True,
          "type": "data_analysis",
          "energy_consumption": 400,
          "priority": 2,
        },
        {
          "enabled": True,
          "type": "experiments",
          "energy_consumption": 500,
          "priority": 3,
        }
      ]
    },
    {
      "id": 4,
      "type": "logistics",
      "modules": [
        {
          "enabled": True,
          "type": "storage",
          "energy_consumption": 300,
          "priority": 1,
        },
        {
          "enabled": True,
          "type": "transport",
          "energy_consumption": 400,
          "priority": 2,
        },
        {
          "enabled": True,
          "type": "maintenance",
          "energy_consumption": 200,
          "priority": 3,
        }
      ]
    },
  ],
  "energy_generation_modules": [
    {
      "type": "solar",
      "input_history": get_random_history(),
      "generation_rate": 0.6
    },
    {
      "type": "eolian",
      "input_history": get_random_history(),
      "generation_rate": 0.8
    },
  ],
}

show_info(colony)

