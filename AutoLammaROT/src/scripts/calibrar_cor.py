import cv2
import numpy as np

def calibrar_cor(caminho_imagem):
    def nothing(x): pass

    cv2.namedWindow("Calibracao")
    # Começamos com os seus valores atuais para você ver o erro
    cv2.createTrackbar("Min-H", "Calibracao", 90, 179, nothing)
    cv2.createTrackbar("Min-S", "Calibracao", 100, 255, nothing)
    cv2.createTrackbar("Min-V", "Calibracao", 100, 255, nothing)
    cv2.createTrackbar("Max-H", "Calibracao", 115, 179, nothing)
    cv2.createTrackbar("Max-S", "Calibracao", 255, 255, nothing)
    cv2.createTrackbar("Max-V", "Calibracao", 255, 255, nothing)

    img = cv2.imread(caminho_imagem)
    # Dica: use apenas a ROI para calibrar mais rápido
    # roi = img[456:529, 721:1200] 

    while True:
        hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
        
        l_h = cv2.getTrackbarPos("Min-H", "Calibracao")
        l_s = cv2.getTrackbarPos("Min-S", "Calibracao")
        l_v = cv2.getTrackbarPos("Min-V", "Calibracao")
        u_h = cv2.getTrackbarPos("Max-H", "Calibracao")
        u_s = cv2.getTrackbarPos("Max-S", "Calibracao")
        u_v = cv2.getTrackbarPos("Max-V", "Calibracao")

        mask = cv2.inRange(hsv, np.array([l_h, l_s, l_v]), np.array([u_h, u_s, u_v]))
        
        cv2.imshow("Ajuste a mascara ate ver apenas o alvo", mask)
        if cv2.waitKey(1) & 0xFF == 27: break

    cv2.destroyAllWindows()

# Execute passando o caminho da sua imagem
calibrar_cor("src/images/image.png")