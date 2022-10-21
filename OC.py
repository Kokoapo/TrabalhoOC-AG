"""
-> TRABALHO DE OTIMIZAÇÃO COMBINATÓRIA

-> Professor: André Luiz Brun

-> Grupo 18:
    — Gabriel Henrique Schumacher;
    — Pedro Henrique de Oliveira Berti;
    — Vinicius Visconsini Diniz.

-> Dados do exercício:
    — Função de otimização: z = x⁵ - 10x³ + 30x - y² + 21y
    — Intervalos: x: [-2.5, 2.5]
                  y: [-2.5, 2.5]
    — Valores base: x = 1.126033
                    y = 2.5
                    z = 67.56377

-> Métodos de codificação:
    — Codificação: binária;
    — Método de seleção: classificação (ranking);
    — Método de cruzamento: dois pontos fixos;
    — Método de mutação: binária;
    — Elitismo: 1 indivíduo da população.
"""


from numpy import random


def cria_pop_inicial(n_pop_inicial, n_genes):
    """
    FUNÇÃO QUE GERA A POPULAÇÃO INICIAL
    Utilizando a função randint():
        0 ≥ valor mínimo
        2 ≥ valor máximo + 1
        n_genes ≥ quantidade de valores gerados
    Depois, convertemos os valores gerados para o formato de lista usando 'tolist()' e, por fim,
    atribuímos essa lista à nossa variável 'aux.' usando 'append()'
    PS: usamos 'n_genes * 2', pois precisamos criar um cromossomo para X e um para Y.
    :param n_pop_inicial: quantidade de cromossomos a ser gerada.
    :param n_genes: quantidade de genes em cada cromossomo.
    :return: população em binário
    """
    populacao = []
    for i in range(n_pop_inicial):
        populacao.append(random.randint(0, 2, n_genes * 2).tolist())
    return populacao


def fitness(v):
    """
    FUNÇÃO QUE CALCULA O FITNESS
    Função que apenas retorna o resultado da equação com x e y passados como parâmetro.
    :param v: vetor contendo os valores para x e y.
    :return: resultado.
    """
    x = v[0]
    y = v[1]
    return x ** 5 - 10 * x ** 3 + 30 * x - y ** 2 + 21 * y


def converte_decimal(n_genes, cromossomo):
    """
    FUNÇÃO QUE CONVERTE OS VALORES DE BINÁRIO PARA DECIMAL.
    :param n_genes: número de genes.
    :param cromossomo: cromossomo contendo os valores de x e y.
    :return: vetor contendo os valores convertidos para base 10
    """
    populacao_decimal = []  # Cria o vetor para armazenar os valores em base 10
    for i in range(2):  # Como cada cromossomo contém o valor de x e y, o parâmetro 'i' identifica qual estamos usando
        x, y = i * n_genes, (i * n_genes) + n_genes  # Identifica onde devemos 'quebrar' o vetor para separar
        # os valores de x e y
        vetor = cromossomo[x:y]
        print(vetor)
        string = ''.join([str(s) for s in vetor])  # Converte ex: [0, 1, 1, 0] para 0110
        print(string)
        decimal = int(string, 2)  # Converte o valor em base 2 para base 10 ex: 0110 para 6
        print(decimal)
        decimal = converte_intervalo(N_GENES, LIMITE_X, LIMITE_Y, decimal, i)  # Função que converte o valor decimal
        # encontrado para o intervalo fornecido no enunciado
        print(decimal)
        populacao_decimal.append(decimal)
    return populacao_decimal


def converte_intervalo(n_genes, lim_x, lim_y, valor, i):
    """
    FUNÇÃO QUE TRANSFORMA O VALOR DADO PARA O INTERVALO FORNECIDO NO ENUNCIADO.
    :param n_genes: número de genes, usamos para calcular o valor decimal máximo.
    :param lim_x: limites de x.
    :param lim_y: limites de y.
    :param valor: valor a ser convertido para o intervalo.
    :param i: identificador para saber se estamos usando intervalo de x ou y
    :return: valor convertido para o intervalo
    """
    maior_decimal = 2 ** n_genes - 1  # Calcula o máximo decimal dado o número de genes em binário.
    #  Ex: se o número de genes for 8, o máximo em base 2 será '11 111 111', em base 10 será 2⁸ = 256.
    #  Como começamos a contagem em 0, o intervalo é 0 – 255, por isso subtraímos 1
    if i == 0:
        cromossomo = lim_x[0] + (valor / maior_decimal) * (lim_x[1] - lim_x[0])
    else:
        cromossomo = lim_y[0] + (valor / maior_decimal) * (lim_y[1] - lim_y[0])
    return cromossomo


def elite(populacao):
    maior = 0
    for i in range(len(populacao)):
        if fitness(populacao[i]) > maior:
            maior = fitness(populacao[i])
    return maior


def main():
    populacao_inicial = cria_pop_inicial(N_POPULACAO_INICIAL, N_GENES)
    print(populacao_inicial)
    populacao_decimal = [converte_decimal(N_GENES, x) for x in populacao_inicial]
    print(populacao_decimal)
    # fit, fit_inicial = 0, fitness(populacao_decimal[0])
    # print(fit)
    # print(fit_inicial)
    a = elite(populacao_decimal)
    print(a)


# CONSTANTES:
LIMITE_X = [-2.5, 2.5]  # Limites de x
LIMITE_Y = [-2.5, 2.5]  # Limites de y
N_POPULACAO_INICIAL = 5  # Número da população inicial
N_ITERACOES_MAX = 100  # Máximo de iterações
N_GENES = 8  # Número de genes em 1 cromossomo
TX_CRUZAMENTO = 0.8  # Taxa de cruzamento
TX_MUTACAO = 0.03  # Taca de mutação
main()

'''
PASSOS:
1 - CRIA POPULAÇÃO
2 - CALCULA FITNESS INICIAL
    LOOP:
    - MANTÉM ELITE
    - SELECIONA PAIS
    - CRUZAMENTO
    - MUTAÇÃO
'''
