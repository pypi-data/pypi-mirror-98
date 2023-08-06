
from .a1syntax import A1Syntax
from .jsdict import jsdict
# from functools import cached_property

class Spreadsheet():
  def __init__(self, api, js):
    self._api = api
    self._js = js
    self._id = js.spreadsheetId
    self._url = js.spreadsheetUrl
    self.__dict__.update(js.properties)
    self.sheets = [v.properties for v in js.sheets]

  @staticmethod
  def fetch(api, id):
    req = api.spreadsheets().get(
      spreadsheetId=id,
      fields="""
spreadsheetId,
spreadsheetUrl,
properties(title),
sheets/properties(title,index,gridProperties(rowCount,columnCount))
""".replace('\n', '')
    )
    return Spreadsheet(api.spreadsheets(), jsdict.from_json(req.execute()))

  def fetch_values(self, idx, majorDimension='ROWS'):
    return jsdict.from_json(
      self._api.values().get(
        spreadsheetId=self._id,
        range=idx,
        majorDimension=majorDimension,
        valueRenderOption='UNFORMATTED_VALUE',
        dateTimeRenderOption='FORMATTED_STRING').execute())

  def clear_values(self, idx):
    return jsdict.from_json(self._api.values().clear(
      spreadsheetId=self._id,
      range=idx).execute())
  
  def update_values(self, idx, data):
    return jsdict.from_json(self._api.values().update(
      spreadsheetId=self._id,
      range=idx,
      valueInputOption='USER_ENTERED',
      body={'values': data}).execute())

  def append_values(self, idx, data):
    return jsdict.from_json(self._api.values().append(
      spreadsheetId=self._id,
      range=idx,
      valueInputOption='USER_ENTERED',
      body={'values': data}).execute())

  def __iter__(self):
    return self.sheets

  def __repr__(self):
    return f'Spreadsheet("{self._id}", sheets={[x.title for x in self.sheets]})'

  def __getitem__(self, idx):
    for w in self.sheets:
      if w.title == idx or w.index == idx:
        return w
    raise IndexError(f"sheet not found: {idx}")
  
# class Worksheet():
#   def __init__(self, doc, js):
#     self._doc = doc
#     self._js = js
#     self.__dict__.update(js.properties)
#     self.ix = A1Syntax(self.title)

#   @property
#   def shape(self):
#     return (self.gridProperties.rowCount, self.gridProperties.columnCount)
  
#   def __repr__(self):
#     return f'Worksheet({self.index}, "{self.title}", size={self.shape})'

#   def __getitem__(self, idx):
#     return self._doc.fetch_values(self.ix[idx])

#   def clear(self, range=None):
#     pass

#   def update(self, data, range=None):
#     pass
  
