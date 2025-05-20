import tkinter as tk
from tkinter import ttk
from .editor import CodeEditor
from .inspector import Inspector

def main():
    root = tk.Tk()
    root.title("VarInspector")
    # set default windowed size and normal state
    root.geometry("520x340")
    root.attributes('-fullscreen', False)
    # hint to the WM (sway/Wayland) to open this window as floating
    root.wm_attributes('-type', 'dialog')

    paned = ttk.PanedWindow(root, orient=tk.HORIZONTAL)
    paned.pack(fill=tk.BOTH, expand=1)

    editor = CodeEditor(paned)
    inspector = Inspector(paned, editor)

    paned.add(editor.text_frame, weight=1)
    paned.add(inspector.frame, weight=1)

    # start inspection using a tweakable interval
    DEFAULT_INSPECT_INTERVAL = 1000  # milliseconds; adjust as needed
    inspector.start_inspection(interval=DEFAULT_INSPECT_INTERVAL)
    root.mainloop()

if __name__ == "__main__":
    main()
