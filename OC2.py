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
from random import randint
import numpy as np


def cria_pop_inicial(n_pop_inicial):
    populacao = list()
    for i in range(n_pop_inicial):
        cromossomo = list()
        for j in range(2):
            sinal = bin(randint(0, 1))[2:].zfill(1)
            inteiro = bin(randint(0, 2))[2:].zfill(2)
            decimal = bin(randint(0, 5000))[2:].zfill(13)
            x = ''.join([sinal, inteiro, decimal])
            cromossomo.append(x)
        populacao.append(cromossomo)
    return populacao


def fitness(v):
    x = v[0]
    y = v[1]
    return x ** 5 - 10 * x ** 3 + 30 * x - y ** 2 + 21 * y


def converte_decimal(populacao):
    cromossomo_decimal = list()
    for i in range(2):
        sinal = populacao[i][0]
        inteiro = int(populacao[i][1:3], 2)
        decimal = int(populacao[i][3:], 2)
        decimal = decimal * 10 ** -4
        valor = inteiro + decimal
        if sinal == 1:
            valor = valor * (-1)
        cromossomo_decimal.append(valor)
    return cromossomo_decimal


def elitismo(populacao):
    maior = fitness(populacao[0])
    maior_id = 0
    for i in range(len(populacao)):
        if fitness(populacao[i]) > maior:
            maior = fitness(populacao[i])
            maior_id = i
    return maior_id


def ordena_populacao(populacao, indices):
    aux = list()
    for x in indices:
        aux.append(populacao[x])
    return aux


def selecao(populacao, fit):
    seleciona_r = np.random.randint(len(populacao))
    for ix in np.random.randint(0, len(populacao), 2):
        if fit[ix] > fit[seleciona_r]:
            seleciona_r = ix
    return populacao[seleciona_r]


def cruzamento(p1, p2, tx):
    f1, f2 = p1, p2
    if np.random.rand() < tx:
        f1 = p1[:PONTO_CRUZAMENTO_1] + p2[PONTO_CRUZAMENTO_1:PONTO_CRUZAMENTO_2] + p1[:PONTO_CRUZAMENTO_2]
        f2 = p2[:PONTO_CRUZAMENTO_1] + p1[PONTO_CRUZAMENTO_1:PONTO_CRUZAMENTO_2] + p2[:PONTO_CRUZAMENTO_2]
    return [[f1, f2]]


def mutacao(cromossomo, tx_mutacao):
    bit = [int(x) for x in cromossomo]
    for i in range(len(bit)):
        if np.random.rand() < tx_mutacao:
            bit[i] = 1 - bit[i]


def main():
    populacao = cria_pop_inicial(N_POPULACAO_INICIAL)
    id_melhor, valor_melhor = 0, fitness(converte_decimal(populacao[0]))
    for i in range(N_ITERACOES_MAX):
        filhos = list()
        populacao_decimal = [converte_decimal(x) for x in populacao]
        valores_fitness = [fitness(x) for x in populacao_decimal]
        sorted_fitness = np.argsort(valores_fitness)
        populacao = ordena_populacao(populacao, sorted_fitness)
        populacao_decimal = ordena_populacao(populacao_decimal, sorted_fitness)
        valores_fitness = ordena_populacao(valores_fitness, sorted_fitness)
        filhos.append(populacao[0])
        for j in range(N_POPULACAO_INICIAL):
            if valores_fitness[j] > valor_melhor:
                id_melhor, valor_melhor = populacao[j], valores_fitness[j]
                print(f'NOVO MELHOR ENCONTRADO EM {populacao_decimal[j]} = {valores_fitness[j]}')
        selecionados = [selecao(populacao, valores_fitness) for _ in range(N_POPULACAO_INICIAL)]
        for j in range(0, N_POPULACAO_INICIAL-1):
            p1, p2 = selecionados[j][0], selecionados[j + 1][1]
            for c in cruzamento(p1, p2, TX_CRUZAMENTO):
                mutacao(c, TX_MUTACAO)
                filhos.append(c)
        populacao = filhos


# CONSTANTES:
LIMITE_X = [-2.5, 2.5]  # Limites de x
LIMITE_Y = [-2.5, 2.5]  # Limites de y
N_POPULACAO_INICIAL = 300  # Número da população inicial
N_ITERACOES_MAX = 1000  # Máximo de iterações
TX_CRUZAMENTO = 0.8  # Taxa de cruzamento
TX_MUTACAO = 0.03  # Taxa de mutação
PONTO_CRUZAMENTO_1 = 4
PONTO_CRUZAMENTO_2 = 8
main()
