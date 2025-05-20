"""Inspector module: evaluates editor code and displays variable values."""
import tkinter as tk
import tkinter.font as tkfont
import re
import sys

class Inspector:
    """Real-time variable inspector pane linked to the code editor."""
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
        """Begin periodic or event-driven inspection of editor content."""
        # initial inspection and bind to editor changes instead of polling
        self._inspect()
        self.editor.text.edit_modified(False)
        # bind inspector to editor modifications alongside existing handlers
        self.editor.text.bind("<<Modified>>", self._on_modified, add="+")

    def _on_modified(self, event=None):
        """Handle editor changes by triggering a new inspection cycle."""
        self._inspect()
        self.editor.text.edit_modified(False)

    def _inspect(self):
        """Evaluate the editor's code, extract variables, and display their values."""
        code = self.editor.text.get("1.0", tk.END)
        # replace ${X} tokens with variable names
        code = re.sub(r'\$\{(\d+)\}', lambda m: f"__var_{m.group(1)}", code)
        lines = code.splitlines()
        func_code = "def __varinspector():\n"
        var_names = set()
        var_order = []
        for idx, line in enumerate(lines, start=1):
            if not line.strip():
                continue
            if re.match(r'\s*([a-zA-Z_]\w*)\s*=', line):
                func_code += f"    {line}\n"
                var_name = re.match(r'\s*([a-zA-Z_]\w*)\s*=', line).group(1)
                var_names.add(var_name)
                var_order.append(var_name)
            else:
                temp_var = f"__var_{idx}"
                func_code += f"    {temp_var} = {line}\n"
                var_names.add(temp_var)
                var_order.append(temp_var)
        return_items = []
        for n in var_order:
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
            print(f"Inspection failed: {e}", file=sys.stderr)
            result = {'error': str(e)}
        self.text.config(state=tk.NORMAL)
        self.text.delete("1.0", tk.END)
        for k, v in result.items():
            self.text.insert(tk.END, f"{k}: {v}\n")
        self.text.config(state=tk.DISABLED)
