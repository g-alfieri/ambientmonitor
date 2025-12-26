# -*- coding: utf-8 -*-
"""Ambient Monitor - Unicode Safe"""
from __future__ import annotations
import sys
import os
import json
import time
import multiprocessing
from multiprocessing import Process, Queue, Event

# --- Force UTF-8 where possible (Windows) ---
try:
    if hasattr(sys.stdout, 'reconfigure'):
        sys.stdout.reconfigure(encoding='utf-8', errors='replace')
    if hasattr(sys.stderr, 'reconfigure'):
        sys.stderr.reconfigure(encoding='utf-8', errors='replace')
except Exception:
    pass

import mss
import numpy as np
from PIL import Image, ImageFilter, ImageTk

try:
    import webview
    WEBVIEW_AVAILABLE = True
except ImportError:
    WEBVIEW_AVAILABLE = False


def safe_print(*args, **kwargs):
    """Stampa sicura che evita crash Unicode su Windows console."""
    try:
        print(*args, **kwargs)
    except UnicodeEncodeError:
        try:
            # Fallback: encode/decode per rimuovere caratteri non supportati
            text = ' '.join(str(a) for a in args)
            end_char = kwargs.get('end', '\n')
            clean_text = text.encode('ascii', 'replace').decode('ascii') + end_char
            sys.stdout.write(clean_text)
        except Exception:
            pass


def overlay_process(img_queue: Queue, config_queue: Queue, stop_event: Event):
    import tkinter as tk

    try:
        initial_config = config_queue.get()
        target_idx = int(initial_config.get('target_monitor', 2))

        with mss.mss() as sct:
            monitors = list(sct.monitors)
            if target_idx >= len(monitors):
                safe_print(f"Overlay: target monitor {target_idx} not found")
                return
            target = monitors[target_idx]

        root = tk.Tk()
        root.overrideredirect(True)
        root.geometry(f"{target['width']}x{target['height']}+{target['left']}+{target['top']}")
        root.configure(bg='black')

        current_opacity = float(initial_config.get('opacity', 0.7))
        current_blend = bool(initial_config.get('blend_mode', True))

        def apply_style(opacity: float, blend: bool):
            try:
                if blend:
                    root.attributes('-alpha', opacity)
                    root.attributes('-topmost', False)
                else:
                    root.attributes('-alpha', 1.0)
                    root.attributes('-topmost', True)
            except Exception:
                pass

        apply_style(current_opacity, current_blend)

        label = tk.Label(root, bg='black')
        label.pack(fill=tk.BOTH, expand=True)

        def check_updates():
            if stop_event.is_set():
                try:
                    root.destroy()
                finally:
                    return

            # Config updates
            try:
                while not config_queue.empty():
                    new_conf = config_queue.get_nowait()
                    current_opacity = float(new_conf.get('opacity', current_opacity))
                    current_blend = bool(new_conf.get('blend_mode', current_blend))
                    apply_style(current_opacity, current_blend)
            except Exception:
                pass

            # Image updates
            try:
                last_img = None
                while not img_queue.empty():
                    last_img = img_queue.get_nowait()
                if last_img:
                    size, mode, data = last_img
                    img = Image.frombytes(mode, size, data)
                    photo = ImageTk.PhotoImage(img)
                    label.configure(image=photo)
                    label.image = photo
            except Exception:
                pass

            root.after(16, check_updates)

        root.after(100, check_updates)
        root.mainloop()

    except Exception as e:
        safe_print("Overlay process error:", e)


