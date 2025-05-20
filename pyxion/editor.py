"""CodeEditor module: provides a text editor with syntax highlighting and state persistence."""
import tkinter as tk
import tkinter.font as tkfont
import pygments
from pygments.lexers import PythonLexer
from pygments.styles import get_style_by_name
from pathlib import Path
import toml
import os
import sys

class CodeEditor:
    """GUI code editor supporting syntax highlighting and loading/saving state."""
    def __init__(self, parent, config_dir):
        """Set up the text widget, load saved state, and configure syntax highlighting."""
        self.config_dir = config_dir
        # load font_size from config
        config_path = self.config_dir / 'config.toml'
        font_size = 20
        if config_path.exists():
            try:
                cfg = toml.loads(config_path.read_text())
                font_size = int(cfg.get('font_size', font_size))
            except Exception as e:
                print(f"Failed to read config: {e}", file=sys.stderr)
        self.text_frame = tk.Frame(parent)
        # line number gutter
        self.linenumbers = tk.Text(self.text_frame, width=2, padx=5, takefocus=0,
                                   border=0, background='lightgrey', state=tk.DISABLED,
                                   wrap=tk.NONE)
        self.linenumbers.pack(side=tk.LEFT, fill=tk.Y)
        self.text = tk.Text(self.text_frame, wrap=tk.NONE)
        # double the default font size
        font = tkfont.Font(font=self.text['font'], size=font_size)
        self.text.configure(font=font)
        # use same font for line numbers
        self.linenumbers.configure(font=font)
        self.text.pack(fill=tk.BOTH, expand=1)
        # load and sync with state file
        state_path = self.config_dir / 'state.py'
        if state_path.exists():
            with state_path.open('r') as f:
                content = f.read()
            self.text.insert('1.0', content)
        self._state_path = state_path
        self._lexer = PythonLexer()
        self._style = get_style_by_name('default')
        self._configure_tags()
        self.text.bind("<<Modified>>", self._on_modified)
        # update gutter whenever text changes
        self.text.bind("<<Modified>>", self._update_linenumbers, add="+")
        self.text.edit_modified(False)
        # ensure there is an empty row at end
        content = self.text.get("1.0", tk.END)
        if not content.endswith("\n\n"):
            self.text.insert(tk.END, "\n")
        # focus editor at end
        self.text.focus_set()
        # update line numbers
        self._update_linenumbers()
        # self.text.mark_set("insert", "end")
        # self.text.see("insert")

    def _configure_tags(self):
        """Create text tags for each pygments token style."""
        for token, style in self._style:
            color = style['color']
            if color:
                self.text.tag_configure(str(token), foreground=f"#{color}")

    def _on_modified(self, event=None):
        """Respond to text edits: re-highlight text and save state."""
        code = self.text.get("1.0", tk.END).strip(' \t\n')
        # self._highlight(code)
        # save state to file
        try:
            with self._state_path.open('w') as f:
                f.write(code)
        except Exception as e:
            print(f"Failed to save editor state: {e}", file=sys.stderr)
        self.text.edit_modified(False)

    def _highlight(self, code):
        """Apply pygments lexing to insert colored text tags."""
        self.text.delete("1.0", tk.END)
        index = "1.0"
        for token, content in pygments.lex(code, self._lexer):
            self.text.insert(index, content, str(token))
            index = self.text.index(f"{index} + {len(content)} chars")

    def _update_linenumbers(self, event=None):
        """Refresh the line number gutter."""
        self.linenumbers.config(state=tk.NORMAL)
        self.linenumbers.delete("1.0", tk.END)
        line_count = int(self.text.index('end-1c').split('.')[0])
        numbers = "\n".join(str(i) for i in range(1, line_count+1))
        # right-align line numbers via tag
        self.linenumbers.tag_configure("right", justify=tk.RIGHT)
        self.linenumbers.insert("1.0", numbers, "right")
        self.linenumbers.config(state=tk.DISABLED)
