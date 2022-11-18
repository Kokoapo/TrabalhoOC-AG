from random import randint
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap
import numpy as np

# Classe com construtor para criar as Pops
class Pops:
    def __init__(self, x, y, fitness):
        self.x = x
        self.y = y
        self.fitness = fitness

#Função Fitness
def fitnessFunc(x, y): return x ** 5 - 10 * x ** 3 + 30 * x - y ** 2 + 21 * y

#Total: 9 Bits
#0: Sinal       (1 Bit)
#1-2: Inteiro   (2 Bits)
#3-8: Fração    (6 Bits)
#Limite: [-2,5 ; 2,5]

#Checa se os Genes estão no Limite e Caso Negativo converte eles para o Limite
def checkLimit(arr):
    res = arr.copy()

    if res[1] == 1: res[2] = 0
    if res[1] == 1 and res[3] == 1:
        for i in range(PALAVRA_SIZE - (TAMANHO_FRAC - TAMANHO_INT)):
            res[i + (TAMANHO_FRAC - TAMANHO_INT)] = 0

    return res

#Gera Genes X e Y em Binário
def genBinary():
    res = list()

    for i in range(PALAVRA_SIZE):
        bit = randint(0, 1)
        res.append(bit)

    res = checkLimit(res)
    return res

#Converter Binário - Float
def convertFloat(strBin, exp_size, frc_size):
    aux_res_exp = 0
    aux_res_frc = 0

    for i in range(exp_size):
        aux = int(strBin[i + 1])
        aux_res_exp += aux * (2 ** (exp_size - 1 - i))
    #if aux_res_exp >= 3: aux_res_exp = 2
    
    for i in range(frc_size):
        aux = int(strBin[i + exp_size + 1])
        aux_res_frc += aux * (2 ** ((i + 1) * -1))
    #if aux_res_frc > 0.5 and aux_res_exp >= 2: aux_res_frc = 0.5

    res = aux_res_exp + aux_res_frc
    if strBin[0] == 1: res *= -1

    return res

#Gera as Pops da Primeira Geração
def genPops():
    count = 0
    while count < N_POPS:
        genX = genBinary()
        genY = genBinary()
        floatX = convertFloat(genX, TAMANHO_INT, TAMANHO_FRAC)
        floatY = convertFloat(genY, TAMANHO_INT, TAMANHO_FRAC)
        pop = Pops(genX, genY, fitnessFunc(floatX, floatY))
        main_pops.append(pop)
        print("Pop " + str(count) + " " + str(main_pops[count].x) + " ", str(main_pops[count].y) + " " + str(main_pops[count].fitness))
        count = count + 1

#Seleciona 5 Pops (Sistema de Ranking) 2 Vezes (Sem Repetições) e usa as 2 Pops selecionadas para serem os Pais
def selectPops():
    selected = [Pops([], [], 0), Pops([], [], 0)]
    higher_rank_pos = [-1, -1]
    
    for i in range(2):
        higher_rank = -100
        for j in range(SELECT_NUM):
            pos = randint(0, 99)
            choosen = main_pops[pos]
            if choosen.fitness >= higher_rank and pos != higher_rank_pos[i]:
                selected[i] = choosen
                higher_rank = choosen.fitness
                higher_rank_pos[i] = pos

    crossingOver(selected)

