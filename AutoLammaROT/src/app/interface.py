import tkinter as tk
import threading
import cv2
import numpy as np
import mss
import pydirectinput
import time
import sys
from analisador_frames import AnalisadorFrames

class AutoLammaGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("AutoLamma v1.5 - Precision Pro")
        self.root.geometry("350x300")
        
        self.running = False
        self.bot_thread = None
        self.analisador = AnalisadorFrames()

        # Elementos da Interface
        self.label_status = tk.Label(root, text="Status: Desligado", fg="red", font=("Arial", 12, "bold"))
        self.label_status.pack(pady=15)

        tk.Label(root, text="Fator Base (Lag):").pack()
        self.entry_lag = tk.Entry(root, justify='center')
        self.entry_lag.insert(0, "0.5") # Valor inicial sugerido
        self.entry_lag.pack(pady=5)

        self.label_info = tk.Label(root, text="Monitorando performance...", font=("Consolas", 9))
        self.label_info.pack(pady=10)

        self.btn_start = tk.Button(root, text="LIGAR BOT", command=self.start_bot, bg="green", fg="white", width=20)
        self.btn_start.pack(pady=5)

        self.btn_stop = tk.Button(root, text="DESLIGAR BOT", command=self.stop_bot, bg="red", fg="white", width=20)
        self.btn_stop.pack(pady=5)

    def bot_loop(self):
        # ROI HIPER-OTIMIZADA: Altura de 10 pixels foca o processamento
        monitor = {
            "top": 487,    
            "left": 711, 
            "width": 489, 
            "height": 10   
        }
        x_anterior = None
        pydirectinput.PAUSE = 0
        f_pressed = 0
        MAX_TRIES = 9

        with mss.mss() as sct:
            while self.running:
                # 1. Captura Ultra-Rápida
                img = np.array(sct.grab(monitor))
                frame = cv2.cvtColor(img, cv2.COLOR_BGRA2BGR)
                
                # Detecção com coordenadas locais (0,0) para evitar erros de índice
                res = self.analisador.analisar_frame(frame, {
                    "x_min": 0, "y_min": 0, 
                    "x_max": monitor["width"], "y_max": monitor["height"]
                })
                
                if res.get("sucesso"):
                    x_atual = res["pos_barra"]
                    t_min, t_max = res["area_azul"]

                    if x_anterior is not None and x_atual > x_anterior:
                        velocidade = x_atual - x_anterior
                        
                        try:
                            fator_base = float(self.entry_lag.get())
                        except:
                            fator_base = 0.5

                        
                        pos_atual = x_atual
                        pos_futura = x_atual + (velocidade * fator_base)

                        # Lógica de Interseção de Trajetória
                        if (pos_futura) >= t_min and pos_atual <= t_max:
                            pydirectinput.press('f')
                            f_pressed += 1
                            if f_pressed == MAX_TRIES:
                                self.stop_bot()
                            x_anterior = None
                            time.sleep(1) # Tempo para reset da animação do jogo
                            continue

                    x_anterior = x_atual
                else:
                    x_anterior = None

    def start_bot(self):
        if not self.running:
            self.running = True
            self.label_status.config(text="Status: RODANDO", fg="green")
            self.bot_thread = threading.Thread(target=self.bot_loop, daemon=True)
            self.bot_thread.start()

    def stop_bot(self):
        self.running = False
        self.label_status.config(text="Status: Desligado", fg="red")

if __name__ == "__main__":
    root = tk.Tk()
    app = AutoLammaGUI(root)
    
    # Tratamento de fechamento da janela
    def on_closing():
        app.stop_bot()
        root.destroy()
        sys.exit(0)

    root.protocol("WM_DELETE_WINDOW", on_closing)
    root.mainloop()