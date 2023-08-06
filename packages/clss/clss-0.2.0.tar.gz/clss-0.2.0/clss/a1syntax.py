
class A1Syntax():
  """Class for translating from numeric canges into A1-syntax.

  >>> A1Syntax()[0,0]
  'A1'
  >>> ix = A1Syntax('sheet')
  >>> ix[:,2], ix.T[:,2]
  ("'sheet'!C:C", "'sheet'!3:3")
  >>> ix[2,:]
  "'sheet'!3:3"
  >>> ix[2:,1], ix.T[2:,1]
  ("'sheet'!B3:B", "'sheet'!C2:2")
  >>> ix[3,1:]
  "'sheet'!B4:4"
  """

  @staticmethod
  def col_name(idx):
    res = []
    while True:
      idx,r = divmod(idx, 26)
      res.append(chr(65 + r))
      if not idx:
        break
    return ''.join(res)

  @staticmethod
  def row_name(idx):
    return f'{idx+1}'

  def __init__(self, sheet=None, transposed=False):
    self._name = sheet
    self._safe = f"""'{sheet.replace("'", "''")}'""" if sheet else None
    self._transposed = transposed

  @property
  def T(self):
    return A1Syntax(self._name, not self._transposed)

  def _slice(self, idx):
    if not isinstance(idx, slice):
      return (idx, idx)
    
    if idx.step is not None and idx.step != 1:
      raise ValueError("worksheet slice must have a step of None or 1")

    if idx.start is None and idx.stop is None:
      return None, None

    return idx.start or 0, idx.stop

  def _make_absolute(self, s):
    return f"{self._safe}!{s}" if self._safe else s
  
  def __getitem__(self, idx):
    if idx is None:
      return self._safe
    if isinstance(idx, str):
      return self._make_absolute(idx)

    if not isinstance(idx, tuple):
      rs = self._slice(idx)
      cs = None, None
    else:
      rs = self._slice(idx[0])
      cs = self._slice(idx[1])

    if cs[1] is None and rs[1] is None:
      # Special case, selecting entire sheet worksheet by simply
      # specifying its name. This works in some parts of the Sheets
      # API.
      if cs[0] in (0, None) and rs[0] in (0, None) and self._safe:
        return self._safe

      # I know of no way to do it when there's an upper left corner
      # specified for the "infinite" sub-table.
      raise ValueError("range cannot be unbounded in both rows and columns")

    if self._transposed:
      rs, cs = cs, rs

    rstr = ''
    if cs[0] is not None:
      rstr += self.col_name(cs[0])
    if rs[0] is not None:
      rstr += self.row_name(rs[0])

    if rs[0] == rs[1] and cs[0] == cs[1] and None not in (rs[0], cs[0]):
      return self._make_absolute(rstr)
    else:
      rstr += ':'

    if cs[1] is not None:
      rstr += self.col_name(cs[1])
    if rs[1] is not None:
      rstr += self.row_name(rs[1])

    return self._make_absolute(rstr)
    
    
