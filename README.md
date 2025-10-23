# colabtool

[![ci](https://github.com/schluchtenscheisser/colabtool/actions/workflows/ci.yml/badge.svg)](../../actions)

## Colab-Quickstart

**Zelle 1**
```python
%pip install -U "git+https://github.com/schluchtenscheisser/colabtool@v0.1.1"
import importlib, colabtool
importlib.reload(colabtool)
print("installiert:", colabtool.__file__)

**Zelle 2** (Beispiel-Start)

import os
os.environ.update({
    "COINGECKO_API_KEY": "",   # optional: Key oder leer
    "CG_FORCE_FREE": "1",
    "REQUIRE_MEXC": "1",
})

from colabtool.utils import pd
from colabtool import *
# hier deinen Pipeline-Code einfügen


Drive-Ordner (für Cache/Seeds)
/content/drive/MyDrive/crypto_tool/
  cache/
  seeds/


Releases

Installiere immer per Tag (z. B. @v0.1.1) für reproduzierbare Runs.
