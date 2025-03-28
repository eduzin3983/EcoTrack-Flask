"""
Módulo de algoritmos para cálculo e classificação dos scores de sustentabilidade.
"""

# Mapeamento para pontuação do transporte
TRANSPORTE_MAP = {
    "caminhada": 0.0,
    "bicicleta": 0.2,
    "carona_compartilhada": 0.4,
    "transporte_publico": 0.5,
    "carro_eletrico": 0.7,
    "carro": 1.0
}

# Funções para calcular os scores individuais

def score_agua(agua):
    """
    Calcula o score de água baseado na quantidade consumida.
    
    Parâmetros:
        agua (float): Quantidade de água consumida.
    
    Retorna:
        float: Score normalizado entre 0 e 1.
    """
    return min(agua / 200, 1)

def score_energia(energia):
    """
    Calcula o score de energia com base no consumo.
    
    Parâmetros:
        energia (float): Consumo de energia em kWh.
    
    Retorna:
        float: Score normalizado entre 0 e 1.
    """
    return min(energia / 10, 1)

def score_residuos(residuos):
    """
    Calcula o score de resíduos com base na quantidade gerada.
    
    Parâmetros:
        residuos (float): Quantidade de resíduos gerados.
    
    Retorna:
        float: Score normalizado entre 0 e 1.
    """
    return min(residuos / 2, 1)

def score_transporte(transporte):
    """
    Retorna o score do transporte utilizado com base em um mapeamento.
    
    Parâmetros:
        transporte (str): Meio de transporte utilizado.
    
    Retorna:
        float: Score do transporte, conforme definido no TRANSPORTE_MAP.
    """
    return TRANSPORTE_MAP.get(transporte, 1.0)

# Função para calcular o score total do registro

def calcular_score_registro(agua, energia, residuos, transporte):
    """
    Calcula o score total de um registro diário, combinando os scores de água, energia, resíduos e transporte.
    
    Cada variável tem peso igual (0.25).
    
    Parâmetros:
        agua (float): Consumo de água.
        energia (float): Consumo de energia.
        residuos (float): Quantidade de resíduos.
        transporte (str): Meio de transporte utilizado.
    
    Retorna:
        float: Score total do registro.
    """
    W_AGUA = W_ENERGIA = W_RESIDUOS = W_TRANSPORTE = 0.25
    s_agua = score_agua(agua)
    s_energia = score_energia(energia)
    s_residuos = score_residuos(residuos)
    s_transp = score_transporte(transporte)
    return (W_AGUA * s_agua +
            W_ENERGIA * s_energia +
            W_RESIDUOS * s_residuos +
            W_TRANSPORTE * s_transp)

# Funções para classificar os scores

def classificar_score(score):
    """
    Classifica o score total em categorias de impacto.
    
    Parâmetros:
        score (float): Score total calculado.
    
    Retorna:
        str: "Baixo Impacto", "Médio Impacto" ou "Alto Impacto" conforme o valor do score.
    """
    if score <= 0.3:
        return "Baixo Impacto"
    elif score <= 0.6:
        return "Médio Impacto"
    else:
        return "Alto Impacto"

def classificar_variavel_agua(agua):
    """
    Classifica o consumo de água com base em seu score normalizado.
    
    Parâmetros:
        agua (float): Quantidade de água consumida.
    
    Retorna:
        str: "Baixo", "Médio" ou "Alto" de acordo com o score.
    """
    s = score_agua(agua)
    if s <= 0.3:
        return "Baixo"
    elif s <= 0.6:
        return "Médio"
    else:
        return "Alto"

def classificar_variavel_energia(energia):
    """
    Classifica o consumo de energia com base em seu score normalizado.
    
    Parâmetros:
        energia (float): Consumo de energia.
    
    Retorna:
        str: "Baixo", "Médio" ou "Alto" conforme o score.
    """
    s = score_energia(energia)
    if s <= 0.3:
        return "Baixo"
    elif s <= 0.6:
        return "Médio"
    else:
        return "Alto"

def classificar_variavel_residuos(residuos):
    """
    Classifica a geração de resíduos com base em seu score normalizado.
    
    Parâmetros:
        residuos (float): Quantidade de resíduos gerados.
    
    Retorna:
        str: "Baixo", "Médio" ou "Alto" conforme o score.
    """
    s = score_residuos(residuos)
    if s <= 0.3:
        return "Baixo"
    elif s <= 0.6:
        return "Médio"
    else:
        return "Alto"

def classificar_variavel_transporte(transporte_score):
    """
    Classifica o score do transporte em categorias.
    
    Parâmetros:
        transporte_score (float): Score do transporte (valor numérico entre 0 e 1).
    
    Retorna:
        str: "Baixo", "Médio" ou "Alto" conforme o score.
    """
    if transporte_score <= 0.3:
        return "Baixo"
    elif transporte_score <= 0.6:
        return "Médio"
    else:
        return "Alto"
