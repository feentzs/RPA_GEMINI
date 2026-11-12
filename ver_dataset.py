import pickle
import cv2
import numpy as np
import time


ARQUIVO_DADOS = "dataset_fnf_pro.pkl" 

def reproduzir_dataset():
    try:
        with open(ARQUIVO_DADOS, 'rb') as f:
            dados = pickle.load(f)
    except FileNotFoundError:
        print(f"Arquivo {ARQUIVO_DADOS} não encontrado. Grave dados primeiro!")
        return

    X_dados = dados['X']
    Y_dados = dados['Y']
    
    total_frames = len(X_dados)
    print(f"Iniciando reprodução de {total_frames} frames...")
    print("Pressione a tecla 'ESC' na janela do vídeo para fechar.")
    time.sleep(2)

    for i in range(total_frames):
        
        
        
        
        frame_bruto = np.reshape(X_dados[i], (50, 75, 3))
        
        
        frame_bruto = frame_bruto.astype(np.uint8)
        
        
        frame_ampliado = cv2.resize(frame_bruto, (640, 520), interpolation=cv2.INTER_NEAREST)
        
        
        cv2.imshow("O que a IA esta vendo (Preto e Branco)", frame_ampliado)
        
        
        print(f"Frame {i:05d}/{total_frames} | Inputs gravados: {Y_dados[i]}")
        
        
        if cv2.waitKey(10) & 0xFF == 27:
            break

    cv2.destroyAllWindows()
    print("Reprodução finalizada.")

if __name__ == "__main__":
    reproduzir_dataset()