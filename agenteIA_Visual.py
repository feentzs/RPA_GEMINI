import keyboard
import mss
import time
import pickle
import os
import numpy as np
import cv2
import ctypes
from sklearn.ensemble import RandomForestClassifier


VK_CAPS_LOCK = 0x14 

def luz_caps_ligada():
    
    return ctypes.windll.user32.GetKeyState(VK_CAPS_LOCK) & 1 == 1

def definir_luz(ligar):
    
    if luz_caps_ligada() != ligar:
        keyboard.send('caps lock')


X_ESQUERDA, X_DIREITA = 750, 1180  
Y_TOPO = 60                        
ALTURA = 500                       

TECLAS = ['d', 'f', 'j', 'k', 'space']

regiao_captura = {
    "top": Y_TOPO, 
    "left": X_ESQUERDA, 
    "width": (X_DIREITA - X_ESQUERDA), 
    "height": ALTURA
}

ARQUIVO_DADOS = "dataset_fnf_pro.pkl"
ARQUIVO_MODELO = "modelo_ia_fnf_pro.pkl"

def processar_visao(tela_mss):
    img = np.array(tela_mss)
    img_bgr = cv2.cvtColor(img, cv2.COLOR_BGRA2BGR)
    img_reduzida = cv2.resize(img_bgr, (50, 75))
    return img_reduzida.flatten()

def ler_teclado():
    return [
        1 if keyboard.is_pressed('d') else 0,
        1 if keyboard.is_pressed('f') else 0,
        1 if keyboard.is_pressed('j') else 0,
        1 if keyboard.is_pressed('k') else 0,
        1 if keyboard.is_pressed('space') else 0
    ]


def coletar_dados():
    print("\n[GRAVAÇÃO PRO] começa")
    print("-> Aperte 'TAB' para PAUSAR/CONTINUAR a gravação.")
    print("-> Aperte 'ESC' para FINALIZAR e salvar os dados.")
    time.sleep(2)
    
    if os.path.exists(ARQUIVO_DADOS):
        with open(ARQUIVO_DADOS, 'rb') as f:
            dados = pickle.load(f)
            X_dados, Y_dados = dados['X'], dados['Y']
        print(f"Banco anterior carregado ({len(X_dados)} frames). Adicionando novos...")
    else:
        X_dados, Y_dados = [], []
    
    gravando = True
    print("\n[GRAVANDO]")
    
    ultimo_piscar = time.time()
    estado_piscar = True
    
    
    definir_luz(True)
    
    with mss.mss() as sct:
        while not keyboard.is_pressed('esc'):
            agora = time.time()
            
            if keyboard.is_pressed('tab'):
                gravando = not gravando
                if gravando:
                    print("[GRAVANDO] Voltando a aprender...")
                    definir_luz(True) 
                else:
                    print("[PAUSADO] Navegue no menu.")
                time.sleep(0.3) 
            
            if gravando:
                tela = sct.grab(regiao_captura)
                features = processar_visao(tela)
                teclas = ler_teclado()
                
                X_dados.append(features)
                Y_dados.append(teclas)
            else:
                
                if agora - ultimo_piscar > 0.5:
                    estado_piscar = not estado_piscar
                    definir_luz(estado_piscar)
                    ultimo_piscar = agora
                
            time.sleep(0.01) 
            
    
    definir_luz(False)
    
    with open(ARQUIVO_DADOS, 'wb') as f:
        pickle.dump({'X': X_dados, 'Y': Y_dados}, f)
    print(f"Dados salvos! Dataset possui {len(X_dados)} frames.")


def treinar_modelo():
    if not os.path.exists(ARQUIVO_DADOS):
        print("Erro: Nenhum dado encontrado. Grave primeiro (Opção 1).")
        return
        
    print("\n Construindo árvores de decisão...")
    with open(ARQUIVO_DADOS, 'rb') as f:
        dados = pickle.load(f)
        
    X_dados = np.array(dados['X'])
    Y_dados = np.array(dados['Y'])
    
    modelo = RandomForestClassifier(n_estimators=25, max_depth=15, random_state=42, n_jobs=-1)
    modelo.fit(X_dados, Y_dados)
    
    with open(ARQUIVO_MODELO, 'wb') as f:
        pickle.dump(modelo, f)
    print("Cérebro treinado e salvo com sucesso!")


def ia_jogar():
    if not os.path.exists(ARQUIVO_MODELO):
        print("Erro: IA não treinada. Treine primeiro (Opção 2).")
        return
        
    with open(ARQUIVO_MODELO, 'rb') as f:
        modelo = pickle.load(f)
        
    estado_atual = [0, 0, 0, 0, 0] 
    
    print("\n[IA ASSUMIU O CONTROLE]. Pressione 'ESC' para parar.")
    time.sleep(2)
    
    with mss.mss() as sct:
        while not keyboard.is_pressed('esc'):
            tela = sct.grab(regiao_captura)
            features = processar_visao(tela)
            
            previsao = modelo.predict([features])[0]
            
            for i in range(5):
                if previsao[i] == 1 and estado_atual[i] == 0:
                    keyboard.press(TECLAS[i])
                    estado_atual[i] = 1
                elif previsao[i] == 0 and estado_atual[i] == 1:
                    keyboard.release(TECLAS[i])
                    estado_atual[i] = 0
                    
            time.sleep(0.01)

if __name__ == "__main__":
    while True:
        print("\n=== +++++ ===")
        print("1. Gravar Gameplay (Aprender)")
        print("2. Treinar IA")
        print("3. Deixar a IA jogar")
        print("4. Sair")
        
        escolha = input("Escolha uma opção: ")
        
        if escolha == '1': coletar_dados()
        elif escolha == '2': treinar_modelo()
        elif escolha == '3': ia_jogar()
        elif escolha == '4': break
        else: print("Opção inválida.")