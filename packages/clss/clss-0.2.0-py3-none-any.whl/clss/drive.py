
class GoogleDrive():
  def __init__(self, service):
    self._service = service

  def list(self, **kwargs):
    params = {
      'q': 'mimeType="application/vnd.google-apps.spreadsheet"',
      'corpora': 'user',
      'spaces': 'drive',
    }
    params.update(kwargs)

    while True:
      req = self._service.files().list(**params)
      resp = jsdict(req.execute())

      for f in resp.files:
        yield f
      
      if not resp.nextPageToken:
        break
      
      params['pageToken'] = resp.nextPageToken


