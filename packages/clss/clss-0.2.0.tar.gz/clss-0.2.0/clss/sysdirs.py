
from pathlib import Path
import sys
import os

def user_relative(pth):
  u = Path('~')
  try:
    return u / pth.relative_to(u.expanduser())
  except ValueError:
    return pth

def local_config():
  """Best guess for what the system's local config directory.

  E.g. ~/.config, ~/AppData/Local, etc.

  Returns a `Path` object.
  """
  if sys.platform.startswith('win'):
    return Path(os.getenv('LOCALAPPDATA', os.path.expanduser('~/AppData/Local')))
  elif sys.platform == 'darwin':
    return Path(os.path.expanduser('~/Library/Preferences'))
  else:
    return Path(os.getenv('XDG_CONFIG_HOME', os.path.expanduser("~/.config")))

def app_config(name):
  """Best guess for app-specific local config directory.

  E.g. ~/.config/appname

  The directory will be created if it doesn't exist.

  Returns a `Path` object.
  """
  conf_dir = local_config()
  if not conf_dir.exists():
    raise RuntimeError("user config dir does not exist: {conf_dir}")
  conf_dir = conf_dir / name
  conf_dir.mkdir(exist_ok=True)
  return conf_dir



