import tkinter as tk
import pygments
from pygments.lexers import PythonLexer
from pygments.styles import get_style_by_name

class CodeEditor:
    def __init__(self, parent):
        self.text_frame = tk.Frame(parent)
        self.text = tk.Text(self.text_frame, wrap=tk.NONE)
        self.text.pack(fill=tk.BOTH, expand=1)
        self._lexer = PythonLexer()
        self._style = get_style_by_name('default')
        self._configure_tags()
        self.text.bind("<<Modified>>", self._on_modified)
        self.text.edit_modified(False)

    def _configure_tags(self):
        for token, style in self._style:
            color = style['color']
            if color:
                self.text.tag_configure(str(token), foreground=f"#{color}")

    def _on_modified(self, event=None):
        code = self.text.get("1.0", tk.END)
        self._highlight(code)
        self.text.edit_modified(False)

    def _highlight(self, code):
        self.text.delete("1.0", tk.END)
        index = "1.0"
        for token, content in pygments.lex(code, self._lexer):
            self.text.insert(index, content, str(token))
            index = self.text.index(f"{index} + {len(content)} chars")
