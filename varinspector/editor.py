"""CodeEditor module: provides a text editor with syntax highlighting and state persistence."""
import tkinter as tk
import tkinter.font as tkfont
import pygments
from pygments.lexers import PythonLexer
from pygments.styles import get_style_by_name
from pathlib import Path
import os
import sys

class CodeEditor:
    """GUI code editor supporting syntax highlighting and loading/saving state."""
    def __init__(self, parent):
        """Set up the text widget, load saved state, and configure syntax highlighting."""
        self.text_frame = tk.Frame(parent)
        self.text = tk.Text(self.text_frame, wrap=tk.NONE)
        # double the default font size
        font = tkfont.Font(font=self.text['font'])
        font.configure(size=font['size'] * 2)
        self.text.configure(font=font)
        self.text.pack(fill=tk.BOTH, expand=1)
        # load and sync with state file
        config_path = Path.home() / '.config' / 'pyxion'
        config_path.parent.mkdir(parents=True, exist_ok=True)
        state_path = config_path / 'state.py'
        if state_path.exists():
            with open(state_path, 'r') as f:
                content = f.read()
            self.text.insert('1.0', content)
        self._state_path = config_path
        self._lexer = PythonLexer()
        self._style = get_style_by_name('default')
        self._configure_tags()
        self.text.bind("<<Modified>>", self._on_modified)
        self.text.edit_modified(False)

    def _configure_tags(self):
        """Create text tags for each pygments token style."""
        for token, style in self._style:
            color = style['color']
            if color:
                self.text.tag_configure(str(token), foreground=f"#{color}")

    def _on_modified(self, event=None):
        """Respond to text edits: re-highlight text and save state."""
        code = self.text.get("1.0", tk.END)
        self._highlight(code)
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
