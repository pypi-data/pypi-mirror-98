
from pathlib import Path

PKG_DIR = Path(__file__).parent

with (PKG_DIR / 'VERSION').open('rt') as f:
  __version__ = f.read().strip()

__all__ = (
  '__version__', # NB! Forced export of __version__.
  'PKG_DIR',
)

