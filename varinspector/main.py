import tkinter as tk
from tkinter import ttk
from .editor import CodeEditor
from .inspector import Inspector

def main():
    root = tk.Tk()
    root.title("VarInspector")

    paned = ttk.PanedWindow(root, orient=tk.HORIZONTAL)
    paned.pack(fill=tk.BOTH, expand=1)

    editor = CodeEditor(paned)
    inspector = Inspector(paned, editor)

    paned.add(editor.text_frame, weight=3)
    paned.add(inspector.frame, weight=1)

    inspector.start_inspection()
    root.mainloop()

if __name__ == "__main__":
    main()
