# Micro-Osciloscope IOT
# IoT Module 1
# Autores:
# - Afonso Alemão
# - Rui Daniel
# - Tomás Fonseca
# Data: 26/04/2022

# módulo de interface com o display
import T_Display
# módulo de funções matemáticas
import math            
import time

# Inicializações de variáveis globais
# Lista com 240 floats, de modo a possuir 240 pontos a imprimir no ecrã
# visto que o display TFT tem uma resolução de 240 pixéis na horizontal
pontos_volt = [0.0] * 240     
# Variável apenas usada para display da calibração                     
width = 160
# Ordenada máxima. Usada para centrar os pontos na grelha.
height = 134
# Grelha possui 6 divisões verticais e 10 divisões horizontais
N_div_verticais = 6
N_div_horizontais = 10

# Função de leitura dos valores do ADC e conversão para tensão de entrada real
# Argumentos de entrada:
# - pontos: número de pontos a ler no ADC
# - escala_horizontal: valor temporal de uma divisão horizontal
# Argumentos de saída:
# - pontos_adc: pontos lidos pelo ADC
# - pontos_volt: valores de tensão de entrada
def read_and_convert(pontos, escala_horizontal):
    if escala_horizontal == 5:
        # Lê pontos do ADC em 50 ms
        pontos_adc = tft.read_adc(pontos, 50)
    elif escala_horizontal == 10:
        # Lê pontos do ADC em 100 ms
        pontos_adc = tft.read_adc(pontos, 100)
    elif escala_horizontal == 20:
        # Lê pontos do ADC em 200 ms
        pontos_adc = tft.read_adc(pontos, 200)
    else:
        # Lê pontos do ADC em 500 ms
        pontos_adc = tft.read_adc(pontos, 500)

    # Inicialização de variáveis a calcular - irrelevante neste trabalho
    # Vmax = 0
    # Vmin = 0
    # Vmed = 0

    for n in range(pontos):
        # Para cada ponto lido pelo ADC, convertemos o valor digital lido 
        # pelo ADC (pontos_adc[n]) em Volt (V_ADC)

        # Usado para testes no laboratório: Depois da calibração
        # V =  0.0004466 * pontos_adc[n] + 0.1027499
        # Usado para testes no simulador: Antes da calibração
        V =  0.00044028 * pontos_adc[n] + 0.091455  

        # Conversão de V_ADC em Vi
        # Tensão entrada de referência de 1V
        V = V - 1
        # Entra com o efeito do div. resistivo
        V = V / fator

        # pontos_volt guarda a tensão de entrada real (Vi)
        pontos_volt[n] = V

        # Cálculos auxiliares para obtenção dos valores máximo, mínimo e
        # médio de tensão: não relevante para este trabalho
        # Caso seja o primeiro ponto, inicializamos as variáveis com o 
        # seu valor de tensão
        # if n == 0:                                 
        #     Vmax = Vmin = Vmed = V
        # else:
        #     Vmed += V
        #     if V > Vmax: Vmax = V
        #     if V < Vmin: Vmin = V
    # Para obtenção do valor médio, o somatório das tensões de entrada é
    # dividido pelo número de amostras - irrelevante neste trabalho
    # Vmed /= pontos

    return [pontos_adc, pontos_volt]

# Função para realizar amostras e médias - usada para calibração
# Argumentos de entrada:
# - num_amostras: número de amostras de 100 pontos a serem 
#                 utilizadas para o cálculo da média
# def media_amostras(num_amostras):
    
    # Apaga parte direita do display exceto ícone WiFi
    # tft.display_set(tft.BLACK, width, 0, 240 - width, height - 16)
    # soma = 0
    # for n in range(num_amostras):
        # Lê 100 pontos do ADC em 50 ms
        # pontos_adc = tft.read_adc(100, 50)
        # for j in range(100):
            # soma += pontos_adc[j]
    
    # Para obtenção do valor médio, o somatório dos pontos lidos do ADC é
    # dividido pelo número total de pontos
    # media = soma / (100 * num_amostras)

    # Escreve valores no display
    # tft.display_write_str(tft.Arial16, "media", width + 5, 90)
    # tft.display_write_str(tft.Arial16, "%d" % num_amostras, width + 5, 70)
    # tft.display_write_str(tft.Arial16, "amostras", width + 5, 50)
    # tft.display_write_str(tft.Arial16, "%.2f" % media, width + 5, 30)


# Programa principal (main)

# Fator do divisor resistivo constituído por R1 e por R5 + R6 
# caso Q1 a conduzir e Q2 ao corte
fator = 1 / 29.3

# Instância um objeto da classe TFT
tft = T_Display.TFT()

# Por defeito, no arranque do programa são utilizados os seguintes valores:
# Escala vertical = 2 V / div; Escala horizontal = 5 ms / div
escala_vertical = 2
escala_horizontal = 5