#Realiza o CrossingOver entre os 2 Pais (Verifica se o cruzamento ocorre e em caso negativo simplesmente passa os pais adiante)
#Também realiza a mutação dos bits quando necessário
def crossingOver(parents):
    x1 = []
    y1 = []
    x2 = []
    y2 = []

    cruz = randint(0, 99)
    if cruz <= TX_CRUZAMENTO:
        for i in range(PONTO_CRUZAMENTO_1):
            x1.append(parents[0].x[i])
            y1.append(parents[0].y[i])

            x2.append(parents[1].x[i])
            y2.append(parents[1].y[i])
        for i in range(PONTO_CRUZAMENTO_2 - PONTO_CRUZAMENTO_1):
            x1.append(parents[1].x[i + PONTO_CRUZAMENTO_1])
            y1.append(parents[1].y[i + PONTO_CRUZAMENTO_1])

            x2.append(parents[0].x[i + PONTO_CRUZAMENTO_1])
            y2.append(parents[0].y[i + PONTO_CRUZAMENTO_1])
    else:
        x1 = parents[0].x.copy()
        y1 = parents[0].y.copy()
        x2 = parents[1].x.copy()
        y2 = parents[1].y.copy()

    for i in x1:
        mutX1 = randint(0, 99)
        mutX2 = randint(0, 99)
        mutY1 = randint(0, 99)
        mutY2 = randint(0, 99)
        if mutX1 <= TX_MUTACAO:
            if x1[i] == 0: x1[i] = 1 
            else: x1[i] = 0 
        if mutY1 <= TX_MUTACAO:
            if y1[i] == 0: y1[i] = 1 
            else: y1[i] = 0 
        if mutX2 <= TX_MUTACAO:
            if x2[i] == 0: x2[i] = 1 
            else: x2[i] = 0 
        if mutY2 <= TX_MUTACAO:
            if y2[i] == 0: y2[i] = 1 
            else: y2[i] = 0 
    
    x1 = checkLimit(x1)
    x2 = checkLimit(x2)
    y1 = checkLimit(y1)
    y2 = checkLimit(y2)

    filho1 = Pops(x1.copy(), y1.copy(), fitnessFunc(convertFloat(x1, TAMANHO_INT, TAMANHO_FRAC), convertFloat(y1, TAMANHO_INT, TAMANHO_FRAC)))
    filho2 = Pops(x2.copy(), y2.copy(), fitnessFunc(convertFloat(x2, TAMANHO_INT, TAMANHO_FRAC), convertFloat(y2, TAMANHO_INT, TAMANHO_FRAC)))
    next_pops.append(filho1)
    next_pops.append(filho2)

#Seleciona Indivíduos (baseado no Elitismo) para ir para a próxima População
def elitismo():
    elitPop = Pops([], [], -100)
    for i in range(N_POPS):
        if main_pops[i].fitness > elitPop.fitness: elitPop = main_pops[i]

    elitIndex = randint(0, 49)
    next_pops[elitIndex] = elitPop

#Transfere Pops da lista secundária para a lista principal
def transferPops():
    main_pops.clear()
    for i in range(N_POPS):
        main_pops.append(next_pops[i])
    next_pops.clear()

#Usa MatPlotLib para fazer um gráfico (Ainda não funcionando)
def plotFinal():
    x = []
    y = []
    for i in range(N_POPS):
        x.append(convertFloat(main_pops[i].x, TAMANHO_INT, TAMANHO_FRAC))
        y.append(convertFloat(main_pops[i].y, TAMANHO_INT, TAMANHO_FRAC))
                

    fig, ax = plt.subplots()
    colors = np.random.randint(100, size=(100))
    sizes = 10 * np.random.randint(100, size=(100))
    ax.scatter(x, y, c=colors, s=sizes, alpha=0.5, cmap='nipy_spectral')

    ax.set_xlabel('Valor X', fontsize=15)
    ax.set_ylabel('Valor Y', fontsize=15)
    ax.set_title('Pops Última Geração')

    plt.show()

    input('')

#Main Method
#Gera Primeira População e Controla o Número de Vezes que o AG irá rodar
def main():
    count = 0

    genPops()
    while count < N_ITERACOES_MAX:
        print('Geração ' + str(count + 1))

        for i in range(int(N_POPS/2)):
            selectPops()
        elitismo()
        transferPops()

        for i in range(N_POPS):
            print("Pop " + str(i) + " : " + str(main_pops[i].x) + " " + str(main_pops[i].y) + " " + str(main_pops[i].fitness))

        count = count + 1
    
    #plotFinal() Não Funcionando Ainda

# CONSTANTES:
main_pops = list()
next_pops = list()
N_POPS = 100  # Número da população
N_ITERACOES_MAX = 100  # Máximo de iterações
TX_CRUZAMENTO = 80  # Taxa de cruzamento
TX_MUTACAO = 3  # Taxa de mutação
SELECT_NUM = 5 # Número de indivíduos a serem selecionados
PONTO_CRUZAMENTO_1 = 4 # Primeiro Ponto para o Cruzamento (dois pontos fixos)
PONTO_CRUZAMENTO_2 = 9 # Segundo Ponto para o Cruzamento (dois pontos fixos)
TAMANHO_INT = 2 # Tamanho da Parte Inteira da Palavra Binária
TAMANHO_FRAC = 6 # Tamanho da Parte Fracionária da Palavra Binária
PALAVRA_SIZE = 9 # Tamanho Total da Palavra Binária

main()