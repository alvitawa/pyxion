# Pyxion

Reactive python expression evaluator / calculator GUI for programmers.

Install:

```bash
pipx install pyxion
```

Run:

```bash
pyxion
```

**Pyxion has no safeguards.** The code you enter will be `exec`ed in the current context every time you make a change in
 the editor. If you don't know what that means, don't use this program.

Dev:
```bash
pipx install --editable .
```

## Configuration

Pyxion stores its configuration in the `~/.config/pyxion/` directory.

### `config.toml`

This file controls the application's appearance and behavior. If it doesn't exist, it will be created with default values upon first run.

Available options:

- `precision`: (Integer) The number of decimal places to display for floating-point numbers in the inspector. Default: `4`.
- `font_size`: (Integer) The font size used in the editor and inspector panes. Default: `20`.

Example `config.toml`:
```toml
precision = 4
font_size = 20
```

### `prelude.py`

This Python script is executed before your code in the editor. You can use it to import commonly used modules or define helper functions that will be available in your Pyxion sessions.

You need to use `pipx inject {package-name}` to install any packages you want to use in `prelude.py`. For example, if you want to use `numpy`, run:
```bash
pipx inject pyxion numpy
```

If it doesn't exist, a default `prelude.py` will be created with:
```python
import numpy as np
from math import *
```
You can customize this file to suit your needs. For example, you might add:
```python
import pandas as pd
from datetime import datetime, timedelta

def my_custom_function():
    print("Custom function executed!")
```
Any changes to `prelude.py` will take effect the next time you modify the code in the Pyxion editor (which triggers a re-evaluation).
