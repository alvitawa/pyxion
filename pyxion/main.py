"""VarInspector main module: sets up the GUI and starts the application."""
import tkinter as tk
from tkinter import ttk
from .editor import CodeEditor
from .inspector import Inspector
from .config import Config

def main():
    """Initialize GUI, editor, and inspector, then start the Tk event loop."""
    root = tk.Tk()
    # ensure config directory and write prelude.py
    from pathlib import Path
    config_dir = Path.home() / '.config' / 'pyxion'
    config_dir.mkdir(parents=True, exist_ok=True)
    prelude_path = config_dir / 'prelude.py'
    if not prelude_path.exists():
        with open(prelude_path, 'w') as f:
            f.write('import numpy as np\nfrom math import *\n')
    # create default config.toml if missing
    config_path = config_dir / 'config.toml'
    if not config_path.exists():
        with open(config_path, 'w') as f:
            f.write('precision = 4\nfont_size = 20\n')
    root.title("Pyxion")
    # load configuration
    config = Config.load(config_dir)
    config.log()
    # set default windowed size and normal state
    root.geometry("520x340")
    root.attributes('-fullscreen', False)
    # hint to the WM (sway/Wayland) to open this window as floating
    root.wm_attributes('-type', 'dialog')

    paned = ttk.PanedWindow(root, orient=tk.HORIZONTAL)
    paned.pack(fill=tk.BOTH, expand=1)

    editor = CodeEditor(paned, config)
    inspector = Inspector(paned, editor, config)

    paned.add(editor.text_frame, weight=1)
    paned.add(inspector.frame, weight=1)

    # start inspection using a tweakable interval
    DEFAULT_INSPECT_INTERVAL = 1000  # milliseconds; adjust as needed
    inspector.start_inspection(interval=DEFAULT_INSPECT_INTERVAL)

    def _on_escape(event):
        # deselect selection if any, else exit
        for w in (editor.text, inspector.text):
            if w.tag_ranges("sel"):
                w.tag_remove("sel", "1.0", tk.END)
                return "break"
        root.quit()

    root.bind("<Escape>", _on_escape)
    root.mainloop()

if __name__ == "__main__":
    print("Starting pyxion.")
    main()
    print("Exited pyxion.")
