"""Inspector module: evaluates editor code and displays variable values."""
import tkinter as tk
import tkinter.font as tkfont
import re
import sys
from pathlib import Path
import toml

class Inspector:
    """Real-time variable inspector pane linked to the code editor."""
    def __init__(self, parent, editor, config_dir):
        self.frame = tk.Frame(parent)
        self.editor = editor
        self.config_dir = config_dir
        self.text = tk.Text(self.frame, state=tk.DISABLED)
        # double the default font size
        font = tkfont.Font(font=self.text['font'], size=20)
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
        # replace ${X} and $X tokens with variable names
        code = re.sub(r'\$\{?(\d+)\}?', lambda m: f"__var_{m.group(1)}", code)
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
        # load prelude script text
        prelude_path = self.config_dir / 'prelude.py'
        prelude_code = ''
        if prelude_path.exists():
            try:
                prelude_code = prelude_path.read_text()
            except Exception as e:
                print(f"Failed to read prelude: {e}", file=sys.stderr)
        # load config.toml for precision
        config_path = self.config_dir / 'config.toml'
        precision = 4
        if config_path.exists():
            try:
                cfg = toml.loads(config_path.read_text())
                precision = int(cfg.get('precision', precision))
            except Exception as e:
                print(f"Failed to read config: {e}", file=sys.stderr)
        # execute prelude and user code in same namespace
        full_code = prelude_code + "\n" + func_code
        try:
            exec(full_code, namespace)
            result = namespace['__varinspector']()
        except Exception as e:
            print(f"Inspection failed: {e}", file=sys.stderr)
            result = {'error': str(e)}
        print(func_code)
        self.text.config(state=tk.NORMAL)
        self.text.delete("1.0", tk.END)
        for k, v in result.items():
            if isinstance(v, float):
                rounded_v = round(v, precision)
                display = format(rounded_v, f".{precision}f")
                if rounded_v != v:
                    display += "~"
            else:
                display = v
            self.text.insert(tk.END, f"{k}: {display}\n")
        self.text.config(state=tk.DISABLED)
