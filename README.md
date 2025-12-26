# 🌈 Ambient Monitor

**Ambient Monitor** è un'applicazione Python che estende l'atmosfera del tuo monitor principale (Gaming/Media) su un monitor secondario, creando un effetto "Ambilight" diffuso e sincronizzato in tempo reale.

![Interface Preview](https://via.placeholder.com/800x400?text=Ambient+Monitor+GUI)

## ✨ Funzionalità

- **Cattura Real-Time**: Sincronizzazione istantanea con il monitor sorgente.
- **Effetto Blur Gaussiano**: Crea un'atmosfera morbida e diffusa.
- **Controlli Completi**:
  - **FPS**: Regola la fluidità (da 10 a 60 FPS).
  - **Blur**: Intensità della sfocatura.
  - **Opacità**: Regolazione trasparenza in tempo reale.
  - **Blend Mode**: Fusione avanzata con lo sfondo nero.
- **Architettura Robusta**: Utilizza **Multiprocessing** per separare GUI, Cattura e Rendering, garantendo stabilità totale e zero crash (fix per errori Tkinter/Thread).
- **GUI Moderna**: Interfaccia HTML/CSS pulita integrata tramite `pywebview`.

## 📦 Requisiti

Assicurati di avere Python 3.x installato. Installa le dipendenze necessarie:

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

2. Esegui il comando di build (assicurati di essere nella cartella del progetto):

   ```bash
   pyinstaller --noconfirm --onefile --windowed --name "AmbientMonitor" --add-data "gui.html;." ambient_monitor_app.py
   ```

   *Nota: Se usi PowerShell, potresti dover mettere le virgolette diversamente o usare cmd.*

3. Troverai l'eseguibile nella cartella `dist/`.

## 🔧 Risoluzione Problemi Comuni

### Errori "Tcl_AsyncDelete" o Crash Tkinter
Questa versione utilizza un'architettura a **Processi Separati** (Multiprocessing). Se riscontri crash legati ai thread, assicurati di usare l'ultima versione del codice che isola Tkinter nel suo processo dedicato.

### Errore "charmap codec" nell'EXE
Se l'EXE crasha all'avvio con errori di Unicode/Encoding, è stato applicato un fix (`safe_print`) che gestisce correttamente i log su console Windows senza supporto UTF-8 completo.

### Schermo nero o non aggiornato
- Controlla di aver selezionato i monitor corretti.
- Prova a disattivare/riattivare il "Blend Mode".
- Verifica che l'opacità non sia a 0.

## 📝 Struttura File

- `ambient_monitor_app.py`: Logica principale, gestione processi e backend.
- `gui.html`: Interfaccia utente frontend.
- `README.md`: Questo file.

## ⚖️ Licenza
Progetto Open Source. Sentiti libero di modificarlo e migliorarlo!
