import numpy as np
import mss
import tkinter as tk
from PIL import Image
from collections import Counter
import time

class AmbientMonitor:
    def __init__(self, source_monitor=1, target_monitor=2, update_rate=30):
        """
        source_monitor: indice del monitor da catturare (1=principale)
        target_monitor: indice del monitor su cui proiettare i colori
        update_rate: aggiornamenti al secondo (FPS)
        """
        self.sct = mss.mss()
        self.source_monitor = source_monitor
        self.target_monitor = target_monitor
        self.update_rate = update_rate
        self.delay = 1.0 / update_rate
        
        # Ottieni informazioni sui monitor
        self.monitors = self.sct.monitors
        print(f"Monitor disponibili: {len(self.monitors)-1}")
        for i, mon in enumerate(self.monitors[1:], 1):
            print(f"Monitor {i}: {mon['width']}x{mon['height']} @ ({mon['left']}, {mon['top']})")
        
        # Setup finestra overlay sul monitor target
        self.setup_overlay()
        
    def setup_overlay(self):
        """Crea finestra fullscreen sul monitor secondario"""
        self.root = tk.Tk()
        self.root.title("Ambient Light")
        
        # Ottieni dimensioni e posizione del monitor target
        target = self.monitors[self.target_monitor]
        
        # Finestra fullscreen senza bordi
        self.root.overrideredirect(True)
        self.root.geometry(f"{target['width']}x{target['height']}+{target['left']}+{target['top']}")
        self.root.attributes('-topmost', True)
        
        # Canvas per i colori
        self.canvas = tk.Canvas(self.root, highlightthickness=0)
        self.canvas.pack(fill=tk.BOTH, expand=True)
        
    def capture_screen(self):
        """Cattura screenshot del monitor principale"""
        monitor = self.monitors[self.source_monitor]
        screenshot = self.sct.grab(monitor)
        img = Image.frombytes('RGB', screenshot.size, screenshot.bgra, 'raw', 'BGRX')
        return img
    
    def get_edge_colors(self, img, edge_width=50, zones=4):
        """
        Estrae colori dai bordi dello schermo divisi in zone
        zones: numero di zone per lato (top, bottom, left, right)
        """
        width, height = img.size
        img_array = np.array(img)
        
        colors = {
            'top': [],
            'bottom': [],
            'left': [],
            'right': []
        }
        
        # Top edge
        top_strip = img_array[:edge_width, :, :]
        zone_width = width // zones
        for i in range(zones):
            zone = top_strip[:, i*zone_width:(i+1)*zone_width, :]
            colors['top'].append(self.get_dominant_color(zone))
        
        # Bottom edge
        bottom_strip = img_array[-edge_width:, :, :]
        for i in range(zones):
            zone = bottom_strip[:, i*zone_width:(i+1)*zone_width, :]
            colors['bottom'].append(self.get_dominant_color(zone))
        
        # Left edge
        left_strip = img_array[:, :edge_width, :]
        zone_height = height // zones
        for i in range(zones):
            zone = left_strip[i*zone_height:(i+1)*zone_height, :, :]
            colors['left'].append(self.get_dominant_color(zone))
        
        # Right edge
        right_strip = img_array[:, -edge_width:, :]
        for i in range(zones):
            zone = right_strip[i*zone_height:(i+1)*zone_height, :, :]
            colors['right'].append(self.get_dominant_color(zone))
        
        return colors
    
    def get_dominant_color(self, img_section):
        """Calcola il colore medio di una sezione"""
        avg_color = np.mean(img_section.reshape(-1, 3), axis=0).astype(int)
        return tuple(avg_color)
    
    def rgb_to_hex(self, rgb):
        """Converte RGB in formato HEX per Tkinter"""
        return f'#{rgb[0]:02x}{rgb[1]:02x}{rgb[2]:02x}'
    
    def draw_ambient(self, colors):
        """Disegna l'effetto ambient sul canvas"""
        self.canvas.delete('all')
        
        width = self.canvas.winfo_width()
        height = self.canvas.winfo_height()
        
        if width <= 1 or height <= 1:
            return
        
        # Sfondo con colore medio generale
        all_colors = []
        for side in colors.values():
            all_colors.extend(side)
        avg_color = tuple(np.mean(all_colors, axis=0).astype(int))
        self.canvas.configure(bg=self.rgb_to_hex(avg_color))
        
        # Gradient dai bordi
        edge_size = min(width, height) // 3
        zones = len(colors['top'])
        
        # Top gradient
        zone_width = width // zones
        for i, color in enumerate(colors['top']):
            x1 = i * zone_width
            x2 = (i + 1) * zone_width
            self.create_gradient(x1, 0, x2, edge_size, color, avg_color, 'vertical')
        
        # Bottom gradient
        for i, color in enumerate(colors['bottom']):
            x1 = i * zone_width
            x2 = (i + 1) * zone_width
            self.create_gradient(x1, height - edge_size, x2, height, color, avg_color, 'vertical')
        
    def create_gradient(self, x1, y1, x2, y2, color1, color2, direction):
        """Crea un gradiente tra due colori"""
        steps = 20
        
        if direction == 'vertical':
            step_height = (y2 - y1) / steps
            for i in range(steps):
                ratio = i / steps
                r = int(color1[0] * (1 - ratio) + color2[0] * ratio)
                g = int(color1[1] * (1 - ratio) + color2[1] * ratio)
                b = int(color1[2] * (1 - ratio) + color2[2] * ratio)
                
                y_start = y1 + i * step_height
                self.canvas.create_rectangle(
                    x1, y_start, x2, y_start + step_height,
                    fill=self.rgb_to_hex((r, g, b)), outline=''
                )
    
    def update(self):
        """Loop principale di aggiornamento"""
        try:
            # Cattura e analizza
            img = self.capture_screen()
            colors = self.get_edge_colors(img)
            
            # Disegna ambient
            self.draw_ambient(colors)
            
            # Schedula prossimo aggiornamento
            self.root.after(int(self.delay * 1000), self.update)
            
        except Exception as e:
            print(f"Errore: {e}")
            self.root.after(int(self.delay * 1000), self.update)
    
    def run(self):
        """Avvia l'applicazione"""
        print("Avvio ambient monitor...")
        print(f"Sorgente: Monitor {self.source_monitor}")
        print(f"Target: Monitor {self.target_monitor}")
        print(f"Update rate: {self.update_rate} FPS")
        print("\nPremi Ctrl+C per terminare")
        
        # Aspetta che la finestra sia renderizzata
        self.root.update()
        
        # Avvia loop di aggiornamento
        self.update()
        
        # Main loop
        self.root.mainloop()

if __name__ == "__main__":
    # Installa dipendenze: pip install mss pillow numpy
    
    # Configura i monitor (cambia gli indici se necessario)
    ambient = AmbientMonitor(
        source_monitor=1,  # Monitor principale (di solito 1)
        target_monitor=2,  # Monitor secondario
        update_rate=30     # FPS (abbassa se è troppo pesante)
    )
    
    ambient.run()
