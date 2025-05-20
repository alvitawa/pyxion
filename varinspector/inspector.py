import tkinter as tk
import tkinter.font as tkfont
import re

class Inspector:
    def __init__(self, parent, editor):
        self.frame = tk.Frame(parent)
        self.editor = editor
        self.text = tk.Text(self.frame, state=tk.DISABLED)
        # double the default font size
        font = tkfont.Font(font=self.text['font'])
        font.configure(size=font['size'] * 2)
        self.text.configure(font=font)
        self.text.pack(fill=tk.BOTH, expand=1)

    def start_inspection(self, interval=1000):
        # initial inspection and bind to editor changes instead of polling
        self._inspect()
        self.editor.text.edit_modified(False)
        self.editor.text.bind("<<Modified>>", self._on_modified)

    def _on_modified(self, event=None):
        self._inspect()
        self.editor.text.edit_modified(False)

    def _inspect(self):
        code = self.editor.text.get("1.0", tk.END)
        var_names = set(re.findall(r'\b([a-zA-Z_]\w*)\b', code))
        func_code = "def __varinspector():\n"
        for line in code.splitlines():
            func_code += "    " + line + "\n"
        func_code += "    return {" + ", ".join(f"'{n}': {n}" for n in var_names) + "}\n"
        namespace = {}
        try:
            exec(func_code, namespace)
            result = namespace['__varinspector']()
        except Exception as e:
            result = {'error': str(e)}
        self.text.config(state=tk.NORMAL)
        self.text.delete("1.0", tk.END)
        for k, v in result.items():
            self.text.insert(tk.END, f"{k}: {v}\n")
        self.text.config(state=tk.DISABLED)
