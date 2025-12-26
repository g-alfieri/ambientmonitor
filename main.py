import numpy as np
import mss
import tkinter as tk
from PIL import Image, ImageFilter
import time

class AmbientMonitor:
    def __init__(self, source_monitor=1, target_monitor=2, update_rate=30, blur_radius=100):
        """
        source_monitor: indice del monitor da catturare (1=principale)
        target_monitor: indice del monitor su cui proiettare i colori
        update_rate: aggiornamenti al secondo (FPS)
        blur_radius: intensità del blur per smooth transitions
        """
        self.sct = mss.mss()
        self.source_monitor = source_monitor
        self.target_monitor = target_monitor
        self.update_rate = update_rate
        self.delay = 1.0 / update_rate
        self.blur_radius = blur_radius
        
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
        
        # Label per visualizzare l'immagine
        self.label = tk.Label(self.root)
        self.label.pack(fill=tk.BOTH, expand=True)
        
    def capture_screen(self):
        """Cattura screenshot del monitor principale"""
        monitor = self.monitors[self.source_monitor]
        screenshot = self.sct.grab(monitor)
        img = Image.frombytes('RGB', screenshot.size, screenshot.bgra, 'raw', 'BGRX')
        return img
    
    def get_edge_colors(self, img, edge_width=100, samples=12):
        """
        Estrae più colori dai bordi dello schermo
        edge_width: larghezza bordo da campionare
        samples: numero di campioni per lato
        """
        width, height = img.size
        img_array = np.array(img)
        
        colors = []
        positions = []
        
        sample_width = width // samples
        sample_height = height // samples
        
        # Top edge
        for i in range(samples):
            x = i * sample_width + sample_width // 2
            zone = img_array[:edge_width, x-sample_width//2:x+sample_width//2, :]
            color = np.mean(zone.reshape(-1, 3), axis=0).astype(int)
            colors.append(tuple(color))
            positions.append((x, 0))
        
        # Right edge
        for i in range(samples):
            y = i * sample_height + sample_height // 2
            zone = img_array[y-sample_height//2:y+sample_height//2, -edge_width:, :]
            color = np.mean(zone.reshape(-1, 3), axis=0).astype(int)
            colors.append(tuple(color))
            positions.append((width, y))
        
        # Bottom edge
        for i in range(samples-1, -1, -1):
            x = i * sample_width + sample_width // 2
            zone = img_array[-edge_width:, x-sample_width//2:x+sample_width//2, :]
            color = np.mean(zone.reshape(-1, 3), axis=0).astype(int)
            colors.append(tuple(color))
            positions.append((x, height))
        
        # Left edge
        for i in range(samples-1, -1, -1):
            y = i * sample_height + sample_height // 2
            zone = img_array[y-sample_height//2:y+sample_height//2, :edge_width, :]
            color = np.mean(zone.reshape(-1, 3), axis=0).astype(int)
            colors.append(tuple(color))
            positions.append((0, y))
        
        return colors, positions
    
    def create_ambient_image(self, colors, positions):
        """Crea un'immagine ambient con blur molto smooth"""
        target = self.monitors[self.target_monitor]
        width, height = target['width'], target['height']
        
        # Scala ridotta per performance
        scale = 4
        small_width = width // scale
        small_height = height // scale
        
        # Crea immagine con i colori posizionati
        img_array = np.zeros((small_height, small_width, 3), dtype=np.float32)
        weight_array = np.zeros((small_height, small_width), dtype=np.float32)
        
        # Mappa i colori sulla griglia con interpolazione gaussiana
        for (px, py), color in zip(positions, colors):
            # Scala le posizioni
            sx = int(px / scale)
            sy = int(py / scale)
            
            # Raggio di influenza
            radius = min(small_width, small_height) // 3
            
            # Crea griglia di coordinate
            y_coords, x_coords = np.ogrid[:small_height, :small_width]
            
            # Calcola distanze dal punto
            distances = np.sqrt((x_coords - sx)**2 + (y_coords - sy)**2)
            
            # Pesi gaussiani
            weights = np.exp(-(distances**2) / (2 * (radius/2)**2))
            
            # Aggiungi colore pesato
            for c in range(3):
                img_array[:, :, c] += weights * color[c]
            weight_array += weights
        
        # Normalizza
        for c in range(3):
            img_array[:, :, c] /= np.maximum(weight_array, 1e-6)
        
        # Converti in immagine PIL
        img_array = np.clip(img_array, 0, 255).astype(np.uint8)
        ambient_img = Image.fromarray(img_array, 'RGB')
        
        # Ridimensiona e applica blur pesante
        ambient_img = ambient_img.resize((width, height), Image.LANCZOS)
        ambient_img = ambient_img.filter(ImageFilter.GaussianBlur(radius=self.blur_radius))
        
        return ambient_img
    
    def update(self):
        """Loop principale di aggiornamento"""
        try:
            # Cattura e analizza
            img = self.capture_screen()
            colors, positions = self.get_edge_colors(img, edge_width=150, samples=16)
            
            # Crea immagine ambient
            ambient_img = self.create_ambient_image(colors, positions)
            
            # Converti per Tkinter
            from PIL import ImageTk
            photo = ImageTk.PhotoImage(ambient_img)
            self.label.configure(image=photo)
            self.label.image = photo  # Mantieni riferimento
            
            # Schedula prossimo aggiornamento
            self.root.after(int(self.delay * 1000), self.update)
            
        except Exception as e:
            print(f"Errore: {e}")
            import traceback
            traceback.print_exc()
            self.root.after(int(self.delay * 1000), self.update)
    
    def run(self):
        """Avvia l'applicazione"""
        print("Avvio ambient monitor...")
        print(f"Sorgente: Monitor {self.source_monitor}")
        print(f"Target: Monitor {self.target_monitor}")
        print(f"Update rate: {self.update_rate} FPS")
        print(f"Blur radius: {self.blur_radius}")
        print("\nPremi Ctrl+C per terminare")
        
        # Aspetta che la finestra sia renderizzata
        self.root.update()
        
        # Avvia loop di aggiornamento
        self.update()
        
        # Main loop
        self.root.mainloop()

if __name__ == "__main__":
    # Installa dipendenze: pip install mss pillow numpy
    
    # Configura i monitor
    ambient = AmbientMonitor(
        source_monitor=1,      # Monitor principale
        target_monitor=2,      # Monitor secondario
        update_rate=30,        # FPS (abbassa a 20-25 se troppo pesante)
        blur_radius=120        # Blur intensity (più alto = più smooth, 80-150 consigliato)
    )
    
    ambient.run()
