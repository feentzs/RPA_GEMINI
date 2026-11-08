import keyboard
import mss
import time

# 1. COORDENADAS DOS RECEPTORES
X_ESQUERDA = 782
X_BAIXO = 906
X_CIMA = 1029
X_DIREITA = 1156

# 2. CONFIGURAÇÃO DA LEITURA 
Y_SETAS_ORIGINAL = 112
OFFSET = 35 
Y_LEITURA = Y_SETAS_ORIGINAL + OFFSET 

TECLAS = {
    'esquerda': 'd',
    'baixo': 'f',
    'cima': 'j',
    'direita': 'k'
}

estado_teclas = {
    'esquerda': False,
    'baixo': False,
    'cima': False,
    'direita': False
}

ultima_vez_visto = {
    'esquerda': 0.0,
    'baixo': 0.0,
    'cima': 0.0,
    'direita': 0.0
}

TOLERANCIA_SOLTAR = 0.08 

regiao_captura = {
    "top": Y_LEITURA - 5, 
    "left": X_ESQUERDA - 5, 
    "width": (X_DIREITA - X_ESQUERDA) + 10, 
    "height": 10
}

print(f"Bot Iniciado Pressione 'ESC' para parar.")
time.sleep(2) 

with mss.mss() as sct:
    while not keyboard.is_pressed('esc'):
        tela = sct.grab(regiao_captura)

        pixel_esq = tela.pixel(5, 5)
        pixel_bai = tela.pixel(X_BAIXO - X_ESQUERDA + 5, 5)
        pixel_cim = tela.pixel(X_CIMA - X_ESQUERDA + 5, 5)
        pixel_dir = tela.pixel(X_DIREITA - X_ESQUERDA + 5, 5)

        r_esq, g_esq, b_esq = pixel_esq 
        r_bai, g_bai, b_bai = pixel_bai 
        r_cim, g_cim, b_cim = pixel_cim 
        r_dir, g_dir, b_dir = pixel_dir 

        agora = time.time()
        
        # ================= ESQUERDA (Roxo)  =================
        if r_esq > 140 and b_esq > 120 and g_esq < 120:
            ultima_vez_visto['esquerda'] = agora 
            if not estado_teclas['esquerda']:
                keyboard.press(TECLAS['esquerda'])
                estado_teclas['esquerda'] = True
        else:
            if estado_teclas['esquerda'] and (agora - ultima_vez_visto['esquerda'] >= TOLERANCIA_SOLTAR):
                keyboard.release(TECLAS['esquerda'])
                estado_teclas['esquerda'] = False

        # ================= BAIXO (Ciano) =================
        if g_bai > 160 and b_bai > 160 and r_bai < 120:
            ultima_vez_visto['baixo'] = agora
            if not estado_teclas['baixo']:
                keyboard.press(TECLAS['baixo'])
                estado_teclas['baixo'] = True
        else:
            if estado_teclas['baixo'] and (agora - ultima_vez_visto['baixo'] >= TOLERANCIA_SOLTAR):
                keyboard.release(TECLAS['baixo'])
                estado_teclas['baixo'] = False

        # ================= CIMA (Verde) =================
        if g_cim > 180 and r_cim < 120 and b_cim < 120:
            ultima_vez_visto['cima'] = agora
            if not estado_teclas['cima']:
                keyboard.press(TECLAS['cima'])
                estado_teclas['cima'] = True
        else:
            if estado_teclas['cima'] and (agora - ultima_vez_visto['cima'] >= TOLERANCIA_SOLTAR):
                keyboard.release(TECLAS['cima'])
                estado_teclas['cima'] = False

        # ================= DIREITA (Vermelho) =================
        if r_dir > 180 and g_dir < 120 and b_dir < 120:
            ultima_vez_visto['direita'] = agora
            if not estado_teclas['direita']:
                keyboard.press(TECLAS['direita'])
                estado_teclas['direita'] = True
        else:
            if estado_teclas['direita'] and (agora - ultima_vez_visto['direita'] >= TOLERANCIA_SOLTAR):
                keyboard.release(TECLAS['direita'])
                estado_teclas['direita'] = False

        time.sleep(0.001)