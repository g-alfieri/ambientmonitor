# -*- coding: utf-8 -*-
"""
Setup script per creare l'installer di Ambient Monitor
"""
import PyInstaller.__main__
import os
import shutil

def build():
    """Crea l'eseguibile con PyInstaller"""

    # Verifica se esiste l'icona
    icon_arg = []
    if os.path.exists('icon.ico'):
        icon_arg = ['--icon=icon.ico']
        print("✓ Usando icon.ico")
    else:
        print("⚠ icon.ico non trovato, proseguo senza icona")

    args = [
        'ambient_monitor_app.py',
        '--name=AmbientMonitor',
        '--windowed',
        '--onefile',
        '--add-data=gui.html;.',
        '--hidden-import=mss',
        '--hidden-import=PIL',
        '--hidden-import=numpy',
        '--hidden-import=pystray',
        '--hidden-import=webview',
        '--clean',
    ]

    # Aggiungi icona solo se esiste
    args.extend(icon_arg)

    PyInstaller.__main__.run(args)

    print("\n✓ Build completato!")
    print("L'eseguibile si trova in: dist/AmbientMonitor.exe")

if __name__ == '__main__':
    build()
