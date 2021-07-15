import pygame as pg, sys
from pygame.locals import *
import time

# Incializando as variaveis globais
XO = 'x'
vencedor = None
empate = False
largura = 400
altura = 400
branco = (255, 255, 255)
cor_linha = (10, 10, 10)

# Jogo da Velha 3x3
jogo_velha = [[None] * 3, [None] * 3, [None] * 3]

# Incializando janela do Pygame
pg.init()
fps = 30
CLOCK = pg.time.Clock()
screen = pg.display.set_mode((largura, altura + 100), 0, 32)
pg.display.set_caption("Jogo da Velha")

# Carregando Imagens
tela_inicial = pg.image.load('jogo_velha.jpg')
x_img = pg.image.load('x.png')
o_img = pg.image.load('o.png')

# Renderizando Imagens
x_img = pg.transform.scale(x_img, (80, 80))
o_img = pg.transform.scale(o_img, (80, 80))
tela_inicial = pg.transform.scale(tela_inicial, (largura, altura + 100))


# Função para iniciar o jogo
def iniciar_jogo():

    screen.blit(tela_inicial, (0, 0))
    pg.display.update()
    time.sleep(1)
    screen.fill(branco)

    # Desenhando linhas verticais
    pg.draw.line(screen, cor_linha, (largura / 3, 0), (largura / 3, altura), 7)
    pg.draw.line(screen, cor_linha, (largura / 3 * 2, 0), (largura / 3 * 2, altura), 7)

    # Desenhando linhas horizontais
    pg.draw.line(screen, cor_linha, (0, altura / 3), (largura, altura / 3), 7)
    pg.draw.line(screen, cor_linha, (0, altura / 3 * 2), (largura, altura / 3 * 2), 7)
    checar_vez()


# Função para checar a vez e imparte
def checar_vez():

    global empate

    if vencedor is None:
        messagem = "Vez do " + XO.upper()
    else:
        messagem = vencedor.upper() + " venceu!"
    if empate:
        messagem = 'Velha!'

    fonte = pg.font.Font(None, 30)
    texto = fonte.render(messagem, 1, (255, 255, 255))

    # Copia a mensagem renderizada no quadro
    screen.fill((0, 0, 0), (0, 400, 500, 100))
    text_rend = texto.get_rect(center=(largura / 2, 500 - 50))
    screen.blit(texto, text_rend)
    pg.display.update()


# Função para verificar vencendor
def verificar_vencendor():

    global jogo_velha, vencedor, empate

    # Verifique se há linhas vencedoras
    for row in range(0, 3):
        if ((jogo_velha[row][0] == jogo_velha[row][1] == jogo_velha[row][2]) and (jogo_velha[row][0] is not None)):
            # Esta linha ganhou
            vencedor = jogo_velha[row][0]
            pg.draw.line(screen, (250, 0, 0), (0, (row + 1) * altura / 3 - altura / 6), \
                         (largura, (row + 1) * altura / 3 - altura / 6), 4)
            break

    # Verifca se há colunas vencedoras
    for col in range(0, 3):
        if (jogo_velha[0][col] == jogo_velha[1][col] == jogo_velha[2][col]) and (jogo_velha[0][col] is not None):
            # Esta coluna ganhou
            vencedor = jogo_velha[0][col]
            # Desenha linha vencedora
            pg.draw.line(screen, (250, 0, 0), ((col + 1) * largura / 3 - largura / 6, 0), \
                         ((col + 1) * largura / 3 - largura / 6, altura), 4)
            break

    # Verifica se há diagonal vencedora
    if (jogo_velha[0][0] == jogo_velha[1][1] == jogo_velha[2][2]) and (jogo_velha[0][0] is not None):
        # jogo ganho diagonalmente da esquerda para a direita
        vencedor = jogo_velha[0][0]
        pg.draw.line(screen, (250, 70, 70), (50, 50), (350, 350), 4)
    if (jogo_velha[0][2] == jogo_velha[1][1] == jogo_velha[2][0]) and (jogo_velha[0][2] is not None):
        # jogo ganho diagonalmente da direita para a esquerda
        vencedor = jogo_velha[0][2]
        pg.draw.line(screen, (250, 70, 70), (350, 50), (50, 350), 4)
    if all([all(row) for row in jogo_velha]) and vencedor is None:
        empate = True
    checar_vez()


# Função para desenhar X ou O
def desenhar_xo(lin, col):

    global jogo_velha, XO

    if lin == 1:
        posx = 30
    if lin == 2:
        posx = largura / 3 + 30
    if lin == 3:
        posx = largura / 3 * 2 + 30

    if col == 1:
        posy = 30
    if col == 2:
        posy = altura / 3 + 30
    if col == 3:
        posy = altura / 3 * 2 + 30

    jogo_velha[lin - 1][col - 1] = XO

    if XO == 'x':
        screen.blit(x_img, (posy, posx))
        XO = 'o'
    else:
        screen.blit(o_img, (posy, posx))
        XO = 'x'
    pg.display.update()


# Função para obter a coordenada do clique do mouse
def click_usuario():

    # obter coordenadas de clique do mouse
    x, y = pg.mouse.get_pos()

    # obter coluna de clique do mouse (1-3)
    if x < largura / 3:
        col = 1
    elif x < largura / 3 * 2:
        col = 2
    elif x < largura:
        col = 3
    else:
        col = None

    # obter linha de clique do mouse (1-3)
    if y < altura / 3:
        row = 1
    elif y < altura / 3 * 2:
        row = 2
    elif y < altura:
        row = 3
    else:
        row = None

    if row and col and jogo_velha[row - 1][col - 1] is None:
        global XO
        # desenhe x ou o na tela
        desenhar_xo(row, col)
        verificar_vencendor()


# Função para reinicar o jogo sempre que ouve vencedor ou imparte
def reniciar_jogo():

    global jogo_velha, vencedor, XO, empate

    time.sleep(3)
    XO = 'x'
    empate = False
    iniciar_jogo()
    vencedor = None
    jogo_velha = [[None] * 3, [None] * 3, [None] * 3]


iniciar_jogo()

# execute o loop do jogo
while True:
    for event in pg.event.get():
        if event.type == QUIT:
            pg.quit()
            sys.exit()
        elif event.type == MOUSEBUTTONDOWN:
            # the user clicked; place an X or O
            click_usuario()
            if vencedor or empate:
                reniciar_jogo()
    pg.display.update()
    CLOCK.tick(fps)
