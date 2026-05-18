# Exibe a estrutura da colonia

def mostrar_colonia(colonia):

    print("\n------ DADOS DA COLÔNIA --------")
    print(colonia)


# Calcula a geração total

def calcular_geracao_total(colonia):

    solar = colonia["energetico"]["solar"]["geracao_atual"]
    eolico = colonia["energetico"]["eolico"]["geracao_atual"]
    return solar + eolico


# Calcula o consumo total

def calcular_consumo_total(modulos):

    total = 0
    for modulo in modulos.values():
        if modulo["status"] == "ativo":
            total += modulo["consumo"]

    return total


# Alertas ambientais




# Analise energética



   # Risco energético

    


    # Alertas da bateria

    

   # Modo economia

    


# Desligamento por prioridade




# Regressão linear




   
# Previsao de energia eolica


    
