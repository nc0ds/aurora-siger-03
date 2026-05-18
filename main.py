"""
Estrutura principal da colônia
"""

# vento[i] gerou energia_eol[i]

historico_vento = [6.0, 8.0, 10.0, 9.0, 12.0, 7.0, 11.0]

historico_energia_eol = [15.0, 18.0, 22.0, 20.0, 26.0, 16.0, 24.0]

"""
Dados energéticos
"""

energetico ={
    "geracao_solar":35.0,
    "geracao_eolica":18.0,
    "consumo":48.0,
    "bateria":72.0
}


"""
Dados ambientais
"""

ambiental ={
    "temp_interna": 22.0,
    "temp_externa": -61.0,
    "vento_atual": 9.5
}


"""
Módulos Operacionais

prioridade:
1 = nunca desliga
3 = primeiro a desligar
"""


modulos ={

    "suporte_vida":{
        "status": "ativo",
        "consumo": 20.0,
        "prioridade": 1
    },

    "habitacao":{
        "status": "ativo",
        "consumo": 18.0,
        "prioridade": 2
    },

    "laboratorio":{
        "status": "ativo",
        "consumo": 10.0,
        "prioridade": 3
    }

}


"""
Hierarquia da colônia
"""

colonia ={

    "energetico":{

        "solar":{

            "geracao_atual": 35.0,

            "historico":[
                30.0,
                32.5,
                35.0,
                33.0,
                28.0,
                35.0,
                36.0
            ]
        },

        "eolico":{

            "geracao_atual": 18.0,

            "historico":historico_energia_eol
        }
    },

    "ambiental":{

        "temp_interna": 22.0,

        "temp_externa": -61.0,

        "vento_atual": 9.5,

        "historico_vento": historico_vento
    },

    "operacional": modulos
}


"""
Limiares do sistema
"""

bateria_critica = 20.0
bateria_atencao = 40.0
consumo_alto = 60.0