def capture_process(img_queue: Queue, config_queue: Queue, stop_event: Event):
    try:
        config = config_queue.get()
        source_idx = int(config.get('source_monitor', 1))
        target_idx = int(config.get('target_monitor', 2))
        fps = int(config.get('update_rate', 30))
        blur = int(config.get('blur_radius', 120))

        with mss.mss() as sct:
            monitors = list(sct.monitors)
            source = monitors[source_idx]
            target = monitors[target_idx]
            t_w, t_h = target['width'], target['height']

            while not stop_event.is_set():
                start_t = time.time()

                # Config updates
                try:
                    while not config_queue.empty():
                        new_c = config_queue.get_nowait()
                        fps = int(new_c.get('update_rate', fps))
                        blur = int(new_c.get('blur_radius', blur))
                except Exception:
                    pass

                sct_img = sct.grab(source)
                img = Image.frombytes('RGB', sct_img.size, sct_img.bgra, 'raw', 'BGRX')

                small = img.resize((32, 32), Image.BILINEAR)
                ambient = small.resize((max(1, t_w // 10), max(1, t_h // 10)), Image.BICUBIC)
                blurred = ambient.filter(ImageFilter.GaussianBlur(radius=max(1, blur // 10)))
                final = blurred.resize((t_w, t_h), Image.BICUBIC)

                if not img_queue.full():
                    img_queue.put((final.size, final.mode, final.tobytes()))

                elapsed = time.time() - start_t
                time.sleep(max(0, (1.0 / max(1, fps)) - elapsed))

    except Exception as e:
        safe_print("Capture process error:", e)


class AmbientMonitorApp:
    def __init__(self):
        self.p_overlay: Process | None = None
        self.p_capture: Process | None = None
        self.stop_event: Event | None = None

        self.img_queue: Queue | None = None
        self.conf_queue_overlay: Queue | None = None
        self.conf_queue_capture: Queue | None = None
        self.current_config: dict = {}

        with mss.mss() as sct:
            self.monitors = list(sct.monitors)

    def get_monitors(self):
        return [{"width": m["width"], "height": m["height"]} for m in self.monitors]

    def startAmbient(self, config_str):
        try:
            new_config = json.loads(config_str)
            new_config['opacity'] = new_config.get('opacity', 70) / 100.0

            if self.p_overlay and self.p_overlay.is_alive():
                if (new_config.get('source_monitor') != self.current_config.get('source_monitor') or
                        new_config.get('target_monitor') != self.current_config.get('target_monitor')):
                    self.stopAmbient()
                else:
                    self.conf_queue_overlay.put(new_config)
                    self.conf_queue_capture.put(new_config)
                    self.current_config = new_config
                    return {"success": True}

            self.stopAmbient()
            self.current_config = new_config

            self.img_queue = Queue(maxsize=2)
            self.conf_queue_overlay = Queue()
            self.conf_queue_capture = Queue()
            self.stop_event = Event()

            self.conf_queue_overlay.put(new_config)
            self.conf_queue_capture.put(new_config)

            self.p_overlay = Process(target=overlay_process, args=(self.img_queue, self.conf_queue_overlay, self.stop_event))
            self.p_capture = Process(target=capture_process, args=(self.img_queue, self.conf_queue_capture, self.stop_event))

            self.p_overlay.start()
            self.p_capture.start()

            return {"success": True}
        except Exception as e:
            safe_print("startAmbient error:", e)
            return {"success": False, "error": str(e)}

    def stopAmbient(self):
        if self.stop_event:
            self.stop_event.set()

        for p in (self.p_capture, self.p_overlay):
            if p and p.is_alive():
                p.join(timeout=1)
                if p.is_alive():
                    p.terminate()

        self.p_capture = None
        self.p_overlay = None
        self.stop_event = None
        return {"success": True}

    def run(self):
        if not WEBVIEW_AVAILABLE:
            safe_print('pywebview is required')
            return

        multiprocessing.freeze_support()

        html_path = os.path.join(os.path.dirname(__file__), 'gui.html')
        window = webview.create_window('Ambient Monitor', html_path, width=550, height=680)

        def on_start():
            window.expose(self.get_monitors, self.startAmbient, self.stopAmbient)

        webview.start(on_start, debug=False)


if __name__ == '__main__':
    multiprocessing.freeze_support()
    safe_print('Ambient Monitor (Safe)')
    AmbientMonitorApp().run()
