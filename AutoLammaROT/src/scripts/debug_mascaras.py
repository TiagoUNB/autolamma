import cv2
import numpy as np
from pathlib import Path

def analisar_visual_mascaras(nome_imagem, roi):
    # 1. Caminhos
    caminho_root = Path(__file__).resolve().parent.parent
    caminho_img = caminho_root / "images" / nome_imagem

    img = cv2.imread(str(caminho_img))
    if img is None:
        print("Erro ao carregar imagem!")
        return

    # 2. Cortar a ROI (Paint: x1, y1 até x2, y2)
    roi_img = img[roi['y_min']:roi['y_max'], roi['x_min']:roi['x_max']]
    hsv = cv2.cvtColor(roi_img, cv2.COLOR_BGR2HSV)

    # 3. Definição de Cores - AJUSTADAS
    # Azul Alvo: Aumentamos o S e V mínimos para ignorar o azul escuro
    azul_baixo = np.array([35, 146, 255]) 
    azul_alto = np.array([108, 165, 255])
    # Branco Indicador
    branco_baixo = np.array([0, 0, 200])
    branco_alto = np.array([180, 40, 255])

    # 4. Gerar Máscaras
    mask_azul = cv2.inRange(hsv, azul_baixo, azul_alto)
    mask_branco = cv2.inRange(hsv, branco_baixo, branco_alto)

    # 5. Criar uma visualização combinada (Resultados)
    res_azul = cv2.bitwise_and(roi_img, roi_img, mask=mask_azul)
    res_branco = cv2.bitwise_and(roi_img, roi_img, mask=mask_branco)

    # Exibição
    print("Pressione qualquer tecla para fechar as janelas...")
    cv2.imshow("1. ROI Original (Paint)", roi_img)
    cv2.imshow("2. Mascara Azul (O que o script entende como ALVO)", mask_azul)
    cv2.imshow("3. Mascara Branca (O que o script entende como BARRA)", mask_branco)
    cv2.imshow("4. Resultado Final Azul", res_azul)

    cv2.waitKey(0)
    cv2.destroyAllWindows()

if __name__ == "__main__":
    # Sua ROI obtida no Paint
    minha_roi = {
        "x_min": 721, 
        "y_min": 486, 
        "x_max": 1200, 
        "y_max": 496
    }
    
    analisar_visual_mascaras("image.png", minha_roi)