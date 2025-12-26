# 🌈 Ambient Monitor

**Ambient Monitor** è un'applicazione Python che estende l'atmosfera del tuo monitor principale (Gaming/Media) su un monitor secondario, creando un effetto "Ambilight" diffuso e sincronizzato in tempo reale.

![Interface Preview](https://via.placeholder.com/800x400?text=Ambient+Monitor+GUI)

## ✨ Caratteristiche

- 🎮 **Perfetto per il gaming**: Cattura i colori dal monitor principale e li proietta sul secondo
- 🌊 **Transizioni smooth**: Effetti fluidi con easing cubic per un'esperienza rilassante
- ⚙️ **Altamente configurabile**: Personalizza intervalli, durata transizioni e intensità blur
- 🖥️ **GUI moderna**: Interfaccia intuitiva con WebView2
- 🔔 **System tray**: Resta in background senza disturbare (per adesso si riduce a icona)
- 🚀 **Performance ottimizzate**: Thread separati per cattura e rendering

## 📦 Installazione

### Download Release
Scarica l'installer dalla [pagina releases](https://github.com/yourusername/ambient-monitor/releases)

### Build da Sorgente

1. Clona il repository:
```bash
pip install pywebview mss numpy pillow
```

*Nota: `tkinter` è solitamente incluso nell'installazione standard di Python.*

## 🚀 Utilizzo

1. Clona o scarica la cartella del progetto.
2. Assicurati che il file `gui.html` sia nella stessa cartella dello script.
3. Avvia l'applicazione:

```bash
python ambient_monitor_app.py
```

4. Dall'interfaccia:
   - Seleziona il **Monitor Sorgente** (quello da catturare).
   - Seleziona il **Monitor Target** (quello dove proiettare la luce).
   - Premi **▶ Avvia**.
   - Regola i cursori a piacimento mentre l'app è in esecuzione.

## 🔨 Creare l'Eseguibile (.exe)

Per creare un file eseguibile standalone per Windows, utilizza **PyInstaller**.

1. Installa PyInstaller:
   ```bash
   pip install pyinstaller
   ```

2. Build l'eseguibile:
```bash
python build.py
```

3. Crea l'installer con Inno Setup:
- Installa [Inno Setup](https://jrsoftware.org/isdl.php)
- Compila `installer.iss`

## 🎯 Come Usare

1. **Avvia l'applicazione** dal menu Start o desktop
2. **Seleziona i monitor**:
   - Monitor Sorgente: dove giochi (es. Monitor 1)
   - Monitor Target: dove proiettare l'ambient (es. Monitor 2)
3. **Configura i parametri**:
   - **Intervallo Cattura**: ogni quanti secondi catturare i colori (1-10s)
   - **Durata Transizione**: quanto dura il fade tra stati (1-10s)
   - **Intensità Blur**: smoothness dell'effetto (50-200px)
4. **Clicca Avvia** e goditi l'esperienza immersiva!

### 💡 Consigli

- **Per gaming intenso** (FPS, azione): `Intervallo 2s, Transizione 1.5s`
- **Per RPG/Esplorazione** (Skyrim, Witcher): `Intervallo 4s, Transizione 3s`
- **Per film/video**: `Intervallo 1s, Transizione 2s`

## 🖼️ Screenshot

*Aggiungi screenshot della GUI e dell'effetto ambient in azione*
<img width="1736" height="759" alt="immagine" src="https://github.com/user-attachments/assets/d50e4244-cc34-41fa-92d2-340ebf4fc75e" />
<img width="693" height="867" alt="immagine" src="https://github.com/user-attachments/assets/003197ff-a6a5-4f47-84da-b1d1c3457c05" />

## ⚙️ Requisiti di Sistema

- **OS**: Windows 10/11
- **RAM**: 4GB minimo (8GB consigliati)
- **Monitor**: Almeno 2 monitor
- **Python**: 3.8+ (solo per build da sorgente)

## 🛠️ Tecnologie

- **Python**: Core logic
- **mss**: Screen capture veloce
- **Pillow**: Elaborazione immagini
- **NumPy**: Calcoli matematici ottimizzati
- **PyWebView**: GUI con WebView2
- **pystray**: System tray integration

## 🤝 Contribuire

Contributi, issues e feature requests sono benvenuti!

1. Fork il progetto
2. Crea il tuo feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit le modifiche (`git commit -m 'Add some AmazingFeature'`)
4. Push al branch (`git push origin feature/AmazingFeature`)
5. Apri una Pull Request

## 📝 License

Questo progetto è rilasciato sotto licenza MIT. Vedi `LICENSE` per dettagli.

## 👤 Autore

**Your Name**
- GitHub: [@yourusername](https://github.com/yourusername)

## ⭐ Supporto

Se questo progetto ti è stato utile, lascia una ⭐!

## 🐛 Bug Report

Hai trovato un bug? [Apri una issue](https://github.com/yourusername/ambient-monitor/issues)

---

Made with ❤️ for immersive gaming
