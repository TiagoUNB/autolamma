import cv2
import numpy as np
from pathlib import Path
import sys

class AnalisadorFrames:
    """Classe para analisar frames de imagens e detectar colisões em uma ROI específica."""
    
    def __init__(self):
        # Localiza a pasta src/images a partir de src/app/analisador.py
        # .parent (app) -> .parent (src)
        self.projeto_root = Path(__file__).resolve().parent.parent
        self.images_dir = self.projeto_root / "images"
        
        if not self.images_dir.exists():
            print(f"Aviso: Pasta de imagens não encontrada em {self.images_dir}")

    def analisar_frame(self, imagem, roi_coords=None):
        """
        Analisa o frame para detectar se a linha branca está sobre a área azul.
        
        Args:
            imagem: Imagem carregada pelo OpenCV (BGR).
            roi_coords (dict): {'x_min': int, 'y_min': int, 'x_max': int, 'y_max': int}
        """
        # 1. Aplicar Recorte (ROI)
        if roi_coords:
            x1, y1 = roi_coords['x_min'], roi_coords['y_min']
            x2, y2 = roi_coords['x_max'], roi_coords['y_max']
            # No NumPy a ordem é [y_start:y_end, x_start:x_end]
            frame_processado = imagem[y1:y2, x1:x2]
        else:
            frame_processado = imagem
            x1, y1 = 0, 0

        # 2. Converter para HSV
        hsv = cv2.cvtColor(frame_processado, cv2.COLOR_BGR2HSV)
        
        # 3. Definição de Cores CALIBRADAS
        # Azul (Zona de Acerto) - Valores obtidos na sua calibração
        azul_baixo = np.array([35, 146, 255])
        azul_alto = np.array([108, 165, 255])
        
        # Branco (Linha Indicadora)
        branco_baixo = np.array([0, 0, 200])
        branco_alto = np.array([180, 40, 255])
        
        # 4. Criar Máscaras
        mask_azul = cv2.inRange(hsv, azul_baixo, azul_alto)
        mask_branco = cv2.inRange(hsv, branco_baixo, branco_alto)
        
        # 5. Localizar Coordenadas X
        # Extraímos apenas as colunas onde há pixels detectados (índice [1])
        pixels_azul = np.where(mask_azul > 0)[1]
        pixels_branco = np.where(mask_branco > 0)[1]
        
        if len(pixels_azul) > 0 and len(pixels_branco) > 0:
            # Posições relativas à imagem original (somando o offset x1)
            x_min_azul = np.min(pixels_azul) + x1
            x_max_azul = np.max(pixels_azul) + x1
            
            # Usamos a mediana para encontrar o centro da linha branca
            x_barra = np.median(pixels_branco) + x1
            
            # Lógica de Colisão: verifica se o centro da barra está dentro do range azul
            colisao = x_min_azul <= x_barra <= x_max_azul
            
            return {
                "colisao": colisao,
                "area_azul": (int(x_min_azul), int(x_max_azul)),
                "pos_barra": int(x_barra),
                "sucesso": True
            }
        
        return {"colisao": False, "sucesso": False, "msg": "Elementos não detectados na ROI"}

    def processar_imagem(self, nome_arquivo, roi_coords=None):
        """Carrega e processa uma imagem específica na pasta images/."""
        caminho = self.images_dir / nome_arquivo
        
        if not caminho.exists():
            return {"erro": f"Arquivo {nome_arquivo} não encontrado."}
            
        imagem = cv2.imread(str(caminho))
        if imagem is None:
            return {"erro": f"Falha ao carregar imagem: {nome_arquivo}"}
            
        resultado = self.analisar_frame(imagem, roi_coords)
        resultado["arquivo"] = nome_arquivo
        return resultado

    def _exibir_resultado(self, res):
        """Formata o output no terminal com cores e status."""
        if "erro" in res:
            print(f"❌ Erro: {res['erro']}")
        elif res.get("sucesso"):
            status = "✅ COLISÃO!" if res["colisao"] else "⏳ Aguardando..."
            print(f"{status} | Arq: {res['arquivo']}")
            print(f"   ↳ Posição Barra: {res['pos_barra']}")
            print(f"   ↳ Alvo (Min/Max): {res['area_azul']}")
        else:
            print(f"⚠️ {res['arquivo']}: {res.get('msg')}")
        print("-" * 50)

# --- Exemplo de Uso ---
if __name__ == "__main__":
    analisador = AnalisadorFrames()
    
    # Configurações para modo JANELA 1680 X 1050
    minha_roi = {
        "x_min": 721, 
        "y_min": 456, 
        "x_max": 1200, 
        "y_max": 529
    }
    
    # Nome da imagem que deve estar em src/images/
    arquivo_teste = "image.png"
    
    print(f"Iniciando análise da ROI em: {minha_roi}")
    resultado = analisador.processar_imagem(arquivo_teste, roi_coords=minha_roi)
    analisador._exibir_resultado(resultado)