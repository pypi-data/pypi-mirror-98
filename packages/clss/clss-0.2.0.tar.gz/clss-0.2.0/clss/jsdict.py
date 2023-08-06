

class nsdict(dict):
  """Namespace-like dictionary.

  Attribute access and regular dictionary key lookups are equivalent
  on this object. No overhead should be incurred over using this class
  instead of a regular `dict()`.

  >>> x = nsdict(foo=2, bar=[])
  >>> assert x.bar is x['bar']
  >>> x['bar'].append(1)
  >>> x.bar
  [1]
  >>> x.foo *= 2
  >>> x['foo']
  4

  """
  def __init__(self, *args, **kwargs):
    super().__init__(*args, **kwargs)
    self.__dict__ = self

  @classmethod
  def from_json(cls, obj):
    if isinstance(obj, dict):
      return cls((k, cls.from_json(v)) for k,v in obj.items())
    if isinstance(obj, list):
      return [cls.from_json(x) for x in obj]
    if isinstance(obj, tuple):
      return tuple(cls.from_json(x) for x in obj)
    return obj


class jsdict(nsdict):
  """JavaScript-like dictionary.

  This is like an `nsdict`, but accessing non-existent keys through
  attributes returns `None` instead of triggering an exception.

  >>> x = jsdict()
  >>> x.bar = 1
  >>> x
  {'bar': 1}
  >>> x.foo is None
  True

  """
  def __getattr__(self, k):
    return None
