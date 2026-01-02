import pyautogui
import time
import sys

def monitorar_mouse():
    print("Pressione Ctrl + C para interromper o script.\n")
    
    try:
        while True:
            # Obtém as coordenadas atuais do mouse
            x, y = pyautogui.position()
            
            # Formata a string com a posição
            # O ljust ajuda a limpar caracteres remanescentes se a string encurtar
            posicao_str = f"X: {str(x).ljust(4)} | Y: {str(y).ljust(4)}"
            
            # Imprime na mesma linha (\r move o cursor para o início da linha)
            print(posicao_str)
            
            # Pequeno intervalo para não sobrecarregar a CPU
            time.sleep(0.1)
            
    except KeyboardInterrupt:
        print("\n\nScript encerrado pelo usuário.")

if __name__ == "__main__":
    monitorar_mouse()