while True:
    # Apaga display
    tft.display_set(tft.BLACK, 0, 0, 240, 135)  

    # Insere no display uma grelha tendo em vista apresentar a forma de onda, 
    # com 10 intervalos na horizontal e 6 na vertical, utilizando todo o display 
    # exceto um espaço de 16 pixéis situado no topo do ecrã. 
    tft.display_write_grid(0, 0, 240, 135 - 16, N_div_horizontais, N_div_verticais, tft.GREY1, tft.GREY2)

    # Na horizontal:
    #   240 pixéis corresponde a N_div_horizontais * escala_horizontal (escala_horizontal 
    #   por divisão) - Cada pixel: tempo_pixel
    #   tempo_pixel = N_div_horizontais * escala_horizontal / 240

    # Na vertical:
    #   134 pixéis corresponde a 6 * escala_vertical (escala_vertical por divisão): 
    #   Cada volt: (134/(6 * escala_vertical)) pixéis

    x = []
    y = []

    # Lê os valores do ADC e obtém tensão de entrada real para cada ponto
    [pontos_adc, pontos_volt] = read_and_convert(240, escala_horizontal)

    # Tendo em vista o display da tensão na grelha, são criados os 
    # pontos (x, y) a serem imprimidos no gráfico.
    for n in range(len(pontos_volt)):
        # t = n * tempo_pixel
        volt = pontos_volt[n]

        # Para o cálculo da coordenada y de cada ponto, consideramos que o valor y = 0 está a 
        # meio da grelha, ou seja, em (height - 16) / 2. A partir desta referência, são calculadas 
        # a coordenada y dos restantes pontos de forma a apresentar a tensão pretendida de acordo 
        # com a escala vertical
        pixel = (height - 16) / 2 + ((height - 16) / (6 * escala_vertical)) * volt

        # Coordenada x de cada ponto
        x.append(n)

        # Assegurar que não são imprimidos pontos fora da grelha (na vertical):
        # Caso estes excedam o limite superior (ou inferior) da grelha, serão imprimidos
        # neste limite. Utilizámos este método, pois é desta forma que funciona o osciloscópio 
        # utilizado nos trabalhos de laboratórios anteriores.
        if pixel > 135 - 16:
            pixel = 135 - 17
        if pixel < 0:
            pixel = 0
        y.append(round(pixel))

    # Imprime a tensão de entrada no ecrã
    tft.display_nline(tft.YELLOW, x, y)

    # É imprimido num espaço com uma altura de 16 pixéis situado na parte de cima 
    # do display informação sobre as escalas atuais (vertical e horizontal) e sobre
    # o estado da ligação Wi-Fi.
    str1 = "y : " + str(escala_vertical) + " V / div"
    str2 = "x : " + str(escala_horizontal) + " ms / div"
    tft.display_write_str(tft.Arial16, str1, 5, 135 - 15)
    tft.display_write_str(tft.Arial16, str2, 115, 135 - 15)
    tft.set_wifi_icon(240 - 16, 135 - 16)

    # Ciclo principal do programa
    # Working é um método que devolve True enquanto o programa está a correr e devolve
    # False quando o utilizador acionar o menu exit ou clicar para fechar a janela do programa.
    while tft.working():
        # Lê estado dos botões           
        but = tft.readButton()                          
        if but != tft.NOTHING:
            # Houve um botão que foi pressionado
            print("Button pressed:", but)

            # Botão 1 click rápido - Nova leitura e representação da forma de onda;
            if but == 11:                               
                break

            # Botão 1 click lento - Envia por mail um ficheiro .csv com os pontos adc 
            # outro ficheiro .csv com os pontos volt obtidos
            if but == 12:
                tft.send_mail(pontos_adc, 
                "tomas.mvf@gmail.com,afonso.alemao@tecnico.ulisboa.pt,ruipcdaniel@tecnico.ulisboa.pt")
                tft.send_mail(pontos_volt, 
                "tomas.mvf@gmail.com,afonso.alemao@tecnico.ulisboa.pt,ruipcdaniel@tecnico.ulisboa.pt")
            
            # Botão 2 click rápido – Altera a escala vertical, passando para a
            # escala imediatamente acima e de forma circular. De seguida, nova leitura 
            # e representação da forma de onda;
            if but == 21:                                     
                if escala_vertical == 1:
                    escala_vertical = 2
                elif escala_vertical == 2:
                    escala_vertical = 5
                elif escala_vertical == 5:
                    escala_vertical = 10
                elif escala_vertical == 10:
                    escala_vertical = 1
                break
            
            # Botão 2 click lento (22) – Altera a escala horizontal, passando para a 
            # escala imediatamente acima e de forma circular. De seguida, nova leitura 
            # e representação da forma de onda;
            if but == 22:                                     
                if escala_horizontal == 5:
                    escala_horizontal = 10
                elif escala_horizontal == 10:
                    escala_horizontal = 20
                elif escala_horizontal == 20:
                    escala_horizontal = 50
                elif escala_horizontal == 50:
                    escala_horizontal = 5
                break
                