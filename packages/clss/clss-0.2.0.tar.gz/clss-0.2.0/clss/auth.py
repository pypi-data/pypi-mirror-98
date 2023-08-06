
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

import logging as log
from pathlib import Path
import pickle

class MissingCredentialsError(RuntimeError):
  pass

class GoogleAuth():
  SCOPE_SHEETS_RW = ['https://www.googleapis.com/auth/spreadsheets']
  SCOPE_DRIVE_RW = ['https://www.googleapis.com/auth/drive']
  SCOPE_SHEETS_RO = ['https://www.googleapis.com/auth/spreadsheets.readonly']
  SCOPE_DRIVE_RO = ['https://www.googleapis.com/auth/drive.readonly']
  SCOPE_READONLY = SCOPE_SHEETS_RO + SCOPE_DRIVE_RO
  SCOPE_FULL = SCOPE_SHEETS_RW + SCOPE_DRIVE_RW

  def __init__(self, credentials, token_file, scopes=None):
    self._cred_file = Path(credentials)
    self._token_file = Path(token_file)
    self._creds = None
    self._scopes = self.SCOPE_FULL if scopes is None else list(scopes)

  def new_token(self):
    log.info('initializing a new login token')
    if not self._cred_file.exists():
      raise MissingCredentialsError()

    if self._cred_file.stat().st_mode & 0o066:
      log.warning(f'file {self._cred_file} (mode=0o{self._cred_file.stat().st_mode:04o}) might be readable by other users!')
    flow = InstalledAppFlow.from_client_secrets_file(self._cred_file, self._scopes)
    self._creds = flow.run_local_server(port=0)
    self.save_credentials()
    return self._creds

  def refresh_token(self):
    log.info('refreshing login token')
    self._creds.refresh(Request())
    self.save_credentials()
    return self._creds

  def save_credentials(self):
    log.info(f'saving login token to {self._token_file}')
    assert self._creds
    with self._token_file.open('wb') as fil:
      pickle.dump(self._creds, fil)
    self._token_file.chmod(0o600)

  def load_token(self):
    log.info(f'loading login session from {self._token_file}')
    if not self._token_file.exists():
      return False
    try:
      with self._token_file.open('rb') as fil:
        self._creds = pickle.load(fil)
    except Exception as e:
      log.warning(f'failed to load session token file: {str(e)}')
      return False
    else:
      return True

  def login(self):
    log.info('authenticating')
    if not self.load_token():
      self.new_token()
    else:
      if self._creds.expired and self._creds.refresh_token:
        self.refresh_token()
      if not self._creds.valid:
        self.new_token()
    assert self._creds

  def get_service(self, name, vers):
    log.debug(f'building service for API {name=} {vers=}')
    if not self._creds:
      self.login()
    return build(name, vers, credentials=self._creds, cache_discovery=False)

