import keyboard
import mss
import time
import pickle
import os
import numpy as np
from sklearn.ensemble import RandomForestClassifier


X_ESQUERDA, X_BAIXO, X_CIMA, X_DIREITA = 782, 906, 1029, 1156
Y_SETAS_ORIGINAL = 112
OFFSET = 35 
Y_LEITURA = Y_SETAS_ORIGINAL + OFFSET 

TECLAS = ['d', 'f', 'j', 'k'] 

regiao_captura = {
    "top": Y_LEITURA - 5, 
    "left": X_ESQUERDA - 5, 
    "width": (X_DIREITA - X_ESQUERDA) + 10, 
    "height": 10
}

ARQUIVO_DADOS = "dataset_fnf.pkl"
ARQUIVO_MODELO = "modelo_ia_fnf.pkl"


def extrair_features(tela):
    r_esq, g_esq, b_esq = tela.pixel(5, 5)
    r_bai, g_bai, b_bai = tela.pixel(X_BAIXO - X_ESQUERDA + 5, 5)
    r_cim, g_cim, b_cim = tela.pixel(X_CIMA - X_ESQUERDA + 5, 5)
    r_dir, g_dir, b_dir = tela.pixel(X_DIREITA - X_ESQUERDA + 5, 5)
    
    
    return [r_esq, g_esq, b_esq, r_bai, g_bai, b_bai, r_cim, g_cim, b_cim, r_dir, g_dir, b_dir]


def ler_teclado():
    
    return [
        1 if keyboard.is_pressed('d') else 0,
        1 if keyboard.is_pressed('f') else 0,
        1 if keyboard.is_pressed('j') else 0,
        1 if keyboard.is_pressed('k') else 0
    ]


def coletar_dados():
    print("\n[MODO GRAVAÇÃO] Inicie uma música e jogue!")
    print("A IA vai gravar suas jogadas. Pressione 'ESC' para parar e salvar.")
    time.sleep(2)
    
    
    if os.path.exists(ARQUIVO_DADOS):
        with open(ARQUIVO_DADOS, 'rb') as f:
            dados = pickle.load(f)
            X_dados = dados['X']
            Y_dados = dados['Y']
        print(f"Banco de dados anterior carregado ({len(X_dados)} frames). Adicionando novos dados...")
    else:
        X_dados = [] 
        Y_dados = [] 
    
    with mss.mss() as sct:
        while not keyboard.is_pressed('esc'):
            tela = sct.grab(regiao_captura)
            features = extrair_features(tela)
            teclas = ler_teclado()
            
            X_dados.append(features)
            Y_dados.append(teclas)
            time.sleep(0.01) 
            
    
    with open(ARQUIVO_DADOS, 'wb') as f:
        pickle.dump({'X': X_dados, 'Y': Y_dados}, f)
    print(f"Dados salvos! O dataset agora possui {len(X_dados)} frames no total.")


def treinar_modelo():
    if not os.path.exists(ARQUIVO_DADOS):
        print("Erro: Nenhum dado encontrado. Grave primeiro (Opção 1).")
        return
        
    print("\n[MODO TREINO] Lendo seus dados e treinando a IA...")
    with open(ARQUIVO_DADOS, 'rb') as f:
        dados = pickle.load(f)
        
    X_dados = np.array(dados['X'])
    Y_dados = np.array(dados['Y'])
    
    
    modelo = RandomForestClassifier(n_estimators=10, random_state=42, n_jobs=-1)
    modelo.fit(X_dados, Y_dados)
    
    
    with open(ARQUIVO_MODELO, 'wb') as f:
        pickle.dump(modelo, f)
    print("Treinamento concluído e modelo salvo com sucesso!")


def ia_jogar():
    if not os.path.exists(ARQUIVO_MODELO):
        print("Erro: A IA ainda não foi treinada. Treine primeiro (Opção 2).")
        return
        
    with open(ARQUIVO_MODELO, 'rb') as f:
        modelo = pickle.load(f)
        
    estado_atual = [0, 0, 0, 0]
    
    print("\n[MODO IA JOGANDO] A Inteligência Artificial assumiu o controle!")
    print("Pressione 'ESC' para parar.")
    time.sleep(2)
    
    with mss.mss() as sct:
        while not keyboard.is_pressed('esc'):
            tela = sct.grab(regiao_captura)
            features = extrair_features(tela)
            
            
            previsao = modelo.predict([features])[0]
            
            
            for i in range(4):
                if previsao[i] == 1 and estado_atual[i] == 0:
                    keyboard.press(TECLAS[i])
                    estado_atual[i] = 1
                elif previsao[i] == 0 and estado_atual[i] == 1:
                    keyboard.release(TECLAS[i])
                    estado_atual[i] = 0
                    
            
            time.sleep(0.01)


if __name__ == "__main__":
    while True:
        print("\n=== BOT IA - FRIDAY NIGHT FUNKIN ===")
        print("1. Gravar Gameplay (Ensinar a IA)")
        print("2. Treinar IA com os dados gravados")
        print("3. Deixar a IA jogar")
        print("4. Sair")
        
        escolha = input("Escolha uma opção: ")
        
        if escolha == '1':
            coletar_dados()
        elif escolha == '2':
            treinar_modelo()
        elif escolha == '3':
            ia_jogar()
        elif escolha == '4':
            break
        else:
            print("Opção inválida.")