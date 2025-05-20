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
        lines = code.splitlines()
        func_code = "def __varinspector():\n"
        var_names = set()
        for idx, line in enumerate(lines, start=1):
            if not line.strip():
                continue
            if re.match(r'\s*([a-zA-Z_]\w*)\s*=', line):
                func_code += f"    {line}\n"
                var_name = re.match(r'\s*([a-zA-Z_]\w*)\s*=', line).group(1)
                var_names.add(var_name)
            else:
                temp_var = f"__var_{idx}"
                func_code += f"    {temp_var} = {line}\n"
                var_names.add(temp_var)
        return_items = []
        for n in var_names:
            if n.startswith("__var_"):
                idx = n.split("_")[-1]
                return_items.append(f"'{idx}': {n}")
            else:
                return_items.append(f"'{n}': {n}")
        func_code += "    return {" + ", ".join(return_items) + "}\n"
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
