import cv2
import numpy as np
import mss
import pydirectinput
import time
from analisador_frames import AnalisadorFrames
import sys

def executar_automacao():
    analisador = AnalisadorFrames()
    pydirectinput.PAUSE = 0 # Remove delays entre comandos
    
    monitor = {"top": 456, "left": 721, "width": 479, "height": 73}
    
    x_anterior = 0
    fator_ante_lag = 0.55 # AJUSTE ESTE VALOR (0.5 a 2.0) conforme a velocidade aumenta

    with mss.mss() as sct:
        print("=== BOT PRO INICIADO (MODO PREDITIVO) ===")
        while True:
            # Captura ultra-rápida
            img = np.array(sct.grab(monitor))
            frame = cv2.cvtColor(img, cv2.COLOR_BGRA2BGR)
            
            res = analisador.analisar_frame(frame, {"x_min": 0, "y_min": 0, "x_max": 479, "y_max": 73})
            
            if res.get("sucesso"):
                x_atual = res["pos_barra"]
                
                # Calcula velocidade e direção
                velocidade = x_atual - x_anterior
                
                # Previsão da posição no próximo instante
                pos_predita = x_atual + (velocidade * fator_ante_lag)
                
                target_min, target_max = res["area_azul"]
                
                # Verifica se a posição PREDITA vai colidir
                if target_min <= pos_predita <= target_max:
                    pydirectinput.press('f')
                    print(f"🎯 Clique Preditivo! V:{velocidade} | Pred:{pos_predita}")
                    time.sleep(0.4)
                
                x_anterior = x_atual

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
def main():
    try:
        print("=" * 30)
        print("   AutoLammaROT v1.0")
        print("=" * 30)
        print("O bot começará em 3 segundos...")
        print("Pressione CTRL+C para encerrar com segurança.")
        
        time.sleep(3)
        executar_automacao()

    except KeyboardInterrupt:
        # Mensagem limpa ao capturar o comando de interrupção
        print("\n\n" + "=" * 30)
        print("🔴 Encerrando bot...")
        print("Saindo com segurança...")
        print("=" * 30)
        
        # Garante que as janelas do OpenCV sejam fechadas
        cv2.destroyAllWindows()
        
        # Encerra o script sem código de erro
        sys.exit(0)

if __name__ == "__main__":
    main